# Plano de Implementação Final - Cadastros Auxiliares (Issue #039)

Este plano descreve o design e as etapas de implementação para o módulo de **Cadastros Auxiliares** no frontend do **GTH Agents**. O objetivo é permitir que usuários com perfil de `ADMIN` ou `RH` gerenciem os cadastros base do sistema: setores, funções, usuários e competências.

---

## Mapeamento e Proteção de Endpoints no Backend

Os endpoints abaixo em [cadastros_routes.py](../../../backend/interface/routes/cadastros_routes.py) possuem as seguintes decorações e regras de segurança reais no backend:

| Entidade | Método e URL | Decorator / Proteção Real | Perfis Autorizados | Payload Aceito |
| :--- | :--- | :--- | :--- | :--- |
| **Setor** | `GET /setores` | Sem decorator de auth | Todos (sem restrição na API) | N/A |
| **Setor** | `POST /setores` | `@roles_required("ADMIN", "RH")` | `ADMIN`, `RH` | `{"nome": str, "descricao": str}` |
| **Setor** | `PUT /setores/<id>` | Sem decorator de auth | Todos (sem restrição na API) | `{"nome": str, "descricao": str}` |
| **Setor** | `PATCH /setores/<id>/ativar` | Sem decorator de auth | Todos (sem restrição na API) | N/A |
| **Setor** | `PATCH /setores/<id>/desativar` | Sem decorator de auth | Todos (sem restrição na API) | N/A |
| **Função** | `GET /funcoes` | Sem decorator de auth | Todos (sem restrição na API) | N/A |
| **Função** | `POST /funcoes` | `@roles_required("ADMIN", "RH")` | `ADMIN`, `RH` | `{"nome": str, "descricao": str}` |
| **Função** | `PUT /funcoes/<id>` | Sem decorator de auth | Todos (sem restrição na API) | `{"nome": str, "descricao": str}` |
| **Função** | `PATCH /funcoes/<id>/ativar` | Sem decorator de auth | Todos (sem restrição na API) | N/A |
| **Função** | `PATCH /funcoes/<id>/desativar` | Sem decorator de auth | Todos (sem restrição na API) | N/A |
| **Usuário** | `GET /usuarios` | Sem decorator de auth | Todos (sem restrição na API) | N/A |
| **Usuário** | `POST /usuarios` | `@roles_required("ADMIN", "RH")` | `ADMIN`, `RH` | `{"nome": str, "email": str, "senha": str, "perfil": str, "colaborador_id": int/null, "setor_id": int/null}` |
| **Usuário** | `PUT /usuarios/<id>` | Sem decorator de auth | Todos (sem restrição na API) | `{"nome": str, "email": str, "senha": str (opcional), "perfil": str (opcional), "colaborador_id": int/null, "setor_id": int/null}` |
| **Usuário** | `PATCH /usuarios/<id>/ativar` | Sem decorator de auth | Todos (sem restrição na API) | N/A |
| **Usuário** | `PATCH /usuarios/<id>/desativar` | Sem decorator de auth | Todos (sem restrição na API) | N/A |
| **Competência**| `GET /competencias` | Sem decorator de auth | Todos (sem restrição na API) | N/A |
| **Competência**| `POST /competencias` | `@roles_required("ADMIN", "RH")` | `ADMIN`, `RH` | `{"nome": str, "tipo": str, "descricao": str, "peso": float}` |
| **Competência**| `PUT /competencias/<id>`| Sem decorator de auth | Todos (sem restrição na API) | `{"nome": str, "tipo": str, "descricao": str, "peso": float}` |
| **Competência**| `PATCH /competencias/<id>/ativar` | Sem decorator de auth | Todos (sem restrição na API) | N/A |
| **Competência**| `PATCH /competencias/<id>/desativar`| Sem decorator de auth | Todos (sem restrição na API) | N/A |

---

## Riscos Técnicos Identificados

> [!WARNING]
> **Ausência de Autenticação/Autorização no Backend**:
> Identificamos que vários endpoints administrativos cruciais (especialmente `GET`, `PUT` e as rotas de `PATCH /ativar` e `PATCH /desativar`) estão sem decorators explícitos de autenticação (`@auth_required`) ou autorização (`@roles_required`) no backend. Isso significa que, do ponto de vista de rede, a API permite consultas e modificações desses registros por qualquer agente de rede.
> 
> **Mitigação e Escopo**:
> 1. O frontend aplicará proteção visual estrita nas rotas `/configuracoes/*` para garantir que apenas perfis `ADMIN` e `RH` iniciem essas requisições no fluxo de uso regular.
> 2. A ausência de autenticação do lado do servidor nas rotas identificadas será registrada no walkthrough como uma sugestão de correção futura para a camada de backend, sem alteração de código backend nesta issue, seguindo a diretriz de não interferência no backend.

