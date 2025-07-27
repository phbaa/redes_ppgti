### ✅ Passo a passo:

## 🚀 Roteiro de Execução dos Testes

### 1. Clonar o repositório

```bash
git clone https://github.com/phbaa/redes_ppgti
cd redes_ppgti
````

### 2. Estrutura esperada do projeto

```
redes_ppgti/
├── docker/
├── python/
└── shell/
```

---

## ⚙️ Montando o cenário

### 1. Build da imagem Docker customizada

```bash
cd docker
docker build -t ubuntu-custom .
```

### 2. Subindo os containers com Docker Compose

```bash
docker compose up -d
```

### 3. Atualizando bridges da rede (Mininet)

```bash
cd ../shell
./atualiza_bridges.sh
./veth_create.sh
```

### 4. Executando o script de rede do Mininet

```bash
cd ../python
python3 mininet-network.py
```

---

## 🧪 Executando os testes 
#### 💡 (Executar cada Servidor e Cliente em um terminal diferente)

### Servidor

```bash
docker exec -it server python3 /conf/socket_tcp_receiver_echo.py
```

### Cliente URLLC1

```bash
docker exec -it urllc1 python3 /conf/socket_tcp_sender_receiver.py
```

### Cliente URLLC2

```bash
docker exec -it urllc2 python3 /conf/socket_tcp_sender_receiver.py
```

### Servidor 2 (iperf)

```bash
docker exec -it server2 iperf -s
```

### Cliente EMBB1 (iperf)

```bash
docker exec -it embb1 iperf -t 500 -i 1 -c 172.20.0.101
```

### Cliente EMBB2 (iperf)

```bash
docker exec -it embb2 iperf -t 500 -i 1 -c 172.20.0.101
```

### No Mininet

```bash
r1 python3 sniffer-r1.py
```

---

## 📊 Acessando o Dashboard no Navegador

1. Acesse: [http://localhost:3000](http://localhost:3000)
2. Faça login com:

   * Usuário: `admin`
   * Senha: `admin`
3. No menu lateral, vá em **Connections > Data sources > Add new data sources**
4. Selecione **Prometheus**
5. Em **Connection > Prometheus server URL**, preencha:

```
http://prometheus:9090
```

6. Clique em **Save & test**
7. No menu lateral, vá em **Dashboards > New > Import**
8. Importe o arquivo `grafana_dashboard.json`

---

## 📌 Observações

* Cenário testado no Ubuntu22
* Docker, Docker Compose, Python3 e Mininet devem estar instalados, se necessário executar comandos com sudo.
* Execute os comandos na ordem para evitar erros.

---
