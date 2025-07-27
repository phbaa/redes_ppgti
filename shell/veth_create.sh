#!/bin/bash

REDE="172.20."
BRIDGE=$(ip -o -f inet addr show | awk -v rede="$REDE" '$4 ~ rede {print $2}' | head -n1)

if [ -z "$BRIDGE" ]; then
    echo "Nenhuma interface encontrada para a rede $REDE"
    exit 1
fi

echo "Interface $BRIDGE encontrada para rede $REDE"

# Criar par veth: veth-host <-> veth-br
sudo ip link add veth-host type veth peer name veth-br

# Colocar a interface do lado "bridge" na bridge do Docker / Mininet
sudo ip link set veth-br master "$BRIDGE"

# Ativar ambas as interfaces
sudo ip link set veth-host up
sudo ip link set veth-br up

# Atribuir IP ao lado host
sudo ip addr add 172.20.0.98/16 dev veth-host

# Deleta rota antiga (criada pelo docker)
sudo ip addr del 172.20.0.1/16 dev "$BRIDGE" # Bridge criada pelo docker