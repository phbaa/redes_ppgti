#!/usr/bin/env python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import Intf, TCLink
from datetime import datetime

class LinuxRouter(Node):
    "Um Node com IP forwarding habilitado."

    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl -w net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl -w net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()


class NetworkTopo(Topo):
    "Topologia com quatro roteadores interligados."

    def build(self, **_opts):

        # Roteadores
        r0 = self.addNode('r0', cls=LinuxRouter, ip='172.18.0.10/16')
        r1 = self.addNode('r1', cls=LinuxRouter, ip='192.168.200.2/30')
        r2 = self.addNode('r2', cls=LinuxRouter, ip='172.19.0.10/16')
        r3 = self.addNode('r3', cls=LinuxRouter, ip='172.20.0.10/16')

        # Switches para redes externas
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')

        # Opções de controle na rede
        #linkopts = dict(cls=TCLink, bw=1000, delay='0.1ms', max_queue_size=100, use_htb=True)
        linkopts = dict(cls=TCLink, bw=1000, use_htb=True)

        # Conexões com redes externas
        self.addLink(s1, r0, intfName2='r0-eth1', params2={'ip': '172.18.0.10/16'}, **linkopts)
        self.addLink(s2, r2, intfName2='r2-eth1', params2={'ip': '172.19.0.10/16'}, **linkopts)
        self.addLink(s3, r3, intfName2='r3-eth2', params2={'ip': '172.20.0.10/16'}, **linkopts)

        # Links entre roteadores
        self.addLink(r0, r1,
                     intfName1='r0-eth2', params1={'ip': '192.168.200.1/30'},
                     intfName2='r1-eth1', params2={'ip': '192.168.200.2/30'}, **linkopts)

        self.addLink(r2, r1,
                     intfName1='r2-eth2', params1={'ip': '192.168.201.1/30'},
                     intfName2='r1-eth2', params2={'ip': '192.168.201.2/30'}, **linkopts)

        self.addLink(r1, r3,
                     intfName1='r1-eth3', params1={'ip': '192.168.202.1/30'},
                     intfName2='r3-eth1', params2={'ip': '192.168.202.2/30'}, **linkopts)


def run():
    "Executa a topologia"
    topo = NetworkTopo()
    net = Mininet(topo=topo, link=TCLink, waitConnected=True)

    # Interfaces externas conectadas aos switches s1, s2 e s3
    s1 = net['s1']
    s2 = net['s2']
    s3 = net['s3']
    _intf = Intf( "br-123456789012", node=s1 )
    _intf = Intf( "br-123456789012", node=s2 )
    _intf = Intf( "br-123456789012", node=s3 )

    net.start()

    # Sincroniza o relógio de todos os roteadores com o do host
    now = datetime.now().strftime('%m%d%H%M%Y.%S')
    for router in ['r0', 'r1', 'r2', 'r3']:
        net[router].cmd(f'date {now}')


    # Adicionando rotas em cada roteador

    # Roteadores de borda: default para r1
    net['r0'].cmd('ip route add default via 192.168.200.2')
    net['r2'].cmd('ip route add default via 192.168.201.2')
    net['r3'].cmd('ip route add default via 192.168.202.1')

    # r1: rotas específicas para redes externas
    net['r1'].cmd('ip route add 172.18.0.0/16 via 192.168.200.1')
    net['r1'].cmd('ip route add 172.19.0.0/16 via 192.168.201.1')
    net['r1'].cmd('ip route add 172.20.0.0/16 via 192.168.202.2')

    #return net

    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()