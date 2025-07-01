from scapy.all import *
import time

def process(pkt):
    if Raw in pkt:
        try:
            # Decodifica o timestamp dentro do payload
            sent_ts = float(pkt[Raw].load.decode())
            # Captura a hora atual
            now = time.time()
            # Calcula a latência em ms
            latency = (now - sent_ts) * 1000
            print(f"Latência: {latency:.3f} ms")
        except Exception as e:
            print(f"Erro ao processar pacote: {e}")

sniff(filter="tcp port 5000", prn=process, store=0)