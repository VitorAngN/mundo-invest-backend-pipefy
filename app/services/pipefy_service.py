from typing import Any

from app.config import Settings, get_settings
from app.constants import STATUS_PROCESSADO
from app.schemas import ClienteCreate


class PipefyService:
    """Builds Pipefy GraphQL payloads without calling the real Pipefy API."""

    CREATE_CARD_MUTATION = """
mutation CreateClientCard($input: CreateCardInput!) {
  createCard(input: $input) {
    card {
      id
    }
  }
}
""".strip()

    UPDATE_CARD_FIELDS_MUTATION = """
mutation UpdateClientCard($statusInput: UpdateCardFieldInput!, $priorityInput: UpdateCardFieldInput!) {
  status: updateCardField(input: $statusInput) {
    success
  }
  priority: updateCardField(input: $priorityInput) {
    success
  }
}
""".strip()

    def __init__(self, settings: Settings | None = None):
        self.settings = settings or get_settings()

    @staticmethod
    def _format_field_value(value: str | float) -> str:
        if isinstance(value, float) and value.is_integer():
            return str(int(value))
        return str(value)

    def build_create_card_payload(self, payload: ClienteCreate) -> dict[str, Any]:
        return {
            "query": self.CREATE_CARD_MUTATION,
            "variables": {
                "input": {
                    "pipe_id": self.settings.pipefy_pipe_id,
                    "title": payload.cliente_nome,
                    "fields_attributes": [
                        {
                            "field_id": self.settings.pipefy_field_cliente_nome,
                            "field_value": payload.cliente_nome,
                        },
                        {
                            "field_id": self.settings.pipefy_field_cliente_email,
                            "field_value": str(payload.cliente_email),
                        },
                        {
                            "field_id": self.settings.pipefy_field_tipo_solicitacao,
                            "field_value": payload.tipo_solicitacao,
                        },
                        {
                            "field_id": self.settings.pipefy_field_valor_patrimonio,
                            "field_value": self._format_field_value(payload.valor_patrimonio),
                        },
                    ],
                }
            },
        }

    def build_update_card_fields_payload(self, card_id: str, prioridade: str) -> dict[str, Any]:
        return {
            "query": self.UPDATE_CARD_FIELDS_MUTATION,
            "variables": {
                "statusInput": {
                    "card_id": card_id,
                    "field_id": self.settings.pipefy_field_status,
                    "new_value": STATUS_PROCESSADO,
                },
                "priorityInput": {
                    "card_id": card_id,
                    "field_id": self.settings.pipefy_field_prioridade,
                    "new_value": prioridade,
                },
            },
        }
