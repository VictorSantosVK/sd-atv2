import os, asyncio, json
from typing import Dict, Set
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import aio_pika

RABBIT_URL = os.getenv("AMQP_URL", "amqp://guest:guest@localhost:5672/")
EXCHANGE = "order.status"
QUEUE = "order.status.notify"

app = FastAPI(title="Notifier")

# conexões WebSocket ativas: user_id -> set de websockets
clients: Dict[str, Set[WebSocket]] = {}

@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    user_id = ws.query_params.get("user_id") or "anon"
    await ws.accept()
    clients.setdefault(user_id, set()).add(ws)
    try:
        await ws.send_json({"info": f"conectado como {user_id}"})
        while True:
            await asyncio.sleep(3600)  # keepalive simples
    except WebSocketDisconnect:
        pass
    finally:
        s = clients.get(user_id, set())
        s.discard(ws)
        if not s:
            clients.pop(user_id, None)

async def amqp_consumer():
    connection = await aio_pika.connect_robust(RABBIT_URL)
    channel = await connection.channel()
    exch = await channel.declare_exchange(EXCHANGE, aio_pika.ExchangeType.TOPIC, durable=True)
    queue = await channel.declare_queue(QUEUE, durable=True)
    await queue.bind(exch, routing_key="#")  # recebe todos os status

    async with queue.iterator() as qit:
        async for message in qit:
            async with message.process():
                evt = json.loads(message.body.decode())
                user_id = evt.get("user_id", "")
                # envia a todos os sockets do mesmo usuário
                for ws in list(clients.get(user_id, [])):
                    try:
                        await ws.send_json(evt)
                    except Exception:
                        clients[user_id].discard(ws)

@app.on_event("startup")
async def on_start():
    asyncio.create_task(amqp_consumer())

@app.get("/health")
async def health():
    return {"status": "ok", "clients": {u: len(s) for u, s in clients.items()}}
