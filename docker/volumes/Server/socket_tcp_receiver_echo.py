import socket
import threading

def handle_client(conn, addr):
    """
    Função que trata a comunicação com um cliente específico.
    Recebe dados e faz echo de volta enquanto o cliente estiver conectado.
    """
    with conn:
        print(f"[Servidor] Conexão estabelecida com {addr}")
        while True:
            data = conn.recv(1024)  # Recebe até 1024 bytes
            if not data:
                # Cliente desconectou
                print(f"[Servidor] Cliente {addr} desconectado.")
                break
            # Envia os dados recebidos de volta para o cliente (echo)
            conn.sendall(data)

def echo_server(host='172.20.0.100', port=5000):
    """
    Servidor TCP que aceita múltiplas conexões simultâneas.
    Cada cliente é tratado em uma thread separada.
    """
    # Cria o socket TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Permite reutilizar o endereço rapidamente após encerrar o servidor
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Associa o socket ao endereço IP e porta
        s.bind((host, port))
        
        # Coloca o socket em modo de escuta
        s.listen()
        print(f"[Servidor] Escutando em {host}:{port}...")

        # Loop principal: aceita conexões continuamente
        while True:
            conn, addr = s.accept()  # Aceita uma nova conexão
            # Cria e inicia uma nova thread para lidar com essa conexão
            client_thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            client_thread.start()

if __name__ == "__main__":
    echo_server()
