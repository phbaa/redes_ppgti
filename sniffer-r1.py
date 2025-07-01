#!/usr/bin/env python3

import time
import subprocess
from scapy.all import sniff, Raw

LATENCY_THRESHOLD_MS = 25.0
HYSTERESIS_MS = 1.0
MIN_CONSECUTIVE_APPLY = 5
MIN_CONSECUTIVE_REMOVE = 5

priority_applied = False
consecutive_high_latency = 0
consecutive_low_latency = 0

# Interfaces que este script vai aplicar tc diretamente (no contexto de r1)
IFACES = ['r1-eth1', 'r1-eth2', 'r1-eth3']

def apply_tc():
    global priority_applied
    if priority_applied:
        return

    print("Aplicando prioridade via tc...")

    tc_cmd_template = '''
    tc qdisc del dev {iface} root 2>/dev/null || true
    tc qdisc add dev {iface} root handle 1: htb default 20
    tc class add dev {iface} parent 1: classid 1:1 htb rate 1000mbit
    tc class add dev {iface} parent 1:1 classid 1:10 htb rate 800mbit ceil 1000mbit prio 0
    tc class add dev {iface} parent 1:1 classid 1:20 htb rate 200mbit ceil 1000mbit prio 1
    tc qdisc add dev {iface} parent 1:10 handle 10: fq_codel limit 30
    tc filter add dev {iface} protocol ip parent 1:0 prio 1 u32 match ip dport 5000 0xffff flowid 1:10
    '''

    for iface in IFACES:
        subprocess.call(tc_cmd_template.format(iface=iface), shell=True)

    priority_applied = True

def remove_tc():
    global priority_applied
    if not priority_applied:
        return

    print("Removendo prioridade via tc...")

    for iface in IFACES:
        subprocess.call(f'tc qdisc del dev {iface} root 2>/dev/null || true', shell=True)

    priority_applied = False

def process_packet(pkt):
    global priority_applied, consecutive_high_latency, consecutive_low_latency

    if Raw in pkt:
        try:
            sent_ts = float(pkt[Raw].load.decode())
            now = time.time()
            latency = (now - sent_ts) * 1000
            print(f"[LATÊNCIA] {latency:.3f} ms")

            if latency > LATENCY_THRESHOLD_MS:
                consecutive_high_latency += 1
                consecutive_low_latency = 0
            elif latency < (LATENCY_THRESHOLD_MS - HYSTERESIS_MS):
                consecutive_low_latency += 1
                consecutive_high_latency = 0
            else:
                consecutive_high_latency = 0
                consecutive_low_latency = 0

            if consecutive_high_latency >= MIN_CONSECUTIVE_APPLY and not priority_applied:
                apply_tc()
            elif consecutive_low_latency >= MIN_CONSECUTIVE_REMOVE and priority_applied:
                remove_tc()

        except Exception as e:
            print(f"[ERRO] Não foi possível processar o pacote: {e}")

def main():
    print("Monitorando latência URLLC com tc em várias interfaces...")

    sniff(filter="tcp port 5000", prn=process_packet, store=0)

if __name__ == '__main__':
    main()