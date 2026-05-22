# Roadmap de escalabilidade

## Objetivo

Mostrar como a solucao pode evoluir de um teste local para uma base mais proxima de producao.

## Fase 1 - Teste tecnico local

Caracteristicas:

- FastAPI local.
- SQLite.
- Pipefy simulado.
- Testes automatizados.
- README e documentacao.

Foco:

- corretude;
- organizacao;
- clareza de regras;
- idempotencia.

## Fase 2 - API real com PostgreSQL

Evolucoes:

- trocar SQLite por PostgreSQL;
- adicionar migrations com Alembic;
- configurar variaveis de ambiente reais;
- melhorar logs estruturados;
- adicionar health check com banco.
- manter CI rodando testes automatizados a cada push/pull request.

Motivo:

PostgreSQL facilita consultas relacionais, constraints e transacoes mais robustas.

## Fase 3 - Integracao real Pipefy

Evolucoes:

- adicionar token Pipefy via variavel/Secrets Manager;
- implementar HTTP client para GraphQL;
- tratar erros da API externa;
- adicionar retry com backoff;
- registrar payloads enviados e respostas relevantes.

Motivo:

A camada `PipefyService` ja isola o ponto onde a simulacao vira chamada real.

## Fase 4 - Webhooks resilientes

Evolucoes:

- API Gateway recebe webhook;
- Lambda valida payload;
- SQS desacopla recebimento de processamento;
- worker processa evento;
- idempotencia segue por `event_id`.

Motivo:

Webhooks podem chegar em pico ou serem reenviados. Fila evita perda e melhora controle de retry.

## Fase 5 - Observabilidade e operacao

Evolucoes:

- CloudWatch Logs;
- metricas de eventos processados;
- alarmes de falha;
- dashboard de webhooks;
- rastreamento de duplicidade;
- runbook de incidentes.

## Fase 6 - Seguranca

Evolucoes:

- adicionar `Bearer token` simples para ambiente local, se fizer sentido;
- validacao de assinatura do webhook, se disponivel;
- secrets no Secrets Manager;
- IAM com minimo privilegio;
- mascaramento de dados sensiveis em logs;
- auditoria de alteracoes importantes.

## Fase 7 - Automacoes e n8n

Evolucoes:

- integrar n8n em fluxos de baixo risco;
- manter regras criticas no backend;
- usar backend como fonte de verdade;
- documentar fluxos automatizados.

## Principio de evolucao

Nao acoplar regra de negocio a ferramenta externa.

Pipefy, AWS, n8n e banco podem mudar. A regra de cliente, prioridade e idempotencia deve continuar clara no dominio da aplicacao.
