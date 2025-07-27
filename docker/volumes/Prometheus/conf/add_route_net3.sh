#!/bin/sh

# Altera a rota padrão
ip route del default
ip route add default via 172.20.0.10

# Executa o Prometheus normalmente
exec /bin/prometheus --config.file=/etc/prometheus/prometheus.yml --storage.tsdb.path=/data