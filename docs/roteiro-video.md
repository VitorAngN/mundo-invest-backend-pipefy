# Roteiro do video de defesa

Tempo maximo: 7 minutos.

## 0:00 - 0:40 Background

Sou Vitor, venho estudando backend, APIs, banco de dados e cloud. Para este teste, implementei uma API em Python com FastAPI para cadastro de clientes, persistencia local, simulacao de integracao Pipefy via GraphQL e processamento idempotente de webhook.

## 0:40 - 1:30 Estrutura

Mostrar:

```text
app/routes
app/services
app/repositories
app/models.py
app/security.py
tests
docs
```

Fala:

Separei a aplicacao em camadas. As rotas cuidam de HTTP, os services concentram regras de negocio, os repositories isolam o banco e o PipefyService monta os payloads GraphQL.

Tambem deixei configuracao centralizada e autenticacao opcional por token como P1, sem atrapalhar o MVP.

## 1:30 - 2:30 Criacao de cliente

Mostrar:

- `app/schemas.py`
- `app/routes/clientes.py`
- `app/services/clientes_service.py`

Pontos:

- validacao com Pydantic;
- email validado com `EmailStr`;
- strings normalizadas;
- status inicial `Aguardando Analise`;
- persistencia local.

## 2:30 - 3:40 Ponto alto: Pipefy GraphQL

Mostrar:

- `app/services/pipefy_service.py`

Fala:

Na documentacao do Pipefy, localizei `createCard`, que recebe `CreateCardInput`, e `updateCardField`, que recebe `UpdateCardFieldInput`. Como o teste pede simulacao, eu nao chamo servidores reais, mas deixo a mutation e as variaveis no formato que seria enviado ao Pipefy.

Tambem criei testes especificos para garantir que as mutations e variaveis continuem no formato esperado.

## 3:40 - 4:50 Webhook e idempotencia

Mostrar:

- `app/services/webhooks_service.py`
- `app/models.py`

Pontos:

- busca por `event_id`;
- tabela `webhook_events`;
- constraint unica de `event_id`;
- prioridade por patrimonio;
- atualizacao para `Processado`.

## 4:50 - 5:50 Testes

Rodar:

```powershell
pytest -v
```

Mostrar testes:

- criacao de cliente;
- prioridade alta e normal;
- bloqueio de evento duplicado.
- PipefyService;
- seguranca opcional;
- constraints de banco.

## 5:50 - 6:40 Endpoints

Rodar:

```powershell
uvicorn app.main:app --reload
```

Depois os curls do README.

## 6:40 - 7:00 Producao AWS

Fechar:

Em producao eu levaria isso para API Gateway e Lambda, com RDS ou DynamoDB para persistencia. Para webhooks, usaria SQS entre recebimento e processamento, mantendo idempotencia pelo `event_id`, logs no CloudWatch e segredo do Pipefy no Secrets Manager.
