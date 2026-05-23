# Checklist de entrega

## Antes de implementar

- [x] Requisitos lidos.
- [x] Escopo definido.
- [x] Backlog Scrum criado.
- [x] Arquitetura definida.
- [x] Contratos de API definidos.
- [x] Modelo de dados definido.
- [x] Plano de testes definido.
- [x] Mutations Pipefy documentadas.

## Implementacao

- [x] Projeto Python criado.
- [x] Ambiente virtual documentado.
- [x] Configuracao centralizada em `Settings`.
- [x] FastAPI configurado.
- [x] Banco local configurado.
- [x] Model `Cliente` criado.
- [x] Model `WebhookEvent` criado.
- [x] Constraints unicas de email e `event_id` testadas.
- [x] `POST /clientes` implementado.
- [x] `createCard` estruturado.
- [x] `POST /webhooks/pipefy/card-updated` implementado.
- [x] Idempotencia por `event_id` implementada.
- [x] Regra de prioridade implementada.
- [x] `updateCardField` estruturado.

## Testes

- [x] Teste de criacao de cliente.
- [x] Teste de prioridade alta.
- [x] Teste de prioridade normal.
- [x] Teste de evento duplicado.
- [x] Teste de email invalido.
- [x] Testes especificos do `PipefyService`.
- [x] Testes de constraints de banco.
- [x] Testes de autenticacao opcional.
- [x] `pytest -v` passando.

## Documentacao

- [x] README com execucao local.
- [x] README com exemplos de curl.
- [x] README com testes.
- [x] README com Pipefy GraphQL.
- [x] README com visao AWS.
- [x] Estrategia de seguranca/autenticacao documentada.
- [x] Autenticacao opcional por `API_ACCESS_TOKEN` testada.
- [x] Docs de arquitetura revisados.
- [x] Roteiro de video revisado.
- [x] Relatorio de validacao criado.

## Video

- [ ] Mostrar background.
- [ ] Mostrar estrutura de pastas.
- [ ] Mostrar `createCard`.
- [ ] Mostrar `updateCardField`.
- [ ] Rodar testes.
- [ ] Rodar endpoints.
- [ ] Falar da visao AWS.
- [ ] Ficar abaixo de 7 minutos.

## Git e envio

- [x] `git status` revisado localmente.
- [x] Arquivos temporarios ignorados.
- [x] GitHub Actions configurado para testes.
- [x] Commits locais criados com mensagens claras.
- [ ] Repositorio remoto criado.
- [ ] Push realizado.
- [ ] Link conferido.
- [ ] Formulario preenchido.

