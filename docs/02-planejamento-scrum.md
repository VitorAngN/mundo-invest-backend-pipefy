# Planejamento Scrum

## Produto

API backend para gerenciamento de clientes e simulacao de integracao Pipefy.

## Product Goal

Entregar um backend testavel e documentado que cadastre clientes, simule mutations GraphQL do Pipefy e processe webhooks com idempotencia.

## Papeis

| Papel | Responsabilidade neste teste |
|---|---|
| Product Owner | Interpretar requisitos do teste e priorizar valor |
| Scrum Master | Controlar fluxo, riscos e definicao de pronto |
| Developer | Implementar API, banco, testes e documentacao |
| Stakeholder | Avaliador tecnico / Mundo Invest |

Neste projeto individual, o candidato acumula PO, Scrum Master e Developer, mas documenta as decisoes para mostrar maturidade.

## Definition of Ready

Uma historia esta pronta para desenvolvimento quando:

- possui objetivo claro;
- possui payload esperado, quando aplicavel;
- possui criterios de aceite;
- possui impacto no banco identificado;
- possui teste esperado definido.

## Definition of Done

Uma historia esta pronta quando:

- codigo implementado;
- validacao de entrada funcionando;
- persistencia funcionando, se aplicavel;
- teste automatizado passando;
- README/docs atualizados, se necessario;
- endpoint validado localmente;
- sem dependencia de servidor real do Pipefy.

## Board

Colunas sugeridas:

```text
Backlog -> Ready -> Doing -> Code Review/Self Review -> Testing -> Done
```

## Backlog priorizado

| Prioridade | Historia | Estimativa | Status inicial |
|---|---|---:|---|
| P0 | Configurar projeto Python/FastAPI | 2 pts | Ready |
| P0 | Modelar banco local | 3 pts | Ready |
| P0 | Implementar POST /clientes | 5 pts | Ready |
| P0 | Estruturar mutation createCard | 3 pts | Ready |
| P0 | Implementar POST /webhooks/pipefy/card-updated | 5 pts | Ready |
| P0 | Implementar idempotencia por event_id | 5 pts | Ready |
| P0 | Estruturar mutation updateCardField | 3 pts | Ready |
| P0 | Criar testes obrigatorios | 5 pts | Ready |
| P1 | Documentar execucao e curls | 3 pts | Ready |
| P1 | Documentar visao AWS | 2 pts | Ready |
| P1 | Criar roteiro de video | 2 pts | Ready |
| P1 | Implementar autenticacao opcional por token | 2 pts | Done |
| P2 | Adicionar testes extras | 3 pts | Backlog |
| P2 | Preparar Docker opcional | 3 pts | Backlog |

## Sprint 0 - Planejamento

Objetivo:

- entender requisitos;
- pesquisar empresa;
- pesquisar Pipefy GraphQL;
- definir arquitetura;
- definir backlog;
- definir criterios de aceite.

Entregaveis:

- documentacao de produto;
- backlog Scrum;
- contratos de API;
- modelo de dados;
- plano de testes;
- decisoes tecnicas.

## Sprint 1 - Fluxo de criacao de cliente

Objetivo:

- criar base FastAPI;
- criar banco local;
- implementar validacao e persistencia de cliente;
- estruturar payload `createCard`.

Entregaveis:

- `POST /clientes`;
- model `Cliente`;
- service de cliente;
- PipefyService com `createCard`;
- teste de criacao.

## Sprint 2 - Webhook e idempotencia

Objetivo:

- implementar webhook;
- aplicar prioridade por patrimonio;
- bloquear evento duplicado;
- estruturar payload `updateCardField`.

Entregaveis:

- `POST /webhooks/pipefy/card-updated`;
- model `WebhookEvent`;
- service de webhook;
- testes de prioridade e duplicidade.

## Sprint 3 - Qualidade e entrega

Objetivo:

- revisar README;
- rodar testes;
- validar endpoints;
- preparar video;
- preparar Git.

Entregaveis:

- README final;
- docs de AWS;
- roteiro de video;
- testes passando;
- commit final.

## Riscos e mitigacoes

| Risco | Impacto | Mitigacao |
|---|---|---|
| Perder tempo com Pipefy real | Alto | Simular envio e focar no payload oficial |
| Duplicidade de webhook | Alto | Tabela `webhook_events` com `event_id` unico |
| Misturar regra com rota | Medio | Separar routes, services e repositories |
| Falha de ambiente Python | Medio | Usar Python 3.11/3.12 |
| README fraco | Alto | Documentar comandos, curls, AWS e decisoes |
| Autenticacao roubar foco do teste | Medio | Documentar como P1 e implementar so se os fluxos obrigatorios estiverem prontos |
