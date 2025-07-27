#!/usr/bin/env python3

import subprocess

# Interfaces
IFACES = ['r1-eth1', 'r1-eth2', 'r1-eth3']

def remove_tc():
    print("Removendo configurações tc")

    for iface in IFACES:
        print(f"Limpando {iface}...")
        subprocess.call(f'tc qdisc del dev {iface} root 2>/dev/null || true', shell=True)

    print("Limpeza concluída.")

def main():
    remove_tc()

if __name__ == '__main__':
    main()