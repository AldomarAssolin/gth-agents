# Walkthrough — Checklist de Ambiente Demo (Issue #081)

Este documento registra a entrega documental e as validações técnicas realizadas para a **Issue #081**, visando a criação de um guia reproduzível e seguro de preparação de ambiente de demonstração controlado para o GTH Agents.

---

## Resumo da implementação

Foi estruturado o checklist de provisionamento para ambiente de demonstração controlado da plataforma GTH Agents. O checklist define a separação entre ambientes (local, demo e produção), pré-requisitos, variáveis de ambiente seguras com placeholders, isolamento de banco de dados, checagens operacionais pós-deploy e procedimentos básicos de backup e restauração.

---

## Arquivos criados e alterados

Todos os arquivos da Issue #081 estão localizados em `docs/deploy/`:

- [Plano de implementação](implementation_plan_issue_081_demo_environment_checklist.md) — Plano revisado e auditado.
- [Checklist do ambiente demo](checklist_demo_environment.md) — Checklist técnico contendo as seções obrigatórias.
- [Walkthrough da Issue #081](walkthrough_issue_081_demo_environment_checklist.md) — Registro final da entrega e das validações realizadas.

---

## Fontes inspecionadas

Para garantir a coerência dos comandos e variáveis descritos no checklist, as seguintes fontes do repositório foram inspecionadas:
- `docker-compose.yml` (raiz) — Verificação das portas padrão (`5000` API, `5173` Web dev, `5432` DB) e volumes persistentes (`postgres_data`).
- `backend/Dockerfile` — Verificação do comando de inicialização Flask.
- `frontend/Dockerfile.prod` e `nginx.conf` — Verificação da compilação estática do React e suporte a SPA no Nginx na porta `80`.
- `backend/seed_db.py` — Auditoria do comportamento de carga e deleção de dados.
- `backend/app.py` — Inspeção da lógica de interceptação e checagem de CORS.
- `backend/interface/routes/health_routes.py` — Verificação do payload retornado pelo endpoint `/health`.
- `backend/migrations/` — Confirmação do uso do Alembic para migrations.

---

## Decisões técnicas e lacunas identificadas

1. **Bloqueio do seed atual**: O arquivo `backend/seed_db.py` realiza remoções diretas de registros e carrega dados estáticos de desenvolvimento. O checklist não recomenda sua execução em ambiente demo persistente. Sua utilização somente seria aceitável em uma base explicitamente descartável, com confirmação de que o banco pode ser completamente recriado. Foi registrada como melhoria futura a criação de um `backend/seed_demo.py` parametrizável, não destrutivo por padrão e adequado à demonstração.
2. **Classificação do Health Check**: O `/health` foi classificado estritamente como **liveness básica** da API Flask, explicando-se no checklist que ele não garante a conectividade do banco de dados de forma isolada.
3. **CORS restritivo**: Exigência de declaração exata da origem na variável `CORS_ORIGINS`, vedando explicitamente o uso de wildcard `*`.
4. **Isolamento do DB**: Instrução no checklist para remover o mapeamento de portas públicas externas para a base PostgreSQL, mantendo o tráfego restrito à rede interna de containers.
5. **Lacuna Docker**: Identificou-se que não existe composição Docker Compose específica para o build de produção (com o frontend empacotado no Nginx). O checklist documenta essa lacuna e trata o `docker-compose.yml` existente como infraestrutura local de desenvolvimento. A criação de uma composição demo será tratada em issue futura.

---

## Comandos validados e sua classificação

Abaixo consta a classificação dos comandos descritos na documentação, divididos conforme o nível de execução e teste realizado nesta issue:

### 1. Comandos efetivamente executados

Os seguintes comandos foram executados localmente durante esta issue:

- `find docs/deploy -maxdepth 1 -type f | sort`
  Confirmou a presença dos três documentos da Issue #081.

- `grep -R -n -E "/home/|/Users/|C:\\\\Users\\\\" docs/deploy/ --include="*.md"`
  Não identificou caminhos absolutos locais nos documentos finais (a correspondência encontrada foi na própria linha de instrução de busca no plano de implementação).

- `grep -R -n -E "admin123|dev-secret-change-me|postgres:postgres|Bearer [A-Za-z0-9._-]+" docs/deploy/ --include="*.md"`
  As correspondências encontradas foram revisadas contextualmente:
  * `docs/deploy/checklist_demo_environment.md:19` (menção técnica para substituição do segredo `dev-secret-change-me`).
  * `docs/deploy/implementation_plan_issue_081_demo_environment_checklist.md:178` (registro do comando de auditoria em si).
  * `docs/deploy/walkthrough_issue_081_demo_environment_checklist.md:53` (registro do comando de auditoria no walkthrough).
  Nenhum segredo real, token válido ou credencial operacional foi identificado. Valores conhecidos de desenvolvimento aparecem apenas como exemplos de padrões proibidos ou alertas técnicos, nunca como credenciais recomendadas.

- `docker compose config`
  Validou a sintaxe e a resolução da composição Docker de desenvolvimento existente.

- `git diff --check`
  Não identificou erros de whitespace no diff, como espaços no final das linhas.

- `grep -n "^## " docs/deploy/checklist_demo_environment.md`
  Listou os títulos de segundo nível. A saída foi revisada para confirmar a presença e a sequência das 20 seções previstas no escopo da Issue #081. Adicionalmente, o comando `grep -c "^## " docs/deploy/checklist_demo_environment.md` confirmou a contagem de `20` seções.

- `PYTHONPATH=. .venv/bin/pytest`
  Executado em `backend/`, com 208 testes aprovados.

- `npm run lint`
  Executado em `frontend/`, sem erros reportados pelas regras configuradas no projeto.

- `npm run build`
  Executado em `frontend/`, gerando o build de produção sem erros.

---

### 2. Comandos apenas confirmados no repositório

Esses comandos foram considerados compatíveis com a estrutura atual do repositório por inspeção dos arquivos e configurações, mas não foram executados nesta issue:
- `docker compose build` e `docker compose up -d` (pilha de containers de desenvolvimento).
- `docker compose ps` e `docker compose logs` (monitoramento de containers).
- `docker compose exec api alembic upgrade head` e `alembic current` (atualização e checagem de migrations no container).
- `curl http://localhost:5000/health` — comando compatível com a rota encontrada no backend, mas não executado nesta issue. O endpoint `GET /health` e o payload esperado foram confirmados por inspeção do código-fonte em `backend/interface/routes/health_routes.py`. Como não houve requisição real nesta tarefa, nenhuma resposta HTTP foi declarada como validada.

---

### 3. Exemplos genéricos não executados

Esses comandos e procedimentos foram documentados apenas como modelos genéricos e não foram validados contra infraestrutura externa:
- Geração de backup local/remoto via `pg_dump`.
- Restauração de backup via `pg_restore` (incluindo testes em container temporário).
- Configuração de domínio e mapeamentos DNS no arquivo `/etc/hosts` local.
- Configuração de Proxy Reverso, roteamento Nginx e instalação de certificados TLS/HTTPS.
- Ações de rollback de código ou infraestrutura cloud.

---

## Resultado consolidado das validações

```text
Documentos da Issue #081: 3 arquivos confirmados
Backend: 208 testes aprovados
Frontend lint: aprovado
Frontend build: aprovado
Docker Compose config: aprovado
git diff --check: aprovado
Caminhos absolutos locais: não identificados
Segredos reais ou tokens válidos: não identificados
Deploy externo: não realizado
Backup e restauração: não executados
Proxy reverso e TLS: não configurados
```

---

## Conclusão

A Issue #081 foi concluída dentro de seu escopo documental.

Foram entregues o plano revisado, o checklist técnico e este walkthrough. As validações locais e documentais previstas foram executadas, incluindo a suíte completa do backend, lint e build do frontend, validação do Docker Compose e inspeções contra caminhos locais e dados sensíveis.

O checklist está pronto para orientar uma futura preparação controlada de ambiente demo.

Nenhum ambiente externo foi provisionado, nenhum deploy efetivo foi realizado e os procedimentos genéricos de backup, restauração, proxy reverso, TLS e rollback não foram executados nesta issue.
