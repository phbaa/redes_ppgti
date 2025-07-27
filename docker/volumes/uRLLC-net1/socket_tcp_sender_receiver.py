import socket
import time
from prometheus_client import start_http_server, Gauge

# -------------------------
# CONFIGURAÇÕES
# -------------------------

IP_SERVIDOR = '172.20.0.100'     # IP do servidor TCP (altere conforme necessário)
PORTA_SERVIDOR = 5000         # Porta onde o servidor escuta
INTERVALO = 1                 # Intervalo entre cada medição (segundos)

# -------------------------
# MÉTRICA PROMETHEUS
# -------------------------

# Gauge: métrica do tipo que pode aumentar ou diminuir (útil para latência)
rtt_gauge = Gauge('rtt_urllc1_ms', 'Round-Trip Time (RTT) em milissegundos')

# -------------------------
# FUNÇÃO PRINCIPAL DO CLIENTE
# -------------------------

def cliente_rtt():
    # Cria um socket TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Conecta ao servidor
        s.connect((IP_SERVIDOR, PORTA_SERVIDOR))
        print(f"[Cliente] Conectado ao servidor {IP_SERVIDOR}:{PORTA_SERVIDOR}")

        while True:
            try:
                # Gera timestamp atual em nanossegundos
                timestamp_ns = time.time_ns()

                # Envia o timestamp como string codificada + \n (para facilitar a separação da mensagem)
                s.sendall(str(timestamp_ns).encode() + b'\n')

                # Marca o tempo exato após envio (para cálculo de RTT)
                send_time = time.time_ns()

                # Aguarda a resposta (eco) do servidor
                data = b''  # Inicializa o buffer de dados recebidos

                # Continua recebendo até encontrar o caractere '\n',
                # que indica o fim da mensagem (como no envio)
                while not data.endswith(b'\n'):
                    chunk = s.recv(1024)  # Recebe até 1024 bytes do servidor
                    if not chunk:
                        # Se não receber nada, significa que a conexão foi encerrada
                        print("[Cliente] Conexão encerrada pelo servidor")
                        return
                    data += chunk  # Acumula os dados no buffer

                # Marca o tempo de recebimento (em nanossegundos)
                recv_time = time.time_ns()

                # Calcula o RTT: tempo total entre envio e recebimento da resposta
                rtt_ns = recv_time - send_time
                rtt_ms = rtt_ns / 1_000_000  # Converte nanossegundos → milissegundos

                # Exibe o RTT no terminal
                print(f"[Cliente] RTT: {rtt_ms:.2f} ms")

                # Atualiza a métrica Prometheus
                rtt_gauge.set(rtt_ms)

                # Aguarda o intervalo definido antes de enviar o próximo pacote
                time.sleep(INTERVALO)

            except Exception as e:
                print(f"[Erro] Falha ao medir RTT: {e}")
                break

# -------------------------
# PONTO DE ENTRADA DO SCRIPT
# -------------------------

if __name__ == "__main__":
    # Inicia o servidor HTTP do Prometheus na porta 8000
    print("[Cliente] Iniciando servidor de métricas Prometheus na porta 8000...")
    start_http_server(8000)  # Métricas disponíveis em http://localhost:8000/metrics

    # Inicia a lógica de medição de RTT
    cliente_rtt()
