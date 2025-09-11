import json
from kafka import KafkaConsumer

BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC = "notificacoes"
GROUP_ID = "notificador-v1"  # permite escalar múltiplos consumidores em grupo

def get_consumer():
    return KafkaConsumer(
        TOPIC,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        group_id=GROUP_ID,
        enable_auto_commit=True,           # simples p/ protótipo
        auto_offset_reset="earliest",      # lê desde o começo se não houver commit
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        key_deserializer=lambda v: v.decode("utf-8") if v else None,
        consumer_timeout_ms=0,             # bloqueante
        max_poll_records=50,
    )

def push_fake(user_id: int, texto: str):
    # Aqui você integraria com FCM/APNs/SMS/e-mail/WebSocket.
    print(f"[PUSH] -> user:{user_id} | msg: {texto}")

def main():
    consumer = get_consumer()
    print("[CONSUMER] Aguardando mensagens...")
    for msg in consumer:
        evento = msg.value
        k = msg.key
        pedido_id = evento.get("pedido_id")
        user_id = evento.get("user_id")
        status = evento.get("status")
        ts = evento.get("timestamp")

        # “Regra de negócio” simples de notificação
        texto = f"Pedido #{pedido_id}: {status} (às {ts})"
        push_fake(user_id, texto)

        # Log técnico
        print(f"[CONSUMER] partição={msg.partition} offset={msg.offset} key={k} value={evento}")

if __name__ == "__main__":
    main()
