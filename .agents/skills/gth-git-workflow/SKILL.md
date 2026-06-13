---
name: gth-git-workflow
description: Orienta e executa com segurança o fluxo Git do GTH Agents, incluindo branches por issue, staging seletivo, Conventional Commits, push, Pull Request e atualização local. Use quando o usuário pedir comandos Git, commit, push, PR, fechamento de issue ou sincronização da main.
---

# GTH Git Workflow

## Objetivo

Manter histórico rastreável por ISSUE sem incluir arquivos acidentais ou executar operações remotas sem autorização.

## Antes de qualquer escrita

```bash
git branch --show-current
git status
git diff --stat
git diff --check
```

Confirme que a branch corresponde à ISSUE e que não há alterações alheias misturadas.

## Branches

Padrões preferidos:

```text
feature/issue-025-pdi
fix/issue-XXX-descricao
chore/issue-XXX-descricao
docs/issue-XXX-descricao
```

Não trabalhar diretamente em `main` para implementação de issue.

## Staging

- Prefira `git add <caminhos-específicos>`.
- Revise com `git diff --cached --stat`, `git diff --cached --check` e `git diff --cached`.
- Evite `git add .` antes de conferir o estado.
- Não adicionar `.env`, segredos, arquivos temporários ou configurações internas do agente.

## Commits

Use Conventional Commits:

```text
feat(frontend): implement PDI module
fix(api): enforce PDI status transition
docs(frontend): document PDI module
```

Separe commits quando mudanças independentes de backend, frontend ou documentação justificarem histórico próprio.

## Push e PR

Só executar com autorização explícita.

Antes do push:

```bash
git status
git log -1 --oneline
```

Push inicial:

```bash
git push -u origin <branch>
```

O PR deve conter:

- objetivo;
- principais alterações;
- decisões técnicas;
- validações;
- limitações;
- referência à ISSUE.

## Após merge

Fluxo típico:

```bash
git switch main
git pull --ff-only origin main
git branch -d <branch-local>
git fetch --prune
```

Excluir branch remota somente quando desejado e permitido pela política do repositório.

## Restrições

- Não executar commit, push, merge, tag, delete ou troca de branch sem pedido explícito.
- Não usar `--force` ou `--force-with-lease` sem explicar o risco e receber autorização.
- Não apagar branch não mesclada sem comprovação e autorização.
