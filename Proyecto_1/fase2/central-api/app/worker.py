import json

from app.ingestion import repository
from app.ingestion.repository import DuplicateInvoiceError
from app.messaging.rabbitmq import get_connection, QUEUE_NAME
from datetime import datetime
from app.core.database import SessionLocal
from app.ingestion.schemas import InvoiceRequest
import time

def process_factura(factura,received_at: datetime | None = None,):
    print("Factura recibida:")
    res = False
    stamp = received_at or datetime.now()
    session = SessionLocal()
    invoice = InvoiceRequest.model_validate(factura["invoice"])
    try:
        repository.insert_invoice(
                session=session,
                store_id=str(factura["store_id"]),
                invoice = invoice,
                received_at=stamp,
                )
        print("Factura procesada y guardada en la base de datos.")
    except DuplicateInvoiceError:
        res = False
    else:
        res = True

    if res:
        session.commit()




def callback(ch, method, properties, body):
    """
    Se ejecuta automáticamente cuando RabbitMQ
    entrega un mensaje al worker.
    """

    print("Mensaje recibido desde RabbitMQ.")

    factura = json.loads(body)

    process_factura(factura)

    # Le avisamos a RabbitMQ que terminamos de procesar
    # el mensaje.
    ch.basic_ack(
        delivery_tag=method.delivery_tag
    )


def main():
    connection = get_connection()
    channel = connection.channel()

    # Aseguramos que la cola exista
    channel.queue_declare(
        queue=QUEUE_NAME,
        durable=True,
    )

    # Le decimos a RabbitMQ:
    # "Cuando llegue un mensaje, ejecuta callback"
    channel.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=callback,
        auto_ack=False,
    )

    print("Worker esperando mensajes...")

    # El worker queda esperando.
    # RabbitMQ llamará a callback() cuando llegue algo.
    channel.start_consuming()


if __name__ == "__main__":
    main()