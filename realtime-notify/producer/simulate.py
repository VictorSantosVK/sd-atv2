import os, asyncio, json, random
import aio_pika

RABBIT_URL = os.getenv("AMQP_URL", "amqp://guest:guest@localhost:5672/")
EXCHANGE = "order.status"
USERS = ["alice", "bob", "carol"]
STATUSES = ["PREPARADO", "ENVIADO", "ENTREGUE"]

async def main():
    conn = await aio_pika.connect_robust(RABBIT_URL)
    ch = await conn.channel()
    exch = await ch.declare_exchange(EXCHANGE, aio_pika.ExchangeType.TOPIC, durable=True)

    order_counter = 1
    while True:
        user = random.choice(USERS)
        order_id = f"ORD-{order_counter:04d}"
        for st in STATUSES:
            msg = {"user_id": user, "order_id": order_id, "status": st}
            rk = f"order.{user}.{order_id}.{st.lower()}"
            await exch.publish(
                aio_pika.Message(
                    body=json.dumps(msg).encode(),
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT
                ),
                routing_key=rk,
            )
            print("published:", msg)
            await asyncio.sleep(random.uniform(0.5, 1.5))
        order_counter += 1
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
