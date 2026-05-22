# Padroes de codigo e estrutura

## Objetivo

Definir regras para manter o projeto legivel, testavel e preparado para crescer.

## Principio geral

Cada camada deve ter uma responsabilidade clara.

```text
routes -> services -> repositories -> database
             |
             -> external clients/services
```

## Estrutura de pastas alvo

```text
app/
  __init__.py
  main.py
  config.py
  constants.py
  database.py
  models.py
  schemas.py
  routes/
    __init__.py
    clientes.py
    webhooks.py
  services/
    __init__.py
    clientes_service.py
    webhooks_service.py
    pipefy_service.py
  repositories/
    __init__.py
    clientes_repository.py
    webhook_events_repository.py
tests/
docs/
```

## Responsabilidades por camada

### `main.py`

Deve:

- criar a instancia FastAPI por meio de `create_app()`;
- registrar routers;
- configurar lifespan/startup;
- expor `app = create_app()` para o Uvicorn.

Nao deve:

- conter regra de negocio;
- acessar banco diretamente fora da inicializacao;
- montar payloads de integracao.

### `routes`

Pode:

- receber request HTTP;
- depender de `get_db`;
- chamar service;
- converter exceptions em HTTP;
- definir `response_model`.

Nao deve:

- montar SQL;
- calcular regra de prioridade;
- montar GraphQL diretamente;
- saber detalhes de persistencia.

### `services`

Pode:

- executar caso de uso;
- aplicar regra de negocio;
- coordenar repositories;
- coordenar servicos externos simulados;
- controlar commit/rollback quando fizer sentido.

Nao deve:

- conhecer detalhes de status code;
- depender de framework HTTP sem necessidade;
- conter queries longas espalhadas.

### `repositories`

Pode:

- consultar banco;
- criar entidades;
- atualizar entidades;
- esconder detalhes do ORM.

Nao deve:

- decidir regra de negocio;
- montar payload GraphQL;
- retornar respostas HTTP.

### `schemas`

Pode:

- validar payload de entrada;
- definir contrato de resposta;
- usar Pydantic.

Nao deve:

- conter regra de negocio complexa;
- acessar banco.

### `models`

Pode:

- declarar tabelas e campos;
- definir constraints e indices.

Nao deve:

- conter casos de uso.

## Padroes de nomes

- Rotas no plural: `/clientes`.
- Services com sufixo `Service`.
- Repositories com sufixo `Repository`.
- Schemas de entrada com sufixo `Create`, `Update` ou nome do evento.
- Schemas de saida com sufixo `Response`.
- Exceptions de dominio com nomes claros, como `ClienteNotFoundError`.

## Constantes

Strings de negocio devem ficar centralizadas:

```python
STATUS_AGUARDANDO_ANALISE = "Aguardando Analise"
STATUS_PROCESSADO = "Processado"
PRIORIDADE_ALTA = "prioridade_alta"
PRIORIDADE_NORMAL = "prioridade_normal"
```

Motivo:

- evita typo;
- facilita teste;
- facilita alteracao futura.

## Configuracao

Configuracoes devem ficar em `app/config.py`.

Padrao:

- usar `Settings` como objeto imutavel;
- carregar ambiente via `Settings.from_env()`;
- expor `get_settings()` com cache;
- evitar chamar `os.getenv` espalhado pelo codigo.

Variaveis como `DATABASE_URL`, IDs do Pipefy e `API_ACCESS_TOKEN` devem entrar por essa camada.

## Tratamento de erro

Erros de regra devem nascer no service e ser traduzidos na rota.

Exemplo:

```text
ClienteNotFoundError -> HTTP 404
ClienteAlreadyExistsError -> HTTP 409
```

## Testabilidade

Cada regra relevante deve ser testavel sem depender de servidor real externo.

Obrigatorio:

- teste do fluxo de criacao;
- teste da regra de prioridade;
- teste de idempotencia.

Recomendado:

- teste de email invalido;
- teste de cliente inexistente;
- teste de patrimonio exatamente no limite.

## Escalabilidade de codigo

Se novos fluxos surgirem, adicionar:

1. schema de entrada/saida;
2. rota curta;
3. service com caso de uso;
4. repository se houver persistencia;
5. testes;
6. documentacao de contrato.

Evitar criar arquivos gigantes.
