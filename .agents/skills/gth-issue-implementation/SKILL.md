---
name: gth-issue-implementation
description: Orquestra a análise, planejamento, implementação e fechamento de issues do monorepo GTH Agents. Use quando o usuário pedir para analisar, planejar, implementar, revisar ou concluir uma ISSUE do projeto, coordenando inspeção do repositório, contratos reais, skills especializadas, validação e documentação.
---

# GTH Issue Implementation

## Objetivo

Executar issues do GTH Agents com rastreabilidade, aderência ao escopo e uso dos padrões reais do monorepo.

## Fluxo obrigatório

1. Leia integralmente a ISSUE e identifique objetivo, escopo, critérios de aceite e itens fora do escopo.
2. Inspecione o estado atual do monorepo antes de sugerir arquivos ou alterações.
3. Classifique a tarefa como frontend, backend, infraestrutura, documentação ou combinação.
4. Acione as Skills especializadas aplicáveis.
5. Confirme contratos reais, arquivos existentes, padrões arquiteturais e mecanismos de autenticação/autorização.
6. Identifique divergências entre a ISSUE e o código atual.
7. Produza um plano de implementação antes de alterar código, salvo quando o usuário pedir execução direta.
8. Implemente apenas o escopo confirmado.
9. Execute as validações aplicáveis.
10. Gere ou atualize o walkthrough com evidências reais.
11. Apresente arquivos alterados, validações, limitações e riscos remanescentes.

## Regras de decisão

- O código atual e os contratos reais prevalecem sobre exemplos marcados como esperados, sugeridos ou prováveis.
- Quando a ISSUE exigir algo sem suporte no backend, não invente endpoint, payload, resposta ou dado simulado.
- Quando houver divergência impeditiva, implemente a parte possível e registre claramente o bloqueio.
- Reutilize componentes, services, use cases e padrões existentes antes de criar novos.
- Não amplie o escopo silenciosamente.
- Não faça refatorações oportunistas sem necessidade direta para a ISSUE.

## Evidências

Diferencie sempre:

- validado por execução;
- verificado por inspeção estática;
- não validado;
- bloqueado por contrato ou ambiente.

Nunca declare como testado algo apenas lido no código.

## Restrições

- Não executar commit, push, merge, tag, criação ou troca de branch sem autorização explícita.
- Não alterar arquivos internos do Antigravity.
- Não criar `files.md` dentro do repositório.
- Não expor senhas, tokens, hashes, segredos ou dados pessoais em documentos.
- Não usar caminhos absolutos da máquina em documentação versionada.
- Não apagar arquivos ou dados sem necessidade comprovada e autorização compatível.

## Formato do relatório final

1. Resumo da entrega.
2. Contratos e padrões confirmados.
3. Arquivos criados e alterados.
4. Validações executadas e resultados.
5. Cenários verificados apenas por inspeção.
6. Limitações, riscos e pendências.
7. Estado para fechamento da ISSUE.
