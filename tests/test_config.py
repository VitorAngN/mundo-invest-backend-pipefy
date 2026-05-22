from app.config import Settings, get_settings


def test_settings_defaults():
    settings = Settings()

    assert settings.database_url == "sqlite:///./mundo_invest.db"
    assert settings.api_access_token is None
    assert settings.pipefy_pipe_id == "PIPE_ID_AQUI"
    assert settings.pipefy_field_cliente_nome == "cliente_nome"
    assert settings.pipefy_field_prioridade == "prioridade"


def test_settings_from_env(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite:///./custom.db")
    monkeypatch.setenv("API_ACCESS_TOKEN", "token_de_teste")
    monkeypatch.setenv("PIPEFY_PIPE_ID", "12345")
    monkeypatch.setenv("PIPEFY_FIELD_PRIORIDADE", "prioridade_custom")

    settings = Settings.from_env()

    assert settings.database_url == "sqlite:///./custom.db"
    assert settings.api_access_token == "token_de_teste"
    assert settings.pipefy_pipe_id == "12345"
    assert settings.pipefy_field_prioridade == "prioridade_custom"


def test_get_settings_usa_cache(monkeypatch):
    get_settings.cache_clear()
    monkeypatch.setenv("PIPEFY_PIPE_ID", "cached_pipe")

    first = get_settings()
    second = get_settings()

    assert first is second
    assert first.pipefy_pipe_id == "cached_pipe"

    get_settings.cache_clear()

