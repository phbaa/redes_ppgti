import socket
import time
from prometheus_client import start_http_server, Gauge
import threading

# Métrica Prometheus para expor a latência em milissegundos
latency_gauge = Gauge('latency_ms', 'Latência unidirecional TCP em milissegundos')

# Configuração de IP e porta onde o servidor irá escutar
HOST = '172.20.0.100'
PORT = 5000

def handle_connection(conn, addr):
    try:
        print(f"[SERVIDOR] Conexão recebida de {addr}")

        # Buffer para armazenar dados recebidos parcialmente
        buffer = b""

        while True:
            data = conn.recv(1024)
            if not data:
                break  # Cliente fechou a conexão

            buffer += data

            while b'\n' in buffer:
                linha, buffer = buffer.split(b'\n', 1)
                if not linha:
                    continue

                try:
                    # Converte o timestamp enviado pelo cliente
                    sent_ts_ns = int(linha.decode())

                    # Timestamp atual do servidor (quando recebe)
                    recv_ts_ns = time.time_ns()

                    # Calcula a latência em milissegundos
                    latency_ms = (recv_ts_ns - sent_ts_ns) / 1_000_000

                    print(f"[SERVIDOR] Latência: {latency_ms:.2f} ms")

                    # Atualiza a métrica Prometheus
                    latency_gauge.set(latency_ms)

                    # Envia de volta o mesmo timestamp recebido do cliente
                    response = linha + b'\n'
                    conn.sendall(response)

                except Exception as e:
                    print(f"[SERVIDOR] Erro ao processar linha: {e}")

    except Exception as e:
        print(f"[SERVIDOR] Erro na conexão com {addr}: {e}")
    finally:
        conn.close()
        print(f"[SERVIDOR] Conexão encerrada com {addr}")

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"[SERVIDOR] Escutando em {HOST}:{PORT}...")

        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_connection, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    # Inicia o servidor de métricas Prometheus na porta 8000
    start_http_server(8000)

    # Inicia o servidor TCP
    start_server()