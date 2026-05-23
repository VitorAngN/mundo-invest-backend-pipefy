# Validacao final

Data da validacao: 2026-05-22.

## Resumo

O projeto foi validado localmente com testes automatizados, compilacao dos arquivos Python, verificacao de links locais em Markdown e smoke test HTTP.

## Testes automatizados

Comando:

```powershell
pytest -v
```

Resultado:

```text
24 passed
```

Cobertura de cenarios:

- criacao de cliente com payload valido;
- validacao de email invalido;
- rejeicao de nome vazio apos trim;
- normalizacao de strings;
- bloqueio de email duplicado;
- carregamento de configuracao;
- constraints unicas de banco;
- mutations Pipefy `createCard`;
- mutations Pipefy `updateCardField`;
- formatacao de patrimonio no payload Pipefy;
- autenticacao opcional por token;
- prioridade alta;
- prioridade normal;
- prioridade alta no limite de `200000`;
- idempotencia por `event_id`;
- webhook para cliente inexistente;
- rejeicao de `event_id` vazio.

## Compile check

Comando:

```powershell
python -m compileall app tests -q
```

Resultado:

```text
OK
```

## Markdown

Verificacoes:

- links locais entre arquivos `.md`;
- ausencia de mojibake real em arquivos UTF-8.

Resultado:

```text
OK
```

## Smoke test HTTP

Fluxos validados manualmente:

- `GET /health`;
- `POST /clientes`;
- `POST /webhooks/pipefy/card-updated`;
- protecao opcional com `API_ACCESS_TOKEN`.

Resultados:

- health check retornou `ok`;
- criacao de cliente retornou status inicial;
- webhook retornou `processed: true`;
- prioridade calculada como `prioridade_alta`;
- sem token, quando `API_ACCESS_TOKEN` esta ativo, endpoint retorna `401`;
- com token correto, endpoint aceita a requisicao.

## Pendencias fora do codigo

- criar repositorio remoto;
- fazer push;
- gravar video;
- preencher formulario de entrega.

