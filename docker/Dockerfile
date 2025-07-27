FROM ubuntu

RUN apt update && apt install -y \
    python3 \
    python3-pip \
    libpcap-dev \
    iputils-ping \
    iproute2 \
    iperf \
    curl \
    tcpdump \
    netcat-openbsd \
    && apt clean

RUN pip3 install --break-system-packages scapy prometheus_client

CMD ["tail", "-f", "/dev/null"]
