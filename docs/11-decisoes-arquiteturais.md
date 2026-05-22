# Decisoes arquiteturais

Este arquivo registra decisoes importantes do projeto em formato ADR simplificado.

## ADR 001 - Usar Python com FastAPI

Status: Aceita.

Contexto:

O teste permite Python ou Golang. A vaga pede backend, GraphQL, Pipefy e AWS.

Decisao:

Usar Python com FastAPI.

Motivos:

- desenvolvimento rapido;
- validacao forte com Pydantic;
- documentacao automatica em Swagger;
- ecossistema bom para APIs e testes;
- aderente ao requisito da vaga.

Consequencias:

- precisa fixar versao de Python estavel;
- Python 3.11 ou 3.12 e recomendado.

## ADR 002 - Usar SQLite no teste local

Status: Aceita.

Contexto:

O teste aceita SQLite ou PostgreSQL via Docker.

Decisao:

Usar SQLite local.

Motivos:

- reduz atrito de execucao;
- facilita avaliacao;
- suficiente para persistencia local do teste.

Consequencias:

- para producao, trocar por PostgreSQL/RDS ou DynamoDB;
- documentar caminho de evolucao.

## ADR 003 - Separar routes, services e repositories

Status: Aceita.

Contexto:

O projeto precisa mostrar capacidade de crescer e ser mantido.

Decisao:

Separar camadas:

```text
routes -> services -> repositories -> database
```

Motivos:

- rotas ficam pequenas;
- regra de negocio fica testavel;
- banco fica isolado;
- novas integracoes podem ser adicionadas sem baguncar endpoints.

Consequencias:

- mais arquivos no inicio;
- melhor clareza para evolucao.

## ADR 004 - Isolar GraphQL Pipefy em PipefyService

Status: Aceita.

Contexto:

O teste exige mutations Pipefy reais, mas nao chamada real.

Decisao:

Centralizar mutations e montagem de variaveis no `PipefyService`.

Motivos:

- mostra claramente o ponto alto do teste;
- evita GraphQL espalhado;
- facilita trocar simulacao por HTTP real;
- melhora testabilidade.

Consequencias:

- `PipefyService` deve ser bem documentado;
- IDs de campos devem ser configuraveis.

## ADR 005 - Idempotencia por event_id

Status: Aceita.

Contexto:

Webhooks podem ser reenviados.

Decisao:

Persistir `event_id` em tabela de eventos processados, com constraint unica.

Motivos:

- evita reprocessamento;
- protege contra duplicidade;
- deixa auditoria minima.

Consequencias:

- webhook duplicado retorna sucesso logico, mas `processed: false`;
- em producao, a mesma ideia pode ir para DynamoDB ou RDS.

## ADR 006 - Autenticacao por token como P1

Status: Aceita e implementada como protecao opcional.

Contexto:

Controle de acesso e importante para um produto real, especialmente em um dominio que envolve clientes, patrimonio e integracoes internas. Ainda assim, o teste tecnico nao exige autenticacao e o foco principal e demonstrar os fluxos de cliente, Pipefy GraphQL, webhook, idempotencia e testes.

Decisao:

Tratar autenticacao por token como prioridade P1, nao como requisito P0 do MVP. A implementacao fica desativada por padrao e e ativada somente quando `API_ACCESS_TOKEN` estiver configurado.

Motivos:

- evita desviar o foco dos requisitos obrigatorios;
- reduz risco de dificultar a execucao local pelo avaliador;
- mostra preocupacao com seguranca sem adicionar complexidade prematura;
- permite evoluir para `Bearer token` simples caso os fluxos centrais estejam finalizados.

Consequencias:

- o MVP pode rodar sem token;
- endpoints principais passam a exigir `Authorization: Bearer <token>` quando `API_ACCESS_TOKEN` existe;
- a estrategia de autenticacao fica documentada;
- em producao, preferir API Gateway Authorizer, JWT/Cognito ou validacao de assinatura para webhooks.
