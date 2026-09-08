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

