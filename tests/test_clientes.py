from app.constants import STATUS_AGUARDANDO_ANALISE
from app.models import Cliente


def test_cria_cliente_com_payload_valido_e_salva_no_banco(client, db_session):
    response = client.post(
        "/clientes",
        json={
            "cliente_nome": "João Silva",
            "cliente_email": "joao.silva@example.com",
            "tipo_solicitacao": "Atualização cadastral",
            "valor_patrimonio": 250000,
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["cliente_email"] == "joao.silva@example.com"
    assert body["status"] == STATUS_AGUARDANDO_ANALISE
    assert body["prioridade"] is None
    assert body["pipefy_payload"]["query"].startswith("mutation CreateClientCard")
    assert body["pipefy_payload"]["variables"]["input"]["fields_attributes"][0]["field_id"] == "cliente_nome"

    cliente = db_session.query(Cliente).filter_by(cliente_email="joao.silva@example.com").first()
    assert cliente is not None
    assert cliente.status == STATUS_AGUARDANDO_ANALISE


def test_criacao_cliente_rejeita_email_invalido(client):
    response = client.post(
        "/clientes",
        json={
            "cliente_nome": "João Silva",
            "cliente_email": "email-invalido",
            "tipo_solicitacao": "Atualização cadastral",
            "valor_patrimonio": 250000,
        },
    )

    assert response.status_code == 422


def test_criacao_cliente_rejeita_nome_vazio_apos_trim(client):
    response = client.post(
        "/clientes",
        json={
            "cliente_nome": "   ",
            "cliente_email": "joao.silva@example.com",
            "tipo_solicitacao": "Atualização cadastral",
            "valor_patrimonio": 250000,
        },
    )

    assert response.status_code == 422


def test_criacao_cliente_remove_espacos_das_strings(client):
    response = client.post(
        "/clientes",
        json={
            "cliente_nome": "  João Silva  ",
            "cliente_email": "joao.silva@example.com",
            "tipo_solicitacao": "  Atualização cadastral  ",
            "valor_patrimonio": 250000,
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["cliente_nome"] == "João Silva"
    assert body["tipo_solicitacao"] == "Atualização cadastral"


def test_criacao_cliente_rejeita_email_duplicado(client):
    payload = {
        "cliente_nome": "João Silva",
        "cliente_email": "joao.silva@example.com",
        "tipo_solicitacao": "Atualização cadastral",
        "valor_patrimonio": 250000,
    }

    first_response = client.post("/clientes", json=payload)
    second_response = client.post("/clientes", json=payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 409
    assert "Cliente" in second_response.json()["detail"]
