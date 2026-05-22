import pytest

from app.config import get_settings


@pytest.fixture()
def api_token(monkeypatch):
    monkeypatch.setenv("API_ACCESS_TOKEN", "token_de_teste")
    get_settings.cache_clear()
    yield "token_de_teste"
    get_settings.cache_clear()


def test_sem_api_access_token_endpoints_principais_continuam_livres(client):
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


def test_com_api_access_token_endpoint_rejeita_requisicao_sem_token(client, api_token):
    response = client.post(
        "/clientes",
        json={
            "cliente_nome": "João Silva",
            "cliente_email": "joao.silva@example.com",
            "tipo_solicitacao": "Atualização cadastral",
            "valor_patrimonio": 250000,
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Missing access token."


def test_com_api_access_token_endpoint_rejeita_token_invalido(client, api_token):
    response = client.post(
        "/clientes",
        headers={"Authorization": "Bearer token_errado"},
        json={
            "cliente_nome": "João Silva",
            "cliente_email": "joao.silva@example.com",
            "tipo_solicitacao": "Atualização cadastral",
            "valor_patrimonio": 250000,
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid access token."


def test_com_api_access_token_endpoint_aceita_token_valido(client, api_token):
    response = client.post(
        "/clientes",
        headers={"Authorization": f"Bearer {api_token}"},
        json={
            "cliente_nome": "João Silva",
            "cliente_email": "joao.silva@example.com",
            "tipo_solicitacao": "Atualização cadastral",
            "valor_patrimonio": 250000,
        },
    )

    assert response.status_code == 201


def test_health_check_continua_publico_mesmo_com_api_access_token(client, api_token):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

