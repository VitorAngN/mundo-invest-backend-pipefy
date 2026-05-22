# Visao de producao na AWS

## Objetivo

Levar a API local para uma arquitetura escalavel, resiliente e simples de operar em AWS, mantendo o mesmo desenho de dominio usado no teste.

## Caminho serverless recomendado

```text
API Gateway
  -> Lambda de API
  -> RDS PostgreSQL ou DynamoDB

Pipefy Webhook
  -> API Gateway
  -> Lambda de recebimento
  -> SQS
  -> Lambda worker
  -> RDS PostgreSQL ou DynamoDB
  -> Pipefy GraphQL API
```

## Componentes

- API Gateway: expor os endpoints HTTP.
- Lambda: executar a logica de negocio com escala sob demanda.
- SQS: desacoplar recebimento de webhook do processamento.
- RDS PostgreSQL: melhor escolha quando houver consultas relacionais e transacoes.
- DynamoDB: boa escolha para idempotencia por `event_id` e acessos por chave.
- Secrets Manager: armazenar token real do Pipefy.
- CloudWatch: logs, metricas e alarmes.
- S3: armazenar payloads historicos, evidencias ou relatorios, se necessario.

## Idempotencia em producao

O `event_id` deve continuar sendo unico. Em DynamoDB, ele pode ser a partition key de uma tabela de eventos processados. Em RDS, deve ter unique constraint.

## Evolucao natural

1. Comecar com API Gateway + Lambda + RDS.
2. Inserir SQS no fluxo de webhook para absorver picos e retentativas.
3. Adicionar monitoramento com CloudWatch Alarms.
4. Adicionar CI/CD para testes e deploy.
5. Adicionar autenticaçao/assinatura de webhook caso o Pipefy envie segredo de validacao.

