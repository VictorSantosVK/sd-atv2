import json
import time
from datetime import datetime, timezone
from kafka import KafkaProducer

BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC = "notificacoes"

# status em ordem (mantemos ordenação por chave -> mesma partição)
STATUS_PEDIDO = [
    "Preparado",
    "Saiu para entrega",
    "Entregue"
]

def utc_iso():
    return datetime.now(timezone.utc).isoformat()

def get_producer():
    return KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        acks="all",  # aguarda confirmação do broker
        retries=5,
        linger_ms=5,  # pode reduzir latência agregando pequenos batches
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        key_serializer=lambda v: str(v).encode("utf-8"),
    )

def enviar_eventos(pedido_id: int, user_id: int):
    producer = get_producer()
    try:
        for status in STATUS_PEDIDO:
            evento = {
                "pedido_id": pedido_id,
                "user_id": user_id,
                "status": status,
                "timestamp": utc_iso()
            }

            # chave = pedido_id garante ordem por partição
            future = producer.send(
                TOPIC,
                key=str(pedido_id),
                value=evento,
                headers=[("content-type", b"application/json")]
            )
            metadata = future.get(timeout=10)
            print(f"[PRODUCER] Enviado => {evento} | partição={metadata.partition} offset={metadata.offset}")
            time.sleep(2)  # simula tempo entre etapas
    finally:
        producer.flush()
        producer.close()

if __name__ == "__main__":
    enviar_eventos(pedido_id=123, user_id=987)
