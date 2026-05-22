# Arquitetura planejada

## Decisao de stack

Linguagem escolhida: Python.

Framework escolhido: FastAPI.

Banco local: SQLite.

Motivos:

- FastAPI entrega validacao e documentacao automatica rapidamente.
- Pydantic ajuda a validar payloads.
- SQLite reduz dependencias locais para o teste.
- SQLAlchemy facilita evolucao para PostgreSQL/RDS.
- Pytest cobre os fluxos obrigatorios.

## Camadas

```text
HTTP request
  -> routes
  -> services
  -> repositories
  -> database

services
  -> PipefyService
```

## Responsabilidades

### routes

- Receber requests.
- Acionar Pydantic.
- Traduzir exceptions em status HTTP.
- Nao conter regra de negocio pesada.

### services

- Executar regras de negocio.
- Calcular prioridade.
- Controlar idempotencia.
- Coordenar repositorios.
- Montar respostas de caso de uso.

### repositories

- Isolar queries e persistencia.
- Buscar cliente por email.
- Salvar cliente.
- Salvar evento processado.

### PipefyService

- Isolar mutations GraphQL.
- Montar payloads `createCard`.
- Montar payloads `updateCardField`.
- Simular integracao sem chamada externa.

## Fluxo POST /clientes

```text
Cliente HTTP
  -> POST /clientes
  -> ClienteCreate schema
  -> ClientesService
  -> ClientesRepository
  -> SQLite
  -> PipefyService.build_create_card_payload
  -> resposta JSON
```

## Fluxo POST /webhooks/pipefy/card-updated

```text
Pipefy simulado
  -> POST /webhooks/pipefy/card-updated
  -> PipefyWebhookCardUpdated schema
  -> WebhooksService
  -> WebhookEventsRepository.exists(event_id)
  -> ClientesRepository.get_by_email(cliente_email)
  -> calcular prioridade
  -> PipefyService.build_update_card_fields_payload
  -> atualizar Cliente
  -> salvar WebhookEvent
  -> resposta JSON
```

## Decisoes tecnicas

### SQLite no teste

Escolhido pela simplicidade local. Para producao, trocar por RDS PostgreSQL ou DynamoDB conforme padrao de acesso.

### Idempotencia com tabela separada

`webhook_events` evita que o mesmo `event_id` seja processado duas vezes.

No fluxo transacional, o evento e registrado antes da atualizacao do cliente. Se a constraint unica de `event_id` falhar, a transacao e revertida e a resposta indica duplicidade.

### Retorno 200 para evento duplicado

Em webhooks reais, retornar erro em evento ja processado pode induzir retry infinito. Por isso, a resposta recomendada e:

```json
{
  "processed": false,
  "duplicated": true
}
```

### Mutations Pipefy em service isolado

Facilita demonstrar ao avaliador onde a sintaxe oficial do Pipefy foi mapeada e permite trocar simulacao por chamada HTTP real depois.
