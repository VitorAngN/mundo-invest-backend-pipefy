# Modelagem de dados

## Entidade Cliente

Representa o cliente cadastrado no sistema local.

| Campo | Tipo | Obrigatorio | Observacao |
|---|---|---|---|
| id | integer | sim | chave primaria |
| cliente_nome | string | sim | nome do cliente |
| cliente_email | string | sim | unico |
| tipo_solicitacao | string | sim | tipo informado no cadastro |
| valor_patrimonio | float | sim | usado para regra de prioridade |
| status | string | sim | `Aguardando Analise` ou `Processado` |
| prioridade | string/null | nao | definida no webhook |
| pipefy_card_id | string/null | nao | id simulado/local do card |
| created_at | datetime | sim | data de criacao |
| updated_at | datetime | sim | data de atualizacao |

Indices/constraints:

- `uq_clientes_cliente_email`: garante `cliente_email` unico.
- `ix_clientes_cliente_email`: acelera busca por email.

## Entidade WebhookEvent

Representa evento de webhook ja processado.

| Campo | Tipo | Obrigatorio | Observacao |
|---|---|---|---|
| id | integer | sim | chave primaria |
| event_id | string | sim | unico, usado para idempotencia |
| card_id | string | sim | card informado pelo webhook |
| cliente_email | string | sim | email recebido no webhook |
| event_timestamp | datetime | sim | timestamp enviado no payload |
| processed_at | datetime | sim | momento de processamento local |

Indices/constraints:

- `uq_webhook_events_event_id`: garante idempotencia por `event_id`.
- `ix_webhook_events_cliente_email`: acelera consultas por email.

## Transacao do webhook

O processamento do webhook deve ocorrer em uma unica transacao:

1. verificar se `event_id` ja existe;
2. buscar cliente;
3. calcular prioridade;
4. inserir `WebhookEvent`;
5. atualizar cliente;
6. confirmar transacao.

Inserir o evento antes de atualizar o cliente ajuda a proteger melhor contra corrida de eventos duplicados.

## Regra de prioridade

```text
valor_patrimonio >= 200000 -> prioridade_alta
valor_patrimonio < 200000  -> prioridade_normal
```

## Observacao financeira

Para o teste, `float` atende o requisito e simplifica validacao. Em producao financeira, seria melhor usar `Decimal` ou tipo monetario apropriado para evitar imprecisao de ponto flutuante.
