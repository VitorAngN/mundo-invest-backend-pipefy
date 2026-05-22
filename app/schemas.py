from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ClienteCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    cliente_nome: str = Field(min_length=1, max_length=255)
    cliente_email: EmailStr
    tipo_solicitacao: str = Field(min_length=1, max_length=255)
    valor_patrimonio: float = Field(ge=0)


class ClienteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cliente_nome: str
    cliente_email: EmailStr
    tipo_solicitacao: str
    valor_patrimonio: float
    status: str
    prioridade: str | None
    pipefy_card_id: str | None
    created_at: datetime
    updated_at: datetime


class ClienteCreateResponse(ClienteResponse):
    pipefy_payload: dict[str, Any]


class PipefyWebhookCardUpdated(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    event_id: str = Field(min_length=1, max_length=120)
    card_id: str = Field(min_length=1, max_length=120)
    cliente_email: EmailStr
    timestamp: datetime


class WebhookProcessResponse(BaseModel):
    processed: bool
    duplicated: bool
    event_id: str
    cliente_email: EmailStr | None = None
    status: str | None = None
    prioridade: str | None = None
    pipefy_payload: dict[str, Any] | None = None
