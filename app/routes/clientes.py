from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.exceptions import ClienteAlreadyExistsError
from app.schemas import ClienteCreate, ClienteCreateResponse
from app.security import require_api_token
from app.services.clientes_service import ClientesService

router = APIRouter(prefix="/clientes", tags=["clientes"], dependencies=[Depends(require_api_token)])


@router.post("", response_model=ClienteCreateResponse, status_code=status.HTTP_201_CREATED)
def create_cliente(payload: ClienteCreate, db: Session = Depends(get_db)):
    service = ClientesService(db)

    try:
        cliente, pipefy_payload = service.create_cliente(payload)
    except ClienteAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc

    return ClienteCreateResponse.model_validate(
        {
            **cliente.__dict__,
            "pipefy_payload": pipefy_payload,
        }
    )
