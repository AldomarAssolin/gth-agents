# Plano de Implementação - ISSUE #77: Reorganizar READMEs e Posicionamento do GTH Agents

## Objetivo
Reorganizar a documentação principal do repositório (**GTH Agents**) para refletir o estado atual do sistema como uma plataforma modular de Gestão do Talento Humano orientada a dados. As alterações visam unificar o tom do repositório, destacar os pilares de negócio do sistema (Desempenho, Desenvolvimento, Saúde Organizacional e Analytics), estruturar os READMEs do backend e do frontend com informações técnicas reais e detalhadas, além de estabelecer um roadmap evolutivo consistente.

Não haverá alterações funcionais de backend, frontend ou regras de negócio. Esta issue é puramente documental e narrativa.

---

## Estado Atual Encontrado e Arquivos Analisados
Foram inspecionadas detalhadamente as seguintes áreas do projeto:

### 1. Backend:
* **Entidades de Domínio (`backend/domain/entities/`)**: Entidades de negócio puro, como colaborador, metas, pdi, feedbacks, reconhecimentos, avaliações, competências, etc.
* **Enums de Domínio (`backend/domain/enums/`)**:
  * Perfis de usuário reais: `PerfilUsuario` com valores técnicos: `ADMIN`, `RH`, `LIDER`, `COLABORADOR` (definidos em `backend/domain/enums/perfil_usuario.py`).
  * Enums de status e prioridades (ex: `prioridade_meta.py`, `status_meta.py`, `pdi_enums.py`, `tipo_reconhecimento.py`).
* **Casos de Uso (`backend/application/use_cases/`)**: Regras de negócio da aplicação (ex: `criar_meta_uc`, `evolucao_colaborador_uc`, `pdi_uc`, `reconhecimento_uc`).
* **Modelos SQLAlchemy e Repositórios (`backend/infrastructure/database/models/`)**: Persistência e Unit of Work localizados em `infrastructure/`.
* **Rotas e Controladores (`backend/interface/routes/`)**: Endpoints expostos pelo Flask:
  * `health_routes.py` -> `GET /health`
  * `auth_routes.py` -> `POST /auth/login`
  * `dashboard_routes.py` -> `GET /dashboard/mvp`
  * `colaboradores_routes.py` -> `GET /colaboradores`, `POST /colaboradores`, `GET /colaboradores/<int:id>`, `PUT /colaboradores/<int:id>`, `GET /colaboradores/<int:colaborador_id>/perfil`, `GET /colaboradores/<int:id>/evolucao`, `GET /colaboradores/<int:id>/metas`
  * `avaliacoes_routes.py` -> `POST /avaliacoes`
  * `metas_routes.py` -> `POST /metas`
  * `feedbacks_routes.py` -> `POST /feedbacks`, `POST /feedbacks/estruturar`
  * `pdis_routes.py` -> `POST /pdis`, `GET /pdis`, `GET /pdis/<int:pdi_id>`, `GET /colaboradores/<int:colaborador_id>/pdis`, `POST /pdis/<int:pdi_id>/acoes`, `GET /pdis/<int:pdi_id>/acoes`
  * `reconhecimentos_routes.py` -> `POST /reconhecimentos`, `GET /reconhecimentos`, `GET /reconhecimentos/<int:reconhecimento_id>`, `GET /colaboradores/<int:colaborador_id>/reconhecimentos`
  * `cadastros_routes.py` -> CRUDs de `/setores`, `/funcoes`, `/usuarios`, e `/competencias`
* **Configuração e Dependências (`backend/requirements.txt`, `backend/app.py`, `backend/seed_db.py`, `backend/alembic.ini`)**: Configurações de banco, CORS, injeção de dependências e ambiente de desenvolvimento.

### 2. Frontend:
* **Features (`frontend/src/features/`)**: Módulos React de negócio, incluindo:
  * `auth/`: `AuthContext`, `useAuth`, `LoginForm`, `PrivateRoute`, `authService.js`, `authStorage.js`
  * `colaboradores/`: listagens, detalhes, erros, helpers e services.
  * `metas/`, `pdis/`, `feedbacks/`, `reconhecimentos/`, `avaliacoes/`, `dashboard/`, `evolucao/` e `configuracoes/`.
* **Roteamento (`frontend/src/routes/AppRoutes.jsx`)**: Definição e proteção de rotas privadas do React Router.
* **Componentes de UI Reutilizáveis (`frontend/src/components/ui/`)**: `Badge`, `Button`, `Card`, `EmptyState`, `ErrorMessage`, `Input`, `Loading`, `Select`, `Table`.
* **Configurações e Docker (`frontend/package.json`, `frontend/Dockerfile.dev`, `frontend/Dockerfile.prod`, `frontend/nginx.conf`)**:
  * Verificado que o arquivo `frontend/nginx.conf` existe e implementa o fallback SPA usando a diretiva `try_files $uri $uri/ /index.html;`.
  * Verificado o suporte Docker standalone.

