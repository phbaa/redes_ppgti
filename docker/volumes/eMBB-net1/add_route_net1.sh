#!/bin/bash

# Configura a rota padrão
ip route del default
ip route add default via 172.18.0.10
exec tail -f /dev/null