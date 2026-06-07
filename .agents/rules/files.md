---
trigger: always_on
---

# Regras de Organização de Arquivos do GTH Agents

Este documento define onde arquivos novos devem ser criados no monorepo e como o Antigravity deve organizar planos, walkthroughs, evidências e documentação técnica.

O objetivo é impedir que arquivos temporários ou documentos de issues sejam criados nas raízes de `frontend/`, `backend/` ou do monorepo.

---

## Estrutura principal do monorepo

```text
gth-agents/
├── backend/
├── frontend/
├── docs/
│   ├── frontend/
│   │   ├── implementation-plans/
│   │   └── walkthroughs/
│   └── backend/
│       ├── implementation-plans/
│       └── walkthroughs/
├── docker-compose.yml
├── README.md
└── files.md
```

---

## Regra geral

Nunca criar arquivos de plano de implementação ou walkthrough diretamente em:

```text
/
frontend/
backend/
```

Arquivos de documentação devem ser criados diretamente em sua pasta definitiva.

Não criar primeiro na raiz para mover depois.

---

## Planos de implementação

### Frontend

Todo plano relacionado a React, Vite, Axios, páginas, componentes, hooks, contexto, rotas ou interface visual deve ser criado em:

```text
docs/frontend/implementation-plans/
```

Padrão de nome:

```text
implementation_plan_issue_NNN_nome_da_issue.md
```

Exemplo:

```text
docs/frontend/implementation-plans/
implementation_plan_issue_022_evolucao_colaborador.md
```

### Backend

Todo plano relacionado a Flask, API, domínio, casos de uso, banco, SQLAlchemy, Alembic, repositories, autenticação ou testes de backend deve ser criado em:

```text
docs/backend/implementation-plans/
```

Exemplo:

```text
docs/backend/implementation-plans/
implementation_plan_issue_012_reconhecimento.md
```

---

## Walkthroughs

### Frontend

Walkthroughs de implementação ou validação do frontend devem ser criados em:

```text
docs/frontend/walkthroughs/
```

Padrão:

```text
walkthrough_issue_NNN_nome_da_issue.md
```

Exemplo:

```text
docs/frontend/walkthroughs/
walkthrough_issue_022_evolucao_colaborador.md
```

### Backend

Walkthroughs do backend devem ser criados em:

```text
docs/backend/walkthroughs/
```

Exemplo:

```text
docs/backend/walkthroughs/
walkthrough_issue_012_reconhecimento.md
```

---

## Documentos do monorepo

Documentos que tratam da estrutura geral do projeto, migração para monorepo, Docker Compose unificado ou decisões arquiteturais compartilhadas devem ser criados diretamente em:

```text
docs/
```

Exemplos:

```text
docs/walkthrough_migracao_monorepo.md
docs/arquitetura_monorepo.md
docs/decisoes_tecnicas.md
```

---

## Evidências visuais

Imagens, vídeos e outras evidências produzidas durante validações devem permanecer junto ao projeto ao qual pertencem.

### Frontend

```text
frontend/src/assets/imagens/
frontend/src/assets/videos/
```

Padrão de nome recomendado:

```text
issue_022_evolucao_completa.png
issue_022_evolucao_403.png
issue_022_evolucao_mobile.webp
```

Não usar nomes gerados automaticamente com timestamps quando um nome descritivo puder ser utilizado.

### Backend

Evidências específicas do backend podem ser armazenadas em:

```text
backend/docs/assets/
```

Criar a pasta apenas quando houver necessidade real.

---

## Caminhos em Markdown

Nunca usar caminhos absolutos locais, como:

```text
/home/aldomar/Workspaces/...
C:\Users\...
```

Usar sempre caminhos relativos válidos dentro do repositório.

Exemplo para um walkthrough localizado em:

```text
docs/frontend/walkthroughs/
```

referenciando uma imagem em:

```text
frontend/src/assets/imagens/
```

usar caminho semelhante a:

```md
![Evidência](../../../frontend/src/assets/imagens/arquivo.png)
```

Sempre verificar o caminho real após criar ou mover o documento.

---

## README e documentação permanente

Arquivos permanentes devem permanecer próximos ao escopo que documentam.

### Raiz

```text
README.md
files.md
docker-compose.yml
```

### Backend

```text
backend/README.md
backend/CHANGELOG.md
backend/docs/API.md
backend/docs/AUTH.md
backend/docs/POSTMAN_FLOW.md
backend/docs/MVP_BACKEND.md
```

### Frontend

```text
frontend/README.md
```

Não mover esses arquivos para as pastas de walkthroughs ou planos.

---

## Arquivos temporários

Não criar ou versionar:

```text
*.tmp
*.bak
*.old
debug.txt
output.txt
notes.txt
```

Caso um arquivo temporário seja indispensável durante análise, removê-lo antes de finalizar a tarefa.

---

## Nomenclatura

Usar nomes em minúsculas com `snake_case`.

Correto:

```text
implementation_plan_issue_022_evolucao_colaborador.md
walkthrough_issue_022_evolucao_colaborador.md
```

Evitar:

```text
ImplementationPlan.md
WalkThrough Issue 22.md
novo-plano-final-agora-v2.md
```

Número de issue deve utilizar três dígitos quando o projeto estiver seguindo essa convenção:

```text
022
023
024
```

---

## Responsabilidade do Antigravity

Antes de criar qualquer documento, o Antigravity deve:

1. identificar se a tarefa pertence ao frontend, backend ou monorepo;
2. selecionar a pasta definitiva;
3. usar o padrão de nomenclatura;
4. verificar se já existe documento da mesma issue;
5. atualizar o documento existente quando apropriado;
6. evitar duplicatas com nomes levemente diferentes;
7. usar caminhos relativos para evidências;
8. não mover documentação permanente sem autorização.

---

## Planos e implementação

Ao gerar um plano:

```text
Criar ou atualizar:
docs/{escopo}/implementation-plans/
implementation_plan_issue_NNN_nome.md
```

Não iniciar implementação até o plano ser aprovado quando a tarefa solicitar revisão prévia.

---

## Walkthrough e finalização

Ao finalizar uma implementação:

```text
Criar ou atualizar:
docs/{escopo}/walkthroughs/
walkthrough_issue_NNN_nome.md
```

O walkthrough deve registrar, quando aplicável:

```text
arquivos criados
arquivos alterados
contrato utilizado
decisões técnicas
lint
build
testes
Docker
validação visual
erros tratados
limitações conhecidas
```

---

## Proibições

O Antigravity não deve:

```text
criar implementation_plan.md na raiz
criar walkthrough.md na raiz
usar caminhos absolutos em Markdown
duplicar documentos da mesma issue
mover README ou CHANGELOG sem autorização
misturar documentação de frontend e backend
realizar commit ou push sem solicitação explícita
```

---

## Validação antes de finalizar

Executar, quando aplicável:

```bash
find frontend backend -maxdepth 1 -type f \
  \( -name "implementation_plan*.md" -o -name "walkthrough*.md" \)
```

O resultado esperado é vazio.

Verificar caminhos absolutos:

```bash
grep -R "/home/" docs --include="*.md"
```

Verificar duplicatas aproximadas:

```bash
find docs -type f -name "*.md" | sort
```

Apresentar no relatório final os arquivos criados, atualizados ou movidos.