### 3. Problemas identificados na documentação atual:
1. O README da raiz é muito curto e não contextualiza a proposta de valor do GTH Agents nem seus pilares estratégicos de negócio.
2. O backend README não detalha a Clean Architecture de forma clara, nem descreve a estrutura real das entidades de domínio e escopos de acesso. Adicionalmente, utiliza nomenclaturas de perfis inconsistentes com o código.
3. O frontend README carece de detalhes sobre as rotas reais, tratamento de 401/403 no cliente Axios e proteção de rota SPA.
4. Não há clareza entre o que já está desenvolvido (MVP) e o que faz parte do roadmap futuro do produto (Saúde Organizacional, Analytics).

---

## Estratégia de Reorganização e Nova Estrutura

### README da Raiz (README.md)
O README raiz será reestruturado para focar na visão de produto e no monorepo de alto nível, cobrindo:
1. **Visão Geral**
2. **Problema que o Projeto Resolve**
3. **Proposta de Valor**
4. **Pilares do Sistema** (Desempenho, Desenvolvimento, Saúde Organizacional [Roadmap], Analytics [Roadmap])
5. **Módulos Implementados** (Cadastro, Colaboradores, Avaliações, Competências, Perfil de Talento, Metas, PDI, Feedbacks, Reconhecimentos, Evolução do Colaborador, Dashboard, Autenticação)
6. **Roadmap do GTH Agents** (Detalhamento das fases v1.0, v1.x, v1.1, v1.2, v2.0)
7. **Arquitetura Geral do Monorepo**
8. **Stack Principal**
9. **Como Executar com Docker**
10. **Estrutura do Repositório**
11. **Documentação Técnica** (links para os READMEs internos)
12. **Status Atual**
13. **Observações de Segurança**

### README do Backend (backend/README.md)
Será voltado para a manutenção e compreensão técnica da API Flask:
1. **Visão Geral**
2. **Stack Técnica**
3. **Clean Architecture** (detalhamento das camadas Domain, Application, Infrastructure, Interface)
4. **Módulos e Endpoints Reais** (apenas rotas existentes confirmadas no código)
5. **Autenticação e Autorização** (JWT, RBAC com perfis reais: `ADMIN`, `RH`, `LIDER`, `COLABORADOR`)
6. **Controle de Escopo** (detalhes da lógica de isolamento por setor do gestor e auto-acesso)
7. **Banco de Dados e Migrations** (Alembic)
8. **Testes** (pytest)
9. **Execução Local**
10. **Execução com Docker**
11. **Health Check**
12. **Variáveis de Ambiente**
13. **Convenções Técnicas**

### README do Frontend (frontend/README.md)
Será focado no desenvolvimento da aplicação React/Vite:
1. **Visão Geral**
2. **Stack Técnica**
3. **Estrutura de Pastas**
4. **Organização por Features**
5. **Rotas Principais**
6. **Autenticação** (AuthContext, useAuth, PrivateRoute)
7. **Integração com API** (Serviços Axios e tratamento correto de endpoints)
8. **Tratamento de Erros e Estados**
9. **Componentes Reutilizáveis UI**
10. **Padrões de Tela**
11. **Execução Local**
12. **Execução com Docker**
13. **Build de Produção e Suporte SPA no Nginx** (referenciando o arquivo `frontend/nginx.conf` existente)
14. **Convenções Técnicas**

---

## O que Ficará Fora de Escopo
- Alterações em códigos-fonte executáveis do backend ou frontend.
- Alterações em dependências nos arquivos `requirements.txt` ou `package.json`.
- Criação de novas tabelas ou migrações do banco de dados.

---

## Critérios de Aceite e Escopo de Entrega
A entrega da issue #77 será considerada pronta quando:
1. O README raiz (`README.md`), o README do backend (`backend/README.md`) e o README do frontend (`frontend/README.md`) estiverem reestruturados conforme planejado.
2. A visão por pilares estiver clara e diferenciada entre módulos implementados e futuros (roadmap).
3. Saúde Organizacional e Analytics estiverem documentados estritamente como roadmap futuro.
4. Os perfis técnicos reais (`ADMIN`, `RH`, `LIDER`, `COLABORADOR`) forem utilizados na documentação.
5. Os endpoints listados forem exatamente correspondentes às rotas Flask implementadas.
6. Criação de toda a documentação da issue no diretório `docs/project/`:
   - `docs/project/implementation-plans/implementation_plan_issue_077_readmes_posicionamento.md` (Este documento)
   - `docs/project/walkthroughs/walkthrough_issue_077_readmes_posicionamento.md` (Relatório de walkthrough ao final)
7. Nenhuma menção a IA generativa para os módulos atuais do MVP for incluída (agentes atuais são descritos como deterministicos baseados em regras de negócio).
8. As validações obrigatórias especificadas forem executadas com sucesso.

---

## Validações Planejadas
Como a issue é exclusivamente de documentação, as validações obrigatórias são:
1. **`git diff --check`**: validação de espaços em branco e formatação no commit.
2. **`git status --short`**: verificação de que apenas os arquivos de documentação e READMEs planejados foram criados/alterados.
3. **Inspeção de links relativos**: validação manual de que os links nos markdowns apontam para caminhos válidos do monorepo.
4. **Busca por caminhos absolutos**: verificação automatizada com `grep` para garantir a ausência de caminhos locais (ex: `/home/`).
5. **Busca por segredos ou credenciais reais**: busca manual/automatizada para impedir a publicação de secrets, senhas ou tokens.
