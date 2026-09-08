"""HTTP surface for batch ingestion.

This layer only translates between HTTP and the service layer: it parses the
request, calls a service, and maps domain exceptions onto status codes. It
builds no queries.
"""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.ingestion import service
from app.ingestion.schemas import BatchRequest, QueueResponse
from app.stores.service import UnknownStoreError
from app.messaging.rabbitmq import publish_to_queue


router = APIRouter(prefix="/sales", tags=["ingestion"])



@router.post("/batch", response_model=QueueResponse)
def ingest_batch(
    batch: BatchRequest,
    session: Session = Depends(get_session),
    
) -> QueueResponse:
    try:
        #ya service no consume y guarda los datos en la base de datos, ahora solo confirma
        #que los datos sean validos
        service.validate_batch(session,batch)
        #Publicamos cada factura en RabbitMQ para que el microservicio de facturas las consuma y las guarde en la base de datos
        
        for invoice in batch.invoices:
            message = {
                #guardamos de que store es el batch
                "store_id": batch.store_id,
                "invoice": invoice.model_dump(mode="json")
            }
            publish_to_queue(message)

    except UnknownStoreError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)
        ) from error
    except service.InvalidBatchError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)
        ) from error

    #Ahora simplemente confiramos que los datos son validos y devolvemos un mensaje de que se han encoladon
    return QueueResponse(
        store_id=batch.store_id,
        queued=True,
    )
    