---

## Diretrizes de Implementação

> [!NOTE]
> O frontend aplica proteção visual para impedir acessos via interface regular por perfis não autorizados.

### 1. Escopo Funcional (Listagem/Criação Obrigatórias vs Edição/Alteração de Status Condicionais)
* **Obrigatório**: A listagem e a criação de todos os quatro recursos (setores, funções, usuários e competências) são obrigatórias e serão implementadas em suas respectivas telas.
* **Condicional**: As operações de edição (`PUT`), ativação e desativação (`PATCH`) serão implementadas nos formulários/tabelas apenas se permanecerem simples, seguras e reutilizáveis (ex. reaproveitando o formulário de criação com suporte a props de preenchimento de dados originais). Caso sua implementação agregue complexidade excessiva, elas serão omitidas no frontend e listadas como melhorias futuras no walkthrough final.

### 2. Regras de Senha no Formulário de Usuários
* **Segurança Estrita**: Nunca renderizar, registrar no console/logs ou documentar senhas reais.
* **Submissão com Erro**: Se a submissão do formulário falhar, manter os dados dos campos não sensíveis (`nome`, `email`, `perfil`, `colaborador_id`, `setor_id`) preenchidos para evitar redigitação, mas **limpar sempre** o campo `senha`.
* **Submissão com Sucesso**: Limpar o formulário inteiro (incluindo senha e demais campos) após a criação bem-sucedida.
* **Edição de Usuário (se implementada)**: Ao editar um usuário existente, o campo `senha` será enviado no payload do `PUT` **apenas se for explicitamente preenchido** pelo usuário. Se estiver em branco ou vazio no formulário, a propriedade `senha` será omitida do payload enviado, evitando sobreescrever a senha existente com valores nulos ou strings vazias no backend.

### 3. Proteção Visual das Rotas no Frontend
* **Proteção Completa**: Além de ocultar o link de "Configurações" na Sidebar, todas as rotas associadas (`/configuracoes`, `/configuracoes/setores`, `/configuracoes/funcoes`, `/configuracoes/usuarios`, `/configuracoes/competencias`) validarão o perfil do usuário logo no carregamento.
* Se o usuário logado possuir perfil `LIDER` ou `COLABORADOR`, a página correspondente renderizará um componente padrão de "Acesso Negado" com `<ErrorMessage title="Acesso Negado" message="Você não possui permissão para acessar esta página de configurações." />` e um botão para retornar ao Dashboard.

### 4. Integração com Colaboradores no Formulário de Usuários
* O select de colaboradores no `UsuarioForm` consumirá a função `listarColaboradores()` do `colaboradoresService` existente, que já está estável e mapeado no projeto. 
* Caso ocorra qualquer instabilidade ou erro inesperado de rede nos testes desse catálogo, adotaremos um campo numérico simples controlado (`Input type="number"`) como fallback opcional para a entrada direta do ID do colaborador, documentando a melhoria do select como pendência.

### 5. Reutilização Inteligente e DRY (Don't Repeat Yourself)
* Para evitar duplicação excessiva nas páginas administrativas de listagem/formulário sem criar componentes genéricos excessivamente complexos e difíceis de dar manutenção:
  * Utilizaremos componentes simples compartilhados de badges para os dados repetitivos (ex. `StatusAtivoBadge`).
  * As quatro telas e seus respectivos formulários serão independentes, porém estruturados com o mesmo padrão visual, facilitando a legibilidade direta do código de cada funcionalidade.

---

## Proposed Changes

### 1. Rotas e Sidebar

#### [MODIFY] [AppRoutes.jsx](../../../frontend/src/routes/AppRoutes.jsx)
* Adicionar as novas rotas filhas de configurações protegidas:
  * `/configuracoes/setores` -> `<SetoresPage />`
  * `/configuracoes/funcoes` -> `<FuncoesPage />`
  * `/configuracoes/usuarios` -> `<UsuariosPage />`
  * `/configuracoes/competencias` -> `<CompetenciasPage />`

#### [MODIFY] [Sidebar.jsx](../../../frontend/src/components/layout/Sidebar.jsx)
* Filtrar condicionalmente o item "Configurações" para exibir apenas a perfis `ADMIN` e `RH`.

