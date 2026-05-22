# Contratos de API

## Health check

```http
GET /health
```

Resposta:

```json
{
  "status": "ok"
}
```

## Criar cliente

```http
POST /clientes
Content-Type: application/json
```

Request:

```json
{
  "cliente_nome": "Joao Silva",
  "cliente_email": "joao.silva@example.com",
  "tipo_solicitacao": "Atualizacao cadastral",
  "valor_patrimonio": 250000
}
```

Validacoes:

- `cliente_nome`: obrigatorio, string nao vazia, com espacos laterais removidos.
- `cliente_email`: obrigatorio, formato de email.
- `tipo_solicitacao`: obrigatorio, string nao vazia, com espacos laterais removidos.
- `valor_patrimonio`: obrigatorio, numero maior ou igual a zero.

Resposta esperada:

```json
{
  "id": 1,
  "cliente_nome": "Joao Silva",
  "cliente_email": "joao.silva@example.com",
  "tipo_solicitacao": "Atualizacao cadastral",
  "valor_patrimonio": 250000,
  "status": "Aguardando Analise",
  "prioridade": null,
  "pipefy_card_id": "simulated_card_1",
  "pipefy_payload": {
    "query": "mutation CreateClientCard...",
    "variables": {}
  }
}
```

Status codes:

| Caso | Status |
|---|---|
| Criado | `201 Created` |
| Payload invalido | `422 Unprocessable Entity` |
| Email duplicado | `409 Conflict` |

## Webhook card updated

```http
POST /webhooks/pipefy/card-updated
Content-Type: application/json
```

Request:

```json
{
  "event_id": "evt_123",
  "card_id": "card_456",
  "cliente_email": "joao.silva@example.com",
  "timestamp": "2026-05-18T12:00:00Z"
}
```

Validacoes:

- `event_id`: obrigatorio, string nao vazia, com espacos laterais removidos.
- `card_id`: obrigatorio, string nao vazia, com espacos laterais removidos.
- `cliente_email`: obrigatorio, formato de email.
- `timestamp`: obrigatorio, datetime valido.

Resposta processada:

```json
{
  "processed": true,
  "duplicated": false,
  "event_id": "evt_123",
  "cliente_email": "joao.silva@example.com",
  "status": "Processado",
  "prioridade": "prioridade_alta",
  "pipefy_payload": {
    "query": "mutation UpdateClientCard...",
    "variables": {}
  }
}
```

Resposta duplicada:

```json
{
  "processed": false,
  "duplicated": true,
  "event_id": "evt_123",
  "cliente_email": "joao.silva@example.com",
  "status": null,
  "prioridade": null,
  "pipefy_payload": null
}
```

Status codes:

| Caso | Status |
|---|---|
| Processado | `200 OK` |
| Evento duplicado | `200 OK` |
| Cliente nao encontrado | `404 Not Found` |
| Payload invalido | `422 Unprocessable Entity` |
