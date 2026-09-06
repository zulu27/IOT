from app.ingestion import repository
from app.ingestion.repository import DuplicateInvoiceError
from app.messaging.rabbitmq import get_invoice
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




def main():
    while True:
        factura = get_invoice()

        if factura is not None:
            process_factura(factura)
        else:
            # No hay facturas en la cola.
            # Esperamos un poco antes de volver a preguntar.
            time.sleep(1)


if __name__ == "__main__":
    main()