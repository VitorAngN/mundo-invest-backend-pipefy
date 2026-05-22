from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.constants import (
    PATRIMONIO_PRIORIDADE_ALTA,
    PRIORIDADE_ALTA,
    PRIORIDADE_NORMAL,
    STATUS_PROCESSADO,
)
from app.exceptions import ClienteNotFoundError
from app.models import WebhookEvent
from app.repositories.clientes_repository import ClientesRepository
from app.repositories.webhook_events_repository import WebhookEventsRepository
from app.schemas import PipefyWebhookCardUpdated
from app.services.pipefy_service import PipefyService


def calcular_prioridade(valor_patrimonio: float) -> str:
    if valor_patrimonio >= PATRIMONIO_PRIORIDADE_ALTA:
        return PRIORIDADE_ALTA
    return PRIORIDADE_NORMAL


class WebhooksService:
    def __init__(self, db: Session, pipefy_service: PipefyService | None = None):
        self.db = db
        self.clientes_repository = ClientesRepository(db)
        self.events_repository = WebhookEventsRepository(db)
        self.pipefy_service = pipefy_service or PipefyService()

    @staticmethod
    def _duplicated_response(payload: PipefyWebhookCardUpdated) -> dict:
        return {
            "processed": False,
            "duplicated": True,
            "event_id": payload.event_id,
            "cliente_email": str(payload.cliente_email),
        }

    def process_card_updated(self, payload: PipefyWebhookCardUpdated) -> dict:
        if self.events_repository.exists(payload.event_id):
            return self._duplicated_response(payload)

        cliente = self.clientes_repository.get_by_email(str(payload.cliente_email))
        if cliente is None:
            raise ClienteNotFoundError("Cliente não encontrado para o e-mail informado.")

        prioridade = calcular_prioridade(cliente.valor_patrimonio)
        pipefy_payload = self.pipefy_service.build_update_card_fields_payload(
            card_id=payload.card_id,
            prioridade=prioridade,
        )

        event = WebhookEvent(
            event_id=payload.event_id,
            card_id=payload.card_id,
            cliente_email=str(payload.cliente_email),
            event_timestamp=payload.timestamp,
        )

        try:
            self.events_repository.add(event)
            self.clientes_repository.mark_processed(cliente, payload.card_id, prioridade)
            self.db.commit()
            self.db.refresh(cliente)
        except IntegrityError:
            self.db.rollback()
            return self._duplicated_response(payload)

        return {
            "processed": True,
            "duplicated": False,
            "event_id": payload.event_id,
            "cliente_email": cliente.cliente_email,
            "status": STATUS_PROCESSADO,
            "prioridade": prioridade,
            "pipefy_payload": pipefy_payload,
        }
