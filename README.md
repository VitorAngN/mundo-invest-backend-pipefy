# Client Management & Pipefy Integration

API backend em Python para gerenciamento de clientes, persistencia local e simulacao de integracao com Pipefy via GraphQL.

Este projeto foi estruturado para o teste tecnico de Desenvolvedor Backend do Mundo Invest.

## Status do projeto

O projeto esta organizado para evoluir por etapas:

1. Planejamento e documentacao.
2. Implementacao dos fluxos obrigatorios.
3. Testes automatizados.
4. Revisao final, video e entrega.

A ideia e demonstrar nao apenas codigo funcionando, mas tambem capacidade de pensar em produto, manutencao, escalabilidade e operacao.

## Tecnologias

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Pytest
- GraphQL

## Funcionalidades implementadas

- Cadastro de cliente com validacao de payload.
- Persistencia local em SQLite.
- Status inicial `Aguardando Análise`.
- Payload GraphQL `createCard` estruturado conforme Pipefy.
- Webhook simulado de card atualizado.
- Idempotencia por `event_id`.
- Regra de prioridade por patrimonio.
- Payload GraphQL `updateCardField` estruturado conforme Pipefy.
- Constraints unicas para `cliente_email` e `event_id`.
- Autenticacao opcional por `API_ACCESS_TOKEN`.
- Testes automatizados cobrindo fluxos obrigatorios e casos extras.

## Contexto

O Mundo Invest e uma plataforma de planejamento financeiro ligada ao ecossistema EWZ, com foco em organizacao financeira, investimentos, tecnologia e atendimento consultivo.

Por isso, a solucao prioriza:

- clareza de regra de negocio;
- rastreabilidade de eventos;
- idempotencia de webhooks;
- isolamento da integracao Pipefy;
- documentacao objetiva;
- caminho simples para evolucao em AWS.

Mais detalhes em [docs/empresa.md](docs/empresa.md).

## Estrutura planejada

```text
app/
  routes/           # camada HTTP
  services/         # casos de uso e regras de negocio
  repositories/     # acesso ao banco
  models.py         # entidades SQLAlchemy
  schemas.py        # contratos Pydantic
tests/              # testes automatizados
docs/               # documentacao de produto, arquitetura e operacao
```

## Documentacao

Antes da implementacao final, o projeto foi modelado em documentos de produto, requisitos, Scrum, arquitetura, contratos de API, dados, testes, operacao e evolucao.

Indice completo em [docs/README.md](docs/README.md).

Principais documentos:

- [Visao do produto](docs/00-visao-do-produto.md)
- [Requisitos e escopo](docs/01-requisitos-e-escopo.md)
- [Planejamento Scrum](docs/02-planejamento-scrum.md)
- [Arquitetura planejada](docs/03-arquitetura-planejada.md)
- [Contratos de API](docs/04-contratos-api.md)
- [Modelagem de dados](docs/05-modelagem-dados.md)
- [Plano de testes](docs/06-plano-de-testes.md)
- [Mapeamento Pipefy GraphQL](docs/07-mapeamento-pipefy-graphql.md)
- [Padroes de codigo](docs/08-padroes-de-codigo.md)
- [Operacao local](docs/09-operacao-local.md)
- [Roadmap de escalabilidade](docs/10-roadmap-escalabilidade.md)
- [Decisoes arquiteturais](docs/11-decisoes-arquiteturais.md)
- [Checklist de entrega](docs/12-checklist-entrega.md)
- [Seguranca e autenticacao](docs/13-seguranca-autenticacao.md)

## Como rodar localmente

Use Python 3.11 ou 3.12. Neste PC, o comando recomendado e `py -3.11`, porque o Python 3.14 ainda pode quebrar dependencias nativas do Pydantic/FastAPI.

Crie e ative o ambiente virtual:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instale as dependencias:

```powershell
pip install -r requirements.txt
```

Suba a API:

```powershell
uvicorn app.main:app --reload
```

Abra a documentacao automatica:

```text
http://127.0.0.1:8000/docs
```

## Como rodar os testes

```powershell
pytest -v
```

Cobertura atual de cenarios:

- criacao de cliente;
- validacao de email;
- validacao de strings vazias;
- email duplicado;
- config por ambiente;
- constraints de banco;
- mutations Pipefy;
- token opcional;
- prioridade alta, normal e limite;
- idempotencia de webhook;
- cliente inexistente no webhook.

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

O cliente e salvo localmente com status inicial:

```text
Aguardando Analise
```

No codigo final, o texto pode manter o acento do enunciado: `Aguardando Análise`.

A resposta tambem inclui o payload GraphQL que seria enviado ao Pipefy.

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

Regras:

- `valor_patrimonio >= 200000`: `prioridade_alta`
- `valor_patrimonio < 200000`: `prioridade_normal`
- `event_id` duplicado nao e reprocessado
- cliente atualizado para `Processado`

## Pipefy GraphQL

As mutations devem ficar isoladas em `PipefyService`, sem chamada real ao Pipefy nesta versao do teste.

Resumo:

- `createCard` cria o card simulado do cliente.
- `updateCardField` atualiza status e prioridade.

Detalhes em [docs/07-mapeamento-pipefy-graphql.md](docs/07-mapeamento-pipefy-graphql.md).

## Visao de producao na AWS

Em producao, esta API poderia ser exposta via API Gateway e executada em Lambda. Para persistencia, RDS PostgreSQL faria sentido quando houver necessidade de relacionamentos, transacoes e consultas SQL; DynamoDB tambem seria uma boa opcao para idempotencia por `event_id`.

Para webhooks, uma arquitetura mais resiliente usaria API Gateway recebendo o evento, Lambda para validacao inicial, SQS para desacoplar o processamento e um worker Lambda para aplicar regras de negocio e chamar a API real do Pipefy. Logs e metricas ficariam no CloudWatch, e tokens do Pipefy ficariam no Secrets Manager.

Mais detalhes em [docs/arquitetura-aws.md](docs/arquitetura-aws.md).

## Video de defesa

Roteiro sugerido em [docs/roteiro-video.md](docs/roteiro-video.md).
