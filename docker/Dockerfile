FROM ubuntu

RUN apt update && apt install -y \
    python3 \
    python3-pip \
    iproute2 \
    iperf \
    libpcap-dev \
    && apt clean

RUN pip3 install --break-system-packages scapy prometheus_client

CMD ["tail", "-f", "/dev/null"]
