# Plano de Implementação - Revisão Final e Release Frontend MVP (Issue #037)

Executar a revisão final do frontend MVP do GTH Agents, validar todo o escopo funcional e técnico, e documentar os procedimentos necessários para a publicação da release `v1.0.0-mvp-frontend`.

## User Review Required

> [!IMPORTANT]
> - Esta issue é focada estritamente em revisão, validação, documentação e versionamento. Nenhuma funcionalidade nova ou alteração nas regras de negócio/contratos do backend deve ser introduzida.
> - A criação da tag Git `v1.0.0-mvp-frontend` não deve ser executada automaticamente pelo assistente. O plano detalha as instruções de criação para que o usuário execute manualmente após aprovação e merge na branch principal.
> - Todos os caminhos de arquivos nos documentos versionados serão estritamente relativos ao monorepo (por exemplo, `frontend/README.md`, `docs/frontend/walkthroughs/...`), sem qualquer referência a caminhos locais absolutos do sistema do desenvolvedor.

## Proposed Changes

Como esta é uma versão de revisão técnica e de documentação, os arquivos a serem criados ou modificados destina-se a atualizar a documentação operacional, estrutural e técnica do frontend MVP.

### Documentação Técnica e Operacional

#### [NEW] `docs/frontend/implementation-plans/implementation_plan_issue_037_release_frontend_mvp.md`
* Plano de implementação detalhando os passos de validação funcional, verificação técnica, testes em ambiente Docker e geração de documentação de release.

#### [NEW] `docs/frontend/walkthroughs/walkthrough_issue_037_release_frontend_mvp.md`
* Relatório final de validação contendo o resultado dos testes, comandos executados, evidências coletadas e decisões de release.

#### [NEW] `docs/scratchpads/issue-037-frontend-release-validation.md`
* Scratchpad contendo a lista exata de todos os cenários de teste manuais e o status de aprovação detalhado de cada um deles. O scratchpad registrará cada cenário com perfil, rota, resultado esperado, resultado observado, status e observações.

#### [MODIFY] `frontend/README.md`
* Atualização completa do README do frontend para refletir os pré-requisitos, instruções de desenvolvimento, instruções de build, execução com Docker dev/prod, variáveis de ambiente reais utilizadas (`VITE_API_URL`), estrutura de diretórios e tratamento de rotas internas no Nginx.

#### [MODIFY] `frontend/.env.example`
* Garantir que a variável `VITE_API_URL` esteja devidamente documentada no arquivo de exemplo de variáveis de ambiente do frontend.

### Configurações de Infraestrutura (Validação e Ajustes se Necessários)

#### [VERIFY/MODIFY IF NEEDED] `frontend/nginx.conf`
* Confirmar que o Nginx está configurado com fallback para React Router usando `try_files $uri $uri/ /index.html;` (ou equivalente funcional como `try_files $uri /index.html;`), garantindo reload direto de rotas internas sem erro 404.

#### [VERIFY] `frontend/Dockerfile.prod`
* Confirmar que a imagem de produção executa o build estático do React/Vite e serve o conteúdo via Nginx.

#### [VERIFY] `frontend/Dockerfile.dev`
* Confirmar que o ambiente de desenvolvimento executa o Vite na porta esperada e com host compatível com Docker.

#### [VERIFY] `docker-compose.yml`
* Confirmar que os serviços `api`, `web` e `db` estão configurados corretamente para desenvolvimento integrado.

---

## Verification Plan

### Automated Tests
- Executar e registrar os resultados de:
  ```bash
  cd frontend
  npm install
  npm run lint
  npm run build
  ```
- Executar `docker compose config` na raiz para validar os arquivos de configuração do Docker Compose.

### Docker Image and Services Execution Validation
- Subir os containers de desenvolvimento na raiz do monorepo:
  ```bash
  docker compose up --build
  ```
- Validar se os serviços sobem corretamente:
  ```bash
  docker compose ps
  curl -i http://localhost:5000/health
  curl -I http://localhost:5173
  ```
- Construir a imagem Docker de produção:
  ```bash
  cd frontend
  docker build -f Dockerfile.prod -t gth-agents-web:prod .
  ```
- Executar o container de produção standalone:
  ```bash
  docker run --rm -p 8080:80 gth-agents-web:prod
  ```
- Validar acesso via comando na raiz e nas rotas internas no container de produção standalone:
  ```bash
  curl -I http://localhost:8080
  curl -I http://localhost:8080/dashboard
  curl -I http://localhost:8080/colaboradores
  curl -I http://localhost:8080/pdis
  curl -I http://localhost:8080/feedbacks
  curl -I http://localhost:8080/reconhecimentos
  ```

### Manual and Nginx Routing Fallback Validation
- Utilizar o navegador para testar de ponta a ponta todos os cenários funcionais especificados no scratchpad.
- Validar o reload de rotas internas no container de produção (`http://localhost:8080`) para garantir que o fallback no Nginx impeça erros 404.
- No scratchpad `docs/scratchpads/issue-037-frontend-release-validation.md`, utilizar os status padronizados:
  * `APROVADO`
  * `REPROVADO`
  * `NÃO VALIDADO`
  * `BLOQUEADO`
  * `VALIDADO POR INSPEÇÃO`

### Sensitive Data Audit
- Executar na raiz do monorepo:
  ```bash
  git status --short
  git ls-files | grep -E '(^|/)\.env$'
  git status --short | grep -Ei 'token|senha|password|secret|\.env$'
  git diff --cached --name-only
  git diff --cached | grep -Ei 'token|senha|password|secret|access_token|refresh_token|Authorization|Bearer'
  ```
- Confirmar que nenhum arquivo `.env` real, token, senha ou segredo esteja incluído na documentação ou nos arquivos preparados para commit.
