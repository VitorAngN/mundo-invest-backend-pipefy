# Requisitos e escopo

## Escopo funcional

### RF01 - Criar cliente

Como sistema interno, quero receber dados de um cliente para registrar a solicitacao e iniciar o fluxo operacional.

Endpoint:

```http
POST /clientes
```

Payload esperado:

```json
{
  "cliente_nome": "Joao Silva",
  "cliente_email": "joao.silva@example.com",
  "tipo_solicitacao": "Atualizacao cadastral",
  "valor_patrimonio": 250000
}
```

Criterios de aceite:

- Deve validar campos obrigatorios.
- Deve validar formato de e-mail.
- Deve salvar o cliente no banco local.
- Deve iniciar com status `Aguardando Analise`.
- Deve montar payload GraphQL `createCard` conforme documentacao oficial do Pipefy.
- Nao deve chamar servidores reais do Pipefy.

### RF02 - Receber webhook de card atualizado

Como sistema interno, quero receber um evento do Pipefy para processar a atualizacao do cliente.

Endpoint:

```http
POST /webhooks/pipefy/card-updated
```

Payload esperado:

```json
{
  "event_id": "evt_123",
  "card_id": "card_456",
  "cliente_email": "joao.silva@example.com",
  "timestamp": "2026-05-18T12:00:00Z"
}
```

Criterios de aceite:

- Deve verificar se `event_id` ja foi processado.
- Se o evento for duplicado, nao deve processar novamente.
- Deve buscar cliente por `cliente_email`.
- Se `valor_patrimonio >= 200000`, prioridade deve ser `prioridade_alta`.
- Se `valor_patrimonio < 200000`, prioridade deve ser `prioridade_normal`.
- Deve montar payload GraphQL `updateCardField` conforme documentacao oficial do Pipefy.
- Deve atualizar status local para `Processado`.
- Deve salvar a prioridade no banco local.

## Escopo de testes

Obrigatorios:

- Criacao de cliente com payload valido e salvamento no banco.
- Processamento do webhook aplicando regra de prioridade.
- Bloqueio de processamento com `event_id` duplicado.

Recomendados:

- Payload com email invalido.
- Webhook para cliente inexistente.
- Patrimonio exatamente igual a `200000`.
- Cliente com e-mail duplicado.

## Fora de escopo nesta versao

- Autenticacao obrigatoria.
- Autorizacao por perfil.
- Chamada real para Pipefy.
- Deploy real na AWS.
- Interface frontend.
- n8n real.
- Docker obrigatorio.
- Observabilidade completa.

## Evolucao de seguranca

Autenticacao por token e uma evolucao desejavel, mas nao obrigatoria no MVP do teste.

Opcao planejada:

- `Authorization: Bearer <token>` para endpoints internos;
- token configurado por variavel de ambiente;
- `GET /health` publico;
- webhook protegido por token ou assinatura quando houver suporte do provedor.

Detalhes em [13-seguranca-autenticacao.md](13-seguranca-autenticacao.md).

## Requisitos nao funcionais

- Codigo organizado em camadas.
- README com instrucoes de execucao.
- Documentacao das decisoes tecnicas.
- Testes automatizados executaveis localmente.
- Simplicidade para avaliacao do teste.
- Caminho claro para evolucao em producao.
