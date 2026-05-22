# Operacao local

## Objetivo

Documentar como preparar, executar e validar a aplicacao localmente.

## Versao de Python

Recomendado:

```text
Python 3.11 ou 3.12
```

Neste computador, usar:

```powershell
py -3.11
```

Motivo:

Python 3.14 pode ser recente demais para algumas dependencias nativas do ecossistema FastAPI/Pydantic.

## Criar ambiente virtual

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## Instalar dependencias

```powershell
pip install -r requirements.txt
```

## Variaveis de ambiente

Copiar `.env.example` para `.env` caso queira customizar configuracoes.

Principais variaveis:

| Variavel | Descricao |
|---|---|
| `DATABASE_URL` | URL do banco local |
| `PIPEFY_PIPE_ID` | ID do pipe simulado |
| `PIPEFY_FIELD_CLIENTE_NOME` | ID do campo nome |
| `PIPEFY_FIELD_CLIENTE_EMAIL` | ID do campo email |
| `PIPEFY_FIELD_TIPO_SOLICITACAO` | ID do campo tipo de solicitacao |
| `PIPEFY_FIELD_VALOR_PATRIMONIO` | ID do campo patrimonio |
| `PIPEFY_FIELD_STATUS` | ID do campo status |
| `PIPEFY_FIELD_PRIORIDADE` | ID do campo prioridade |
| `API_ACCESS_TOKEN` | Token planejado para autenticacao P1 |

Observacao:

`API_ACCESS_TOKEN` nao bloqueia o MVP. Quando vazio, a API roda sem exigir token. Quando preenchido, endpoints principais exigem `Authorization: Bearer <token>`.

Exemplo com token:

```powershell
$env:API_ACCESS_TOKEN="token_de_teste"
uvicorn app.main:app --reload
```

## Rodar API

```powershell
uvicorn app.main:app --reload
```

URL local:

```text
http://127.0.0.1:8000
```

Documentacao Swagger:

```text
http://127.0.0.1:8000/docs
```

## Rodar testes

```powershell
pytest -v
```

## Health check

```powershell
curl.exe "http://127.0.0.1:8000/health"
```

## Teste manual do fluxo

### 1. Criar cliente

```powershell
curl.exe -X POST "http://127.0.0.1:8000/clientes" `
  -H "Content-Type: application/json" `
  -d "{\"cliente_nome\":\"Joao Silva\",\"cliente_email\":\"joao.silva@example.com\",\"tipo_solicitacao\":\"Atualizacao cadastral\",\"valor_patrimonio\":250000}"
```

Com token:

```powershell
curl.exe -X POST "http://127.0.0.1:8000/clientes" `
  -H "Content-Type: application/json" `
  -H "Authorization: Bearer token_de_teste" `
  -d "{\"cliente_nome\":\"Joao Silva\",\"cliente_email\":\"joao.silva@example.com\",\"tipo_solicitacao\":\"Atualizacao cadastral\",\"valor_patrimonio\":250000}"
```

### 2. Processar webhook

```powershell
curl.exe -X POST "http://127.0.0.1:8000/webhooks/pipefy/card-updated" `
  -H "Content-Type: application/json" `
  -d "{\"event_id\":\"evt_123\",\"card_id\":\"card_456\",\"cliente_email\":\"joao.silva@example.com\",\"timestamp\":\"2026-05-18T12:00:00Z\"}"
```

### 3. Testar idempotencia

Enviar o mesmo webhook novamente.

Resultado esperado:

```json
{
  "processed": false,
  "duplicated": true
}
```

## Troubleshooting

### `ModuleNotFoundError: app`

Rode os comandos na raiz do projeto.

### Porta 8000 ocupada

Use outra porta:

```powershell
uvicorn app.main:app --reload --port 8001
```

### Erro instalando Pydantic no Python 3.14

Use Python 3.11:

```powershell
py -3.11 -m venv .venv
```

### Problema com acentos no curl do Windows

Use texto sem acento nos exemplos manuais ou envie JSON por arquivo UTF-8.
