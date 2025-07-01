import time
import sys
from scapy.all import send, IP, TCP, Raw

# --- Configurações ---
IP_SERVIDOR = "172.20.0.100"
PORTA_SERVIDOR = 5000
INTERVALO_ENTRE_PACOTES = 1

def sender_tcp_com_payload():
    """
    Envia pacotes TCP SYN contendo um timestamp no payload.
    """
    print(f"[*] Iniciando envio de pacotes TCP SYN com timestamp para {IP_SERVIDOR}:{PORTA_SERVIDOR}...")
    seq_num = 0
    while True:
        try:
            seq_num += 1
            
            # Pega o timestamp atual e o converte para uma string de bytes
            timestamp_str = str(time.time())
            payload = bytes(timestamp_str, 'utf-8')
            
            # Monta o pacote: IP / TCP (com flag SYN) / Payload com o timestamp
            pacote = IP(dst=IP_SERVIDOR) / TCP(dport=PORTA_SERVIDOR, flags='S', seq=seq_num) / Raw(load=payload)

            # Envia o pacote e não espera pela resposta
            send(pacote, verbose=0)
            
            print(f"[CLIENTE] Pacote SYN (SEQ={seq_num}) com timestamp enviado.")
            time.sleep(INTERVALO_ENTRE_PACOTES)

        except KeyboardInterrupt:
            print("\n[CLIENTE] Envio interrompido.")
            sys.exit(0)

if __name__ == "__main__":
    sender_tcp_com_payload()