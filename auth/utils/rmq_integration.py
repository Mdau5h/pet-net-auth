import aio_pika
import uuid
from auth.serializers.common import EventMessage
from config import config


def catch_event(event_type: str):
    def catch_particular_event(func):
        async def wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)
            await publish_message(result, event_type=event_type)
            return result
        return wrapper
    return catch_particular_event


async def publish_message(result: dict, event_type: str):
    message = EventMessage(
        msg_id=str(uuid.uuid4()),
        msg_type=event_type,
        msg_data=result
    )
    connection = await aio_pika.connect_robust(config.rabbitmq_url, heartbeat=360)
    queue_name = 'test_queue'
    async with connection:
        channel = await connection.channel()
        await channel.declare_queue(
            queue_name,
            auto_delete=False,
        )
        await channel.default_exchange.publish(
            aio_pika.Message(body=message.json().encode()),
            routing_key=queue_name,
        )
