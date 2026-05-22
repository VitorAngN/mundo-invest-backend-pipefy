# Mapeamento Pipefy GraphQL

## Objetivo

Documentar como a aplicacao mapeia os fluxos locais para mutations GraphQL do Pipefy.

O teste tecnico nao exige chamada real para a API do Pipefy. Ele exige que o codigo deixe estruturadas as mutations no formato oficial.

## Referencias oficiais

- `createCard`: https://api-docs.pipefy.com/reference/mutations/createCard/
- `CreateCardInput`: https://api-docs.pipefy.com/reference/inputObjects/CreateCardInput
- `fields_attributes`: https://developers.pipefy.com/reference/create-a-card-with-the-required-fields-fulfilled
- `updateCardField`: https://api-docs.pipefy.com/reference/mutations/updateCardField/
- `UpdateCardFieldInput`: https://api-docs.pipefy.com/reference/inputObjects/UpdateCardFieldInput
- Guia de fields: https://developers.pipefy.com/reference/fields

## Criacao de card

Fluxo local:

```text
POST /clientes
  -> valida payload
  -> salva cliente
  -> monta payload createCard
```

Mutation:

```graphql
mutation CreateClientCard($input: CreateCardInput!) {
  createCard(input: $input) {
    card {
      id
    }
  }
}
```

Variaveis esperadas:

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

## Atualizacao de campos do card

Fluxo local:

```text
POST /webhooks/pipefy/card-updated
  -> verifica idempotencia por event_id
  -> busca cliente por email
  -> calcula prioridade
  -> monta payload updateCardField
  -> atualiza banco local
```

Mutation:

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

Variaveis esperadas:

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

## IDs de campos

Neste teste, os IDs de campos sao simulados por configuracao:

| Variavel | Valor local |
|---|---|
| `PIPEFY_FIELD_CLIENTE_NOME` | `cliente_nome` |
| `PIPEFY_FIELD_CLIENTE_EMAIL` | `cliente_email` |
| `PIPEFY_FIELD_TIPO_SOLICITACAO` | `tipo_solicitacao` |
| `PIPEFY_FIELD_VALOR_PATRIMONIO` | `valor_patrimonio` |
| `PIPEFY_FIELD_STATUS` | `status_cliente` |
| `PIPEFY_FIELD_PRIORIDADE` | `prioridade` |

Em producao, esses valores seriam os IDs reais dos campos configurados no Pipefy.

## Formatacao de valores

O Pipefy recebe os valores dos campos em `field_value`. Para evitar diferenca visual desnecessaria em valores inteiros, o patrimonio `250000` e enviado como string `"250000"` em vez de `"250000.0"`.

Se o valor possuir casas decimais, elas sao preservadas.

## Decisao de isolamento

As strings GraphQL devem ficar concentradas em uma camada de servico/client, por exemplo `PipefyService`.

Motivos:

- facilita teste unitario;
- evita mutation espalhada por rotas;
- facilita trocar simulacao por chamada HTTP real;
- deixa claro onde a documentacao oficial do Pipefy foi aplicada.

## Fora de escopo

- Autenticacao real no Pipefy.
- Token real de API.
- Retry real de chamada externa.
- Tratamento de erros reais da API Pipefy.

Esses pontos entram no roadmap de producao.
