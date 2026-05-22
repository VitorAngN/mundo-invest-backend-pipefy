# Plano de testes

## Objetivo

Garantir que os fluxos obrigatorios do teste tecnico funcionem e possam ser demonstrados no video.

## Estrategia

Usar testes automatizados com `pytest` e `TestClient` do FastAPI, executando contra banco SQLite isolado para testes.

## Casos obrigatorios

### CT01 - Criacao de cliente com payload valido

Pre-condicao:

- API disponivel em ambiente de teste.

Passos:

1. Enviar `POST /clientes` com payload valido.
2. Verificar status HTTP.
3. Consultar banco local.

Resultado esperado:

- HTTP `201 Created`.
- Cliente salvo.
- Status `Aguardando Analise`.
- Prioridade `null`.
- Payload GraphQL `createCard` presente.

### CT02 - Webhook aplica prioridade correta

Pre-condicao:

- Cliente salvo no banco.

Passos:

1. Criar cliente com `valor_patrimonio` maior ou igual a `200000`.
2. Enviar webhook.
3. Verificar resposta e banco.

Resultado esperado:

- HTTP `200 OK`.
- Status `Processado`.
- Prioridade `prioridade_alta`.
- Payload GraphQL `updateCardField` presente.

Variacao:

- Cliente com patrimonio menor que `200000` deve receber `prioridade_normal`.

### CT03 - Webhook duplicado nao reprocessa

Pre-condicao:

- Cliente salvo no banco.
- Um webhook ja processado com `event_id` especifico.

Passos:

1. Enviar webhook com `event_id`.
2. Enviar o mesmo webhook novamente.

Resultado esperado:

- Segunda resposta com `processed: false`.
- Segunda resposta com `duplicated: true`.
- Apenas um registro em `webhook_events` para aquele `event_id`.

## Casos recomendados

| Caso | Resultado esperado |
|---|---|
| Email invalido em `/clientes` | `422` |
| Nome vazio ou apenas com espacos | `422` |
| Strings com espacos laterais | Valores normalizados |
| Cliente inexistente no webhook | `404` |
| `event_id` vazio ou apenas com espacos | `422` |
| Patrimonio exatamente `200000` | `prioridade_alta` |
| Cliente duplicado por email | `409` |
| Payload `createCard` do Pipefy | Mutation `createCard` e `CreateCardInput` presentes |
| Payload `updateCardField` do Pipefy | Mutation `updateCardField` e `UpdateCardFieldInput` presentes |
| Patrimonio inteiro no payload Pipefy | Valor formatado como `"250000"` |
| Patrimonio decimal no payload Pipefy | Valor decimal preservado |
| Constraint unica de email | Banco rejeita cliente duplicado |
| Constraint unica de event_id | Banco rejeita evento duplicado |

## Comando de teste

```powershell
pytest -v
```
