#!/bin/bash

ARQUIVO="../python/mininet-network.py"

# Função para identificar a interface de uma rede e atualizar a linha correspondente
atualizar_bridge() {
    REDE=$1
    NODE=$2

    # Descobre a interface associada à rede
    BRIDGE=$(ip -o -f inet addr show | awk -v rede="$REDE" '$4 ~ rede {print $2}' | head -n1)

    if [ -z "$BRIDGE" ]; then
        echo "Nenhuma interface encontrada para a rede $REDE"
        return 1
    fi

    echo "Interface $BRIDGE encontrada para rede $REDE (node=$NODE)"

    # Atualiza a linha correspondente no mininet.py
    sed -i "s|_intf = Intf( \"br-.*\", node=$NODE )|_intf = Intf( \"$BRIDGE\", node=$NODE )|" "$ARQUIVO"
}

# Executa a substituição para cada rede e switch correspondente
atualizar_bridge "172.18." "s1"
atualizar_bridge "172.19." "s2"
atualizar_bridge "172.20." "s3"

echo "Todas as bridges foram atualizadas no arquivo $ARQUIVO"