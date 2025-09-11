# Kafka Delivery Notifications Demo

Protótipo simples de **notificações em tempo real** para um app de delivery usando **Kafka (Redpanda)** e **Python**.

## 🧱 Arquitetura

```
[producer: Serviço de Pedidos] -> (topic: notificacoes) -> [consumer: Serviço de Notificações]
```

- **Ordem por pedido** garantida via `key=pedido_id`.
- **Escala** com partições (3) e **grupos de consumidores**.
- **Confiabilidade** via `acks=all` no produtor.

---

## 🚀 Como rodar

### 1) Subir o Kafka (Redpanda via Docker)
Crie/edite o arquivo `docker-compose.yml` (já incluído no projeto) e rode:

```bash
docker compose up -d
```

Crie o tópico (3 partições, 1 réplica – ideal para protótipo local):

```bash
docker exec -it redpanda rpk topic create notificacoes -p 3 -r 1 --brokers localhost:9092
```

> `-p 3` = 3 partições (escala) • `-r 1` = 1 réplica (ambiente local)

### 2) Instalar dependências Python

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows (PowerShell)
# .venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

### 3) Executar

Em um terminal, **consumer**:

```bash
python consumer.py
```

Em outro terminal, **producer**:

```bash
python producer.py
```

Você verá logs no *producer* (partição/offset) e "notificações" no *consumer*.

---

## 🧪 Dicas de Teste

- Abra **2 ou mais consumidores** com o mesmo `GROUP_ID` para ver o *rebalance* entre partições.
- Mude o `pedido_id` no `producer.py` para gerar chaves diferentes e observar a distribuição entre partições.
- Para latência mínima, reduza `linger_ms` no produtor.

---

## 🔧 Troubleshooting

- **`NoBrokersAvailable`**: verifique se o container `redpanda` está rodando e `localhost:9092` acessível.
- **Tópico não existe**: confirme a criação com `docker exec -it redpanda rpk topic list`.
- **Permissão no Windows** ao ativar venv: abra PowerShell como admin e execute `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`.

---

## 📄 Licença

MIT
