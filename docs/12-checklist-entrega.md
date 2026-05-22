# Checklist de entrega

## Antes de implementar

- [ ] Requisitos lidos.
- [ ] Escopo definido.
- [ ] Backlog Scrum criado.
- [ ] Arquitetura definida.
- [ ] Contratos de API definidos.
- [ ] Modelo de dados definido.
- [ ] Plano de testes definido.
- [ ] Mutations Pipefy documentadas.

## Implementacao

- [ ] Projeto Python criado.
- [ ] Ambiente virtual documentado.
- [ ] Configuracao centralizada em `Settings`.
- [ ] FastAPI configurado.
- [ ] Banco local configurado.
- [ ] Model `Cliente` criado.
- [ ] Model `WebhookEvent` criado.
- [ ] Constraints unicas de email e `event_id` testadas.
- [ ] `POST /clientes` implementado.
- [ ] `createCard` estruturado.
- [ ] `POST /webhooks/pipefy/card-updated` implementado.
- [ ] Idempotencia por `event_id` implementada.
- [ ] Regra de prioridade implementada.
- [ ] `updateCardField` estruturado.

## Testes

- [ ] Teste de criacao de cliente.
- [ ] Teste de prioridade alta.
- [ ] Teste de prioridade normal.
- [ ] Teste de evento duplicado.
- [ ] Teste de email invalido.
- [ ] Testes especificos do `PipefyService`.
- [ ] `pytest -v` passando.

## Documentacao

- [ ] README com execucao local.
- [ ] README com exemplos de curl.
- [ ] README com testes.
- [ ] README com Pipefy GraphQL.
- [ ] README com visao AWS.
- [ ] Estrategia de seguranca/autenticacao documentada.
- [ ] Autenticacao opcional por `API_ACCESS_TOKEN` testada.
- [ ] Docs de arquitetura revisados.
- [ ] Roteiro de video revisado.

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

- [ ] `git status` revisado.
- [ ] Arquivos temporarios ignorados.
- [ ] Commit criado com mensagem clara.
- [ ] Repositorio remoto criado.
- [ ] Push realizado.
- [ ] Link conferido.
- [ ] Formulario preenchido.
