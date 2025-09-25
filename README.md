# 📦 Real-Time Notifications (Mini Demo)  
_Notificações em tempo real com RabbitMQ + Python + WebSockets_

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![RabbitMQ](https://img.shields.io/badge/RabbitMQ-3.12-orange)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![Status](https://img.shields.io/badge/status-prototype-lightgrey)

Este projeto demonstra um **sistema de notificações em tempo real** para um delivery.  
Ele simula avisos ao cliente quando o pedido é **PREPARADO → ENVIADO → ENTREGUE**, utilizando **RabbitMQ** como broker de mensagens.

---

## ✨ Funcionalidades
- **Producer**: simula pedidos mudando de status  
- **RabbitMQ**: faz o roteamento e enfileiramento dos eventos  
- **Notifier (FastAPI + WebSocket)**: consome da fila e envia em tempo real  
- **Client (HTML)**: recebe as notificações no navegador  

---

## 🔧 Pré-requisitos
- [Python 3.9+](https://www.python.org/)  
- [Docker + Docker Compose](https://docs.docker.com/get-docker/)  
- Navegador para abrir o `client.html`

---

## 📂 Estrutura
realtime-notify/
├─ docker-compose.yml # sobe o RabbitMQ com UI
├─ .env # variáveis de ambiente
├─ notifier/
│ ├─ requirements.txt # FastAPI, Uvicorn, aio-pika
│ └─ app.py # consumidor da fila + servidor WebSocket
├─ producer/
│ ├─ requirements.txt # aio-pika
│ └─ simulate.py # simula pedidos e publica eventos
└─ web/
└─ client.html # cliente WebSocket simples

yaml
Copiar código

---

## 🚀 Como rodar

### 1) Subir o RabbitMQ
Na raiz do projeto:
```bash
docker compose up -d
UI em: http://localhost:15672

Login: guest | Senha: guest

2) Rodar o Notifier
Em outra janela:

bash
Copiar código
cd notifier
pip install -r requirements.txt
python -m uvicorn app:app --reload --port 8000 --ws websockets
Teste em http://localhost:8000/health.

3) Abrir o Cliente Web
Abra web/client.html no navegador e clique em Conectar.
Use alice, bob ou carol como user_id.

4) Rodar o Producer
Em outra janela:

bash
Copiar código
cd producer
pip install -r requirements.txt
python simulate.py
As mensagens aparecerão no navegador em tempo real.

🎓 Demonstrações
Tempo real: cliente recebe eventos sem refresh

Isolamento: cada usuário recebe só seus próprios pedidos

RabbitMQ UI: em Queues → order.status.notify, veja o fluxo das mensagens

Tolerância a falhas: se o Notifier cair, mensagens ficam na fila e são entregues quando ele volta

✅ Objetivos educacionais
Este protótipo cobre os requisitos do PBL:

Escolha: RabbitMQ (simples e rápido). Kafka serviria para cenários de alto volume/replay.

Arquitetura: Producer → RabbitMQ → Notifier → Cliente.

Escalabilidade: basta rodar múltiplos Notifiers em paralelo.

Disponibilidade: filas garantem entrega mesmo se consumidores caírem.
