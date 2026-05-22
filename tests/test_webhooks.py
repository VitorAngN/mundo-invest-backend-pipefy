from app.constants import PRIORIDADE_ALTA, PRIORIDADE_NORMAL, STATUS_PROCESSADO
from app.models import Cliente, WebhookEvent


def criar_cliente(client, email="joao.silva@example.com", valor_patrimonio=250000):
    return client.post(
        "/clientes",
        json={
            "cliente_nome": "João Silva",
            "cliente_email": email,
            "tipo_solicitacao": "Atualização cadastral",
            "valor_patrimonio": valor_patrimonio,
        },
    )


def test_webhook_processa_prioridade_alta_com_base_no_patrimonio(client, db_session):
    criar_cliente(client, valor_patrimonio=250000)

    response = client.post(
        "/webhooks/pipefy/card-updated",
        json={
            "event_id": "evt_123",
            "card_id": "card_456",
            "cliente_email": "joao.silva@example.com",
            "timestamp": "2026-05-18T12:00:00Z",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["processed"] is True
    assert body["duplicated"] is False
    assert body["status"] == STATUS_PROCESSADO
    assert body["prioridade"] == PRIORIDADE_ALTA
    assert body["pipefy_payload"]["query"].startswith("mutation UpdateClientCard")

    cliente = db_session.query(Cliente).filter_by(cliente_email="joao.silva@example.com").first()
    assert cliente.status == STATUS_PROCESSADO
    assert cliente.prioridade == PRIORIDADE_ALTA


def test_webhook_processa_prioridade_alta_no_limite_do_patrimonio(client, db_session):
    criar_cliente(client, email="limite@example.com", valor_patrimonio=200000)

    response = client.post(
        "/webhooks/pipefy/card-updated",
        json={
            "event_id": "evt_limite",
            "card_id": "card_limite",
            "cliente_email": "limite@example.com",
            "timestamp": "2026-05-18T12:00:00Z",
        },
    )

    assert response.status_code == 200
    assert response.json()["prioridade"] == PRIORIDADE_ALTA

    cliente = db_session.query(Cliente).filter_by(cliente_email="limite@example.com").first()
    assert cliente.prioridade == PRIORIDADE_ALTA


def test_webhook_processa_prioridade_normal_com_base_no_patrimonio(client, db_session):
    criar_cliente(client, email="maria@example.com", valor_patrimonio=150000)

    response = client.post(
        "/webhooks/pipefy/card-updated",
        json={
            "event_id": "evt_456",
            "card_id": "card_789",
            "cliente_email": "maria@example.com",
            "timestamp": "2026-05-18T12:00:00Z",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["prioridade"] == PRIORIDADE_NORMAL

    cliente = db_session.query(Cliente).filter_by(cliente_email="maria@example.com").first()
    assert cliente.status == STATUS_PROCESSADO
    assert cliente.prioridade == PRIORIDADE_NORMAL


def test_webhook_bloqueia_processamento_com_event_id_duplicado(client, db_session):
    criar_cliente(client)
    payload = {
        "event_id": "evt_duplicado",
        "card_id": "card_456",
        "cliente_email": "joao.silva@example.com",
        "timestamp": "2026-05-18T12:00:00Z",
    }

    first_response = client.post("/webhooks/pipefy/card-updated", json=payload)
    second_response = client.post("/webhooks/pipefy/card-updated", json=payload)

    assert first_response.status_code == 200
    assert second_response.status_code == 200
    assert second_response.json()["processed"] is False
    assert second_response.json()["duplicated"] is True

    events_count = db_session.query(WebhookEvent).filter_by(event_id="evt_duplicado").count()
    assert events_count == 1


def test_webhook_retorna_404_quando_cliente_nao_existe(client):
    response = client.post(
        "/webhooks/pipefy/card-updated",
        json={
            "event_id": "evt_sem_cliente",
            "card_id": "card_999",
            "cliente_email": "nao.existe@example.com",
            "timestamp": "2026-05-18T12:00:00Z",
        },
    )

    assert response.status_code == 404


def test_webhook_rejeita_event_id_vazio_apos_trim(client):
    response = client.post(
        "/webhooks/pipefy/card-updated",
        json={
            "event_id": "   ",
            "card_id": "card_999",
            "cliente_email": "nao.existe@example.com",
            "timestamp": "2026-05-18T12:00:00Z",
        },
    )

    assert response.status_code == 422
