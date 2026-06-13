---
name: gth-documentation
description: Cria e revisa planos de implementação, walkthroughs e documentação técnica de issues do GTH Agents. Use ao documentar uma implementação, organizar arquivos em docs, registrar evidências, revisar coerência ou preparar o fechamento de uma ISSUE.
---

# GTH Documentation

## Objetivo

Documentar decisões, execução e evidências do GTH Agents de forma rastreável e honesta.

## Organização

Use, conforme a camada predominante:

```text
docs/frontend/implementation-plans/
docs/frontend/walkthroughs/
docs/backend/implementation-plans/
docs/backend/walkthroughs/
```

Nomes sugeridos:

```text
implementation_plan_issue_025_pdi.md
walkthrough_issue_025_pdi.md
```

## Plano de implementação

Deve conter:

- objetivo e escopo;
- estado atual inspecionado;
- contratos reais confirmados;
- arquivos a criar e alterar;
- fluxo funcional;
- regras de perfil e escopo;
- estratégia de erros e estados;
- estratégia de validação;
- riscos e itens fora do escopo.

## Walkthrough

Deve conter:

- resumo da implementação;
- arquivos criados e alterados;
- decisões técnicas;
- contratos efetivamente usados;
- comandos executados;
- resultados reais;
- cenários validados por execução;
- comportamentos verificados por inspeção;
- limitações e pendências;
- conclusão sobre fechamento da ISSUE.

## Regras editoriais

- Use caminhos relativos ao repositório.
- Preserve payloads e respostas reais sem inventar campos.
- Não chamar regras determinísticas de IA generativa.
- Não afirmar que um cenário foi testado se apenas existe fallback no código.
- Diferencie proteção visual de autorização HTTP.
- Evite percentuais sem cálculo.
- Não mascarar erros dos dados de teste como se o dado real fosse diferente.
- Links de mídias devem apontar para caminhos relativos existentes.

## Segurança

Nunca incluir:

- senha;
- token JWT;
- hash de senha;
- segredo;
- `.env` real;
- dados pessoais desnecessários;
- caminho absoluto da máquina.

## Arquivos internos do agente

- Não criar, mover ou versionar `files.md`.
- Não incluir configurações internas do Antigravity na documentação do projeto.
