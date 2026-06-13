---
name: gth-api-contract-analysis
description: Inspeciona e confirma contratos reais da API Flask do GTH Agents antes de implementar integrações. Use quando uma issue mencionar endpoints, payloads, respostas, enums, permissões, códigos HTTP ou quando o frontend depender do backend.
---

# GTH API Contract Analysis

## Objetivo

Impedir integrações baseadas em endpoints imaginários, campos presumidos ou exemplos desatualizados.

## Fontes prioritárias

Inspecione, conforme existirem:

1. rotas Flask e blueprints;
2. schemas e validadores;
3. DTOs;
4. use cases;
5. entidades e enums;
6. serializers ou montagem de `jsonify`;
7. testes automatizados;
8. coleção Postman e documentação, apenas como apoio.

O código executável e os testes prevalecem sobre documentação antiga.

## Para cada operação, confirme

- método HTTP;
- URL exata;
- autenticação exigida;
- perfis autorizados;
- regra de escopo;
- payload obrigatório e opcional;
- enums aceitos;
- formato da resposta;
- status HTTP de sucesso;
- erros relevantes;
- transições de estado;
- inclusão ou não de recursos relacionados.

## Procedimento

1. Pesquise por entidade, blueprint, rota e use case.
2. Leia o fluxo completo da requisição até a persistência.
3. Consulte testes para confirmar comportamento de borda.
4. Registre divergências entre a ISSUE e a implementação.
5. Proponha adaptação do consumidor sem inventar contrato.

## Saída esperada

Apresente uma tabela ou blocos contendo:

```text
Operação
Método e URL
Permissão
Request
Response
Status
Erros e regras
Fonte no código
```

## Restrições

- Não presumir que endpoints REST convencionais existam.
- Não inferir campos apenas pelo nome da entidade.
- Não usar exemplos antigos como fonte de verdade sem confirmar no código.
- Não criar chamada separada se o recurso já vier incorporado na resposta principal.
- Não omitir divergência que reduza o escopo implementável.