---

### 2. Services e Tratamento de Erro

#### [NEW] [setoresService.js](../../../frontend/src/features/configuracoes/setoresService.js)
#### [NEW] [funcoesService.js](../../../frontend/src/features/configuracoes/funcoesService.js)
#### [NEW] [usuariosService.js](../../../frontend/src/features/configuracoes/usuariosService.js)
#### [NEW] [competenciasService.js](../../../frontend/src/features/configuracoes/competenciasService.js)
#### [NEW] [configuracoesErrors.js](../../../frontend/src/features/configuracoes/configuracoesErrors.js)
* Tratamento centralizado de erros da API para o módulo de configurações (mapeamento amigável de HTTP 400, 403, 404, 409, 500 e rede).

---

### 3. Componentes de Interface (Features)

#### [NEW] [StatusAtivoBadge.jsx](../../../frontend/src/features/configuracoes/StatusAtivoBadge.jsx)
#### [NEW] [PerfilUsuarioBadge.jsx](../../../frontend/src/features/configuracoes/PerfilUsuarioBadge.jsx)
#### [NEW] [TipoCompetenciaBadge.jsx](../../../frontend/src/features/configuracoes/TipoCompetenciaBadge.jsx)
#### [NEW] [SetorForm.jsx](../../../frontend/src/features/configuracoes/SetorForm.jsx)
#### [NEW] [FuncaoForm.jsx](../../../frontend/src/features/configuracoes/FuncaoForm.jsx)
#### [NEW] [UsuarioForm.jsx](../../../frontend/src/features/configuracoes/UsuarioForm.jsx)
* Preserva os inputs não sensíveis em falha de submissão, limpa sempre o campo de senha.
#### [NEW] [CompetenciaForm.jsx](../../../frontend/src/features/configuracoes/CompetenciaForm.jsx)

---

### 4. Páginas (Pages)

#### [MODIFY] [ConfiguracoesPage.jsx](../../../frontend/src/pages/ConfiguracoesPage.jsx)
* Painel administrativo com grid de cards para cada cadastro auxiliar, com validação de permissão.

#### [NEW] [SetoresPage.jsx](../../../frontend/src/pages/SetoresPage.jsx)
#### [NEW] [FuncoesPage.jsx](../../../frontend/src/pages/FuncoesPage.jsx)
#### [NEW] [UsuariosPage.jsx](../../../frontend/src/pages/UsuariosPage.jsx)
#### [NEW] [CompetenciasPage.jsx](../../../frontend/src/pages/CompetenciasPage.jsx)

---

## Entregas e Documentos Previstos

* **Plano de Implementação**: [implementation_plan_issue_039_cadastros_auxiliares.md](../../../docs/frontend/implementation-plans/implementation_plan_issue_039_cadastros_auxiliares.md)
* **Walkthrough de Entrega**: [walkthrough_issue_039_cadastros_auxiliares.md](../../../docs/frontend/walkthroughs/walkthrough_issue_039_cadastros_auxiliares.md)
* **Scratchpad de Validação Manual**: [issue-039-cadastros-auxiliares-manual-validation.md](../../../docs/scratchpads/issue-039-cadastros-auxiliares-manual-validation.md)

---

## Verification Plan

### Automated Tests
1. **Linting de código do frontend**:
   ```bash
   cd frontend && npm run lint
   ```
2. **Build de produção do frontend**:
   ```bash
   cd frontend && npm run build
   ```
3. **Validação do Docker Compose**:
   ```bash
   docker compose config
   ```

### Manual Verification
O fluxo de teste manual no navegador focará nos seguintes pontos:
1. **Bloqueio Visual de Acesso**:
   - Tentar acessar `/configuracoes` e sub-rotas com perfil `LIDER` ou `COLABORADOR`. O sistema exibirá a tela de Acesso Negado no frontend.
2. **Retorno HTTP 403 do Servidor**:
   - Simular ou disparar uma requisição `POST` aos endpoints protegidos sem perfil `ADMIN`/`RH`, verificando que o servidor retorna `403 Forbidden` e o frontend lida de forma graciosa via `<ErrorMessage />` sem quebrar o fluxo.
3. **Criação e Listagem de Recursos**:
   - Criação com sucesso de Setor, Função, Usuário (com limpeza de senha) e Competência (com validações de peso).
   - Preservação de dados não sensíveis em erros de validação da API (ex: 409 conflito).
