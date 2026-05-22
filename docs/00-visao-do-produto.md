# Visao do produto

## Contexto

O Mundo Invest e uma plataforma de planejamento financeiro associada ao ecossistema EWZ. A proposta publica da plataforma envolve organizar a vida financeira do usuario, dar visibilidade de custos, receitas, objetivos e patrimonio, e apoiar decisoes de investimento com tecnologia.

Este teste tecnico pede um esqueleto de sistema interno para gerenciar clientes e mapear eventos para o Pipefy, simulando a integracao real por meio de persistencia local.

## Problema a resolver

O time operacional precisa cadastrar clientes, acompanhar solicitacoes e receber atualizacoes vindas do Pipefy sem gerar duplicidade de processamento.

O sistema deve:

- registrar clientes localmente;
- iniciar o cliente com status de analise;
- montar o payload GraphQL que criaria um card no Pipefy;
- receber um webhook de card atualizado;
- aplicar regra de prioridade baseada em patrimonio;
- montar o payload GraphQL que atualizaria campos no Pipefy;
- garantir idempotencia por `event_id`;
- atualizar o banco local.

## Objetivo do produto

Entregar uma API backend simples, testavel e extensivel, capaz de demonstrar:

- dominio de APIs REST;
- validacao de payload;
- persistencia local;
- regras de negocio;
- integracao simulada com GraphQL/Pipefy;
- tratamento de webhook com idempotencia;
- testes automatizados;
- documentacao clara.

## Usuarios envolvidos

### Operador interno

Pessoa do time operacional que usa o Pipefy para acompanhar solicitacoes e atualizar cards.

### Sistema interno

API que recebe cadastros, persiste dados e reage a eventos vindos do Pipefy.

### Pipefy

Ferramenta externa de controle de processos. Neste teste, ela e simulada: o sistema apenas estrutura as mutations GraphQL reais, sem enviar requisicoes para servidores do Pipefy.

## Valor para o negocio

- Reduzir trabalho manual.
- Evitar duplicidade em webhooks.
- Criar base tecnica para automacoes futuras.
- Manter regras de cliente centralizadas no backend.
- Facilitar evolucao para AWS, filas e banco gerenciado.

