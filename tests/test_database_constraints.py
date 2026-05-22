from datetime import UTC, datetime

import pytest
from sqlalchemy.exc import IntegrityError

from app.constants import STATUS_AGUARDANDO_ANALISE
from app.models import Cliente, WebhookEvent

EVENT_TIMESTAMP = datetime(2026, 5, 18, 12, 0, tzinfo=UTC)


def test_cliente_email_tem_constraint_unica(db_session):
    primeiro = Cliente(
        cliente_nome="João Silva",
        cliente_email="joao.silva@example.com",
        tipo_solicitacao="Atualização cadastral",
        valor_patrimonio=250000,
        status=STATUS_AGUARDANDO_ANALISE,
    )
    duplicado = Cliente(
        cliente_nome="Outro João",
        cliente_email="joao.silva@example.com",
        tipo_solicitacao="Nova solicitação",
        valor_patrimonio=100000,
        status=STATUS_AGUARDANDO_ANALISE,
    )

    db_session.add(primeiro)
    db_session.commit()

    db_session.add(duplicado)
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_webhook_event_id_tem_constraint_unica(db_session):
    primeiro = WebhookEvent(
        event_id="evt_123",
        card_id="card_456",
        cliente_email="joao.silva@example.com",
        event_timestamp=EVENT_TIMESTAMP,
    )
    duplicado = WebhookEvent(
        event_id="evt_123",
        card_id="card_789",
        cliente_email="maria@example.com",
        event_timestamp=EVENT_TIMESTAMP,
    )

    db_session.add(primeiro)
    db_session.commit()

    db_session.add(duplicado)
    with pytest.raises(IntegrityError):
        db_session.commit()
