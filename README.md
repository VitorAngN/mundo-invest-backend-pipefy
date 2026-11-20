# Client Management & Pipefy Integration

**[Página do projeto](https://vitorangn.github.io/mundo-invest-backend-pipefy/) · [Documentação da API](https://vitorangn.github.io/mundo-invest-backend-pipefy/api/)**

[![CI](https://github.com/VitorAngN/mundo-invest-backend-pipefy/actions/workflows/ci.yml/badge.svg)](https://github.com/VitorAngN/mundo-invest-backend-pipefy/actions/workflows/ci.yml)

API backend em Python para gerenciamento de clientes, persistencia local e simulacao de integracao com Pipefy via GraphQL.

Projeto desenvolvido para o teste tecnico de Desenvolvedor Backend do Mundo Invest.

## Tecnologias

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Pytest
- GraphQL

## Funcionalidades

- Cadastro de cliente em `POST /clientes`.
- Validacao de campos obrigatorios e e-mail.
- Persistencia local em SQLite.
- Status inicial `Aguardando Análise`.
- Simulacao de payload Pipefy com mutation `createCard`.
- Processamento de webhook em `POST /webhooks/pipefy/card-updated`.
- Idempotencia por `event_id`.
- Regra de prioridade por patrimonio:
  - `valor_patrimonio >= 200000`: `prioridade_alta`
  - `valor_patrimonio < 200000`: `prioridade_normal`
- Atualizacao local do cliente para `Processado`.
- Simulacao de payload Pipefy com mutation `updateCardField`.
- Autenticacao opcional por token via `API_ACCESS_TOKEN`.
- Testes automatizados.

## Estrutura

```text
app/
  routes/          # endpoints HTTP
  services/        # regras de negocio e integracao Pipefy simulada
  repositories/    # acesso ao banco
  models.py        # modelos SQLAlchemy
  schemas.py       # schemas Pydantic
tests/             # testes automatizados
```

## Como rodar localmente

Use Python 3.11 ou 3.12.

No Windows:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Documentacao automatica:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
http://127.0.0.1:8000/health
```

## Como rodar com Docker

```bash
docker build -t mundo-invest-api .
docker run -p 8000:8000 mundo-invest-api
```

## Como rodar os testes

```powershell
pytest -v
```

## Autenticacao opcional

Por padrao, a API roda sem exigir token para facilitar a avaliacao local.

Se `API_ACCESS_TOKEN` for configurado, os endpoints principais passam a exigir:

```http
Authorization: Bearer <token>
```

Exemplo:

```powershell
$env:API_ACCESS_TOKEN="token_de_teste"
uvicorn app.main:app --reload
```

## Endpoint: criar cliente

```http
POST /clientes
```

Exemplo:

```powershell
curl.exe -X POST "http://127.0.0.1:8000/clientes" `
  -H "Content-Type: application/json" `
  -d "{\"cliente_nome\":\"Joao Silva\",\"cliente_email\":\"joao.silva@example.com\",\"tipo_solicitacao\":\"Atualizacao cadastral\",\"valor_patrimonio\":250000}"
```

Com token opcional ativado:

```powershell
curl.exe -X POST "http://127.0.0.1:8000/clientes" `
  -H "Content-Type: application/json" `
  -H "Authorization: Bearer token_de_teste" `
  -d "{\"cliente_nome\":\"Joao Silva\",\"cliente_email\":\"joao.silva@example.com\",\"tipo_solicitacao\":\"Atualizacao cadastral\",\"valor_patrimonio\":250000}"
```

## Endpoint: webhook Pipefy card updated

```http
POST /webhooks/pipefy/card-updated
```

Exemplo:

```powershell
curl.exe -X POST "http://127.0.0.1:8000/webhooks/pipefy/card-updated" `
  -H "Content-Type: application/json" `
  -d "{\"event_id\":\"evt_123\",\"card_id\":\"card_456\",\"cliente_email\":\"joao.silva@example.com\",\"timestamp\":\"2026-05-18T12:00:00Z\"}"
```

Com token opcional ativado, adicione:

```powershell
-H "Authorization: Bearer token_de_teste"
```

## Pipefy GraphQL

As mutations ficam em `app/services/pipefy_service.py`.

### createCard

```graphql
mutation CreateClientCard($input: CreateCardInput!) {
  createCard(input: $input) {
    card {
      id
    }
  }
}
```

Variaveis simuladas:

```json
{
  "input": {
    "pipe_id": "PIPE_ID_AQUI",
    "title": "Joao Silva",
    "fields_attributes": [
      {
        "field_id": "cliente_nome",
        "field_value": "Joao Silva"
      },
      {
        "field_id": "cliente_email",
        "field_value": "joao.silva@example.com"
      },
      {
        "field_id": "tipo_solicitacao",
        "field_value": "Atualizacao cadastral"
      },
      {
        "field_id": "valor_patrimonio",
        "field_value": "250000"
      }
    ]
  }
}
```

### updateCardField

```graphql
mutation UpdateClientCard($statusInput: UpdateCardFieldInput!, $priorityInput: UpdateCardFieldInput!) {
  status: updateCardField(input: $statusInput) {
    success
  }
  priority: updateCardField(input: $priorityInput) {
    success
  }
}
```

Variaveis simuladas:

```json
{
  "statusInput": {
    "card_id": "card_456",
    "field_id": "status_cliente",
    "new_value": "Processado"
  },
  "priorityInput": {
    "card_id": "card_456",
    "field_id": "prioridade",
    "new_value": "prioridade_alta"
  }
}
```

Referencias oficiais:

- https://api-docs.pipefy.com/reference/mutations/createCard/
- https://api-docs.pipefy.com/reference/inputObjects/CreateCardInput
- https://developers.pipefy.com/reference/create-a-card-with-the-required-fields-fulfilled
- https://api-docs.pipefy.com/reference/mutations/updateCardField/
- https://api-docs.pipefy.com/reference/inputObjects/UpdateCardFieldInput
- https://developers.pipefy.com/reference/fields

## Visao de producao na AWS

Em producao, a API poderia ser exposta pelo API Gateway e executada em Lambda. A persistencia poderia usar RDS PostgreSQL quando houver necessidade de relacionamento, transacoes e consultas SQL, ou DynamoDB para acessos por chave, como `cliente_email` e `event_id`.

Para webhooks, uma arquitetura mais resiliente usaria API Gateway recebendo o evento, Lambda para validacao inicial, SQS para desacoplar o processamento e um worker Lambda para aplicar a regra de negocio e chamar a API real do Pipefy. Logs e metricas ficariam no CloudWatch, e tokens reais do Pipefy ficariam no Secrets Manager.

