from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.exceptions import ClienteNotFoundError
from app.schemas import PipefyWebhookCardUpdated, WebhookProcessResponse
from app.security import require_api_token
from app.services.webhooks_service import WebhooksService

router = APIRouter(prefix="/webhooks/pipefy", tags=["webhooks"], dependencies=[Depends(require_api_token)])


@router.post("/card-updated", response_model=WebhookProcessResponse)
def pipefy_card_updated(payload: PipefyWebhookCardUpdated, db: Session = Depends(get_db)):
    service = WebhooksService(db)

    try:
        return service.process_card_updated(payload)
    except ClienteNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
