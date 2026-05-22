from dataclasses import dataclass
from functools import lru_cache
from os import getenv


@dataclass(frozen=True)
class Settings:
    database_url: str = "sqlite:///./mundo_invest.db"
    api_access_token: str | None = None

    pipefy_pipe_id: str = "PIPE_ID_AQUI"
    pipefy_field_cliente_nome: str = "cliente_nome"
    pipefy_field_cliente_email: str = "cliente_email"
    pipefy_field_tipo_solicitacao: str = "tipo_solicitacao"
    pipefy_field_valor_patrimonio: str = "valor_patrimonio"
    pipefy_field_status: str = "status_cliente"
    pipefy_field_prioridade: str = "prioridade"

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            database_url=getenv("DATABASE_URL", cls.database_url),
            api_access_token=getenv("API_ACCESS_TOKEN") or None,
            pipefy_pipe_id=getenv("PIPEFY_PIPE_ID", cls.pipefy_pipe_id),
            pipefy_field_cliente_nome=getenv(
                "PIPEFY_FIELD_CLIENTE_NOME",
                cls.pipefy_field_cliente_nome,
            ),
            pipefy_field_cliente_email=getenv(
                "PIPEFY_FIELD_CLIENTE_EMAIL",
                cls.pipefy_field_cliente_email,
            ),
            pipefy_field_tipo_solicitacao=getenv(
                "PIPEFY_FIELD_TIPO_SOLICITACAO",
                cls.pipefy_field_tipo_solicitacao,
            ),
            pipefy_field_valor_patrimonio=getenv(
                "PIPEFY_FIELD_VALOR_PATRIMONIO",
                cls.pipefy_field_valor_patrimonio,
            ),
            pipefy_field_status=getenv("PIPEFY_FIELD_STATUS", cls.pipefy_field_status),
            pipefy_field_prioridade=getenv(
                "PIPEFY_FIELD_PRIORIDADE",
                cls.pipefy_field_prioridade,
            ),
        )


@lru_cache
def get_settings() -> Settings:
    return Settings.from_env()

