# Seguranca e autenticacao

## Objetivo

Definir como o projeto pode controlar acesso sem comprometer o foco do teste tecnico.

## Decisao para o MVP do teste

Autenticacao fica classificada como prioridade P1.

Ela nao entra como requisito obrigatorio do MVP, mas foi implementada como protecao opcional.

Motivos:

- o enunciado nao pede autenticacao;
- o foco principal e Pipefy GraphQL, banco local, webhook e idempotencia;
- adicionar seguranca antes dos fluxos centrais pode aumentar risco e tempo;
- a entrega deve permanecer facil de executar pelo avaliador.

Mesmo assim, a preocupacao de seguranca e valida e deve aparecer como evolucao planejada.

## Opcao simples para evolucao local

Adicionar um token estatico via variavel de ambiente:

```text
API_ACCESS_TOKEN=token_local_de_desenvolvimento
```

A variavel ja esta prevista no arquivo `.env.example` e no objeto `Settings`. Quando preenchida, os endpoints principais exigem `Authorization: Bearer <token>`.

Clientes chamariam a API com:

```http
Authorization: Bearer token_local_de_desenvolvimento
```

Comportamento:

- se `API_ACCESS_TOKEN` nao estiver configurado, a autenticacao pode ficar desativada em ambiente local;
- se estiver configurado, endpoints protegidos exigem o header `Authorization`.

Essa abordagem e simples e suficiente para demonstrar controle de acesso sem criar complexidade de usuarios, senha e JWT.

## Endpoints que deveriam ser protegidos

| Endpoint | Protecao sugerida |
|---|---|
| `POST /clientes` | `Bearer token` |
| `POST /webhooks/pipefy/card-updated` | token ou assinatura de webhook |
| `GET /health` | publico |
| `/docs` | publico localmente, restrito em producao |

## Webhook Pipefy

Para webhooks, o ideal em producao e validar algum segredo compartilhado ou assinatura enviada pelo provedor.

Como alternativa simples:

```http
X-Webhook-Token: segredo_do_webhook
```

Mas isso so deve ser implementado se estiver claro que o produtor do webhook consegue enviar esse header.

## Producao AWS

Em AWS, as opcoes melhores seriam:

- API Gateway Authorizer;
- Cognito ou JWT para endpoints internos;
- Secrets Manager para guardar tokens;
- IAM com minimo privilegio;
- WAF, se a API for publica;
- logs sem expor dados sensiveis.

## Riscos de implementar cedo demais

Adicionar autenticacao no teste pode:

- dificultar a execucao do avaliador;
- quebrar exemplos de curl se o README nao estiver impecavel;
- desviar atencao do ponto alto, que e Pipefy GraphQL;
- aumentar superficie de bugs.

## Recomendacao

Para a entrega:

1. Documentar autenticacao como evolucao P1.
2. Manter MVP focado nos fluxos obrigatorios.
3. Manter `Bearer token` opcional para nao dificultar a avaliacao local.
4. No video, comentar que em producao usaria API Gateway Authorizer ou validacao de assinatura de webhook.
