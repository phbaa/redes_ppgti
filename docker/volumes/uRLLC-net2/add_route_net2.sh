#!/bin/bash

# Configura a rota padrão
ip route del default
ip route add default via 172.19.0.10
exec tail -f /dev/null