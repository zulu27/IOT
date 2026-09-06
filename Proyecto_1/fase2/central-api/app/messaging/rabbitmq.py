import json
import os
import pika

RABBITMQ_URL = os.getenv(
    "RABBITMQ_URL",
    "amqp://user:password@rabbitmq:5672/",
)

QUEUE_NAME = "invoices"


def get_connection():
    """Create a connection with RabbitMQ."""
    return pika.BlockingConnection(
        pika.URLParameters(RABBITMQ_URL)
    )

def publish_to_queue(message: dict):
    """Add one invoice to the RabbitMQ queue."""

    connection = get_connection()
    channel = connection.channel()

    # Make sure the queue exists
    channel.queue_declare(
        queue=QUEUE_NAME,
        durable=True,
    )

    channel.basic_publish(
        exchange="",
        routing_key=QUEUE_NAME,
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=pika.DeliveryMode.Persistent,
        ),
    )

    connection.close()


def get_invoice():
    """Remove one invoice from the queue."""

    connection = get_connection()
    channel = connection.channel()

    channel.queue_declare(
        queue=QUEUE_NAME,
        durable=True,
    )

    method, properties, body = channel.basic_get(
        queue=QUEUE_NAME,
        auto_ack=False,
    )

    if method is None:
        connection.close()
        return None

    message = json.loads(body)

    channel.basic_ack(
        delivery_tag=method.delivery_tag
    )

    connection.close()

    return message