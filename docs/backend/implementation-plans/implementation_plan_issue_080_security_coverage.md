# Plano de Implementação — Cobertura de Segurança de Autoria e Autorização (Issue #080)

Este plano detalha a estratégia de implementação de testes de segurança para garantir a integridade dos mecanismos de autoria e autorização (perfil e escopo) no backend do GTH Agents. O foco é cobrir todas as operações dos módulos operacionais (Avaliações, Metas, Feedbacks, PDI, Reconhecimentos) e relatórios/visualizações (Listagens, Evolução e Dashboard).

## 1. Auditoria e Matrizes de Referência

### A. Matriz Real de Autorização (Perfil e Escopo)

A tabela abaixo resume as regras vigentes de segurança no backend para os módulos abrangidos:

| Recurso / Operação | Método | Rota | Perfis Permitidos | Regras de Escopo (LIDER e COLABORADOR) |
| :--- | :---: | :--- | :--- | :--- |
| **Avaliação** / Criar | `POST` | `/avaliacoes` | `ADMIN`, `RH`, `LIDER` | LIDER só pode criar para colaboradores do mesmo setor. |
| **Meta** / Criar | `POST` | `/metas` | `ADMIN`, `RH`, `LIDER` | LIDER só pode criar para colaboradores do mesmo setor. |
| **Meta** / Listar do Colaborador | `GET` | `/colaboradores/<int:id>/metas` | Todos | LIDER (mesmo setor), COLABORADOR (próprio ID). |
| **Feedback** / Criar | `POST` | `/feedbacks` | `ADMIN`, `RH`, `LIDER` | LIDER só pode criar para colaboradores do mesmo setor. |
| **Feedback** / Estruturar | `POST` | `/feedbacks/estruturar` | `ADMIN`, `RH`, `LIDER` | Sem validação de colaborador (apenas IA). |
| **PDI** / Criar | `POST` | `/pdis` | `ADMIN`, `RH`, `LIDER` | LIDER só pode criar para colaboradores do mesmo setor. |
| **PDI** / Listar Geral | `GET` | `/pdis` | Todos | LIDER vê apenas do setor; COLABORADOR vê apenas os próprios. |
| **PDI** / Obter Individual | `GET` | `/pdis/<int:pdi_id>` | Todos | LIDER (mesmo setor), COLABORADOR (próprio ID). |
| **PDI** / Atualizar | `PATCH` | `/pdis/<int:pdi_id>` | `ADMIN`, `RH`, `LIDER` | LIDER só pode gerenciar se colaborador for do mesmo setor. |
| **PDI** / Concluir | `PATCH` | `/pdis/<int:pdi_id>/concluir` | `ADMIN`, `RH`, `LIDER` | LIDER só pode gerenciar se colaborador for do mesmo setor. |
| **PDI** / Cancelar | `PATCH` | `/pdis/<int:pdi_id>/cancelar` | `ADMIN`, `RH`, `LIDER` | LIDER só pode gerenciar se colaborador for do mesmo setor. |
| **PDI** / Listar do Colaborador | `GET` | `/colaboradores/<int:id>/pdis` | Todos | LIDER (mesmo setor), COLABORADOR (próprio ID). |
| **Ação PDI** / Criar | `POST` | `/pdis/<int:pdi_id>/acoes` | `ADMIN`, `RH`, `LIDER` | LIDER só pode gerenciar se colaborador for do mesmo setor. |
| **Ação PDI** / Listar | `GET` | `/pdis/<int:pdi_id>/acoes` | Todos | LIDER (mesmo setor), COLABORADOR (próprio ID). |
| **Ação PDI** / Atualizar | `PATCH` | `/pdis/<int:pdi_id>/acoes/<int:acao_id>` | `ADMIN`, `RH`, `LIDER` | LIDER só pode gerenciar se colaborador for do mesmo setor. |
| **Ação PDI** / Concluir | `PATCH` | `/pdis/<int:pdi_id>/acoes/<int:acao_id>/concluir` | `ADMIN`, `RH`, `LIDER` | LIDER só pode gerenciar se colaborador for do mesmo setor. |
| **Ação PDI** / Cancelar | `PATCH` | `/pdis/<int:pdi_id>/acoes/<int:acao_id>/cancelar` | `ADMIN`, `RH`, `LIDER` | LIDER só pode gerenciar se colaborador for do mesmo setor. |
| **Reconhecimento** / Criar | `POST` | `/reconhecimentos` | `ADMIN`, `RH`, `LIDER` | LIDER só pode criar para colaboradores do mesmo setor. |
| **Reconhecimento** / Listar Geral | `GET` | `/reconhecimentos` | Todos | LIDER vê apenas do setor; COLABORADOR vê apenas os próprios. |
| **Reconhecimento** / Obter Individual | `GET` | `/reconhecimentos/<int:id>` | Todos | LIDER (mesmo setor), COLABORADOR (próprio ID). |
| **Reconhecimento** / Cancelar | `PATCH` | `/reconhecimentos/<int:id>/cancelar` | `ADMIN`, `RH`, `LIDER` | LIDER só pode gerenciar se colaborador for do mesmo setor. |
| **Reconhecimento** / Listar do Colab | `GET` | `/colaboradores/<int:id>/reconhecimentos` | Todos | LIDER (mesmo setor), COLABORADOR (próprio ID). |
| **Evolução** / Obter | `GET` | `/colaboradores/<int:id>/evolucao` | Todos | LIDER (mesmo setor), COLABORADOR (próprio ID). |
| **Dashboard** / Consultar MVP | `GET` | `/dashboard/mvp` | `ADMIN`, `RH`, `LIDER` | LIDER vê agregados do setor; COLABORADOR não tem acesso. |

### B. Mapeamento de Persistência de Autoria

Os seguintes campos de autoria são extraídos estritamente de `g.usuario["id"]` e persistidos nas tabelas correspondentes:

| Módulo | Operação | Entidade / Modelo | Campo de Autoria | Tipo de Validação / Substituição |
| :--- | :--- | :--- | :--- | :--- |
| **Avaliações** | Criar Avaliação | `AvaliacaoModel` | `avaliador_id` | Ignora payload e injeta `g.usuario["id"]` |
| **Metas** | Criar Meta | `MetaModel` | `criado_por_id` | Ignora payload e injeta `g.usuario["id"]` |
| **Feedbacks** | Registrar Feedback | `FeedbackModel` | `autor_id` | Ignora payload e injeta `g.usuario["id"]` |
| **PDI** | Criar PDI | `PDIModel` | `criado_por_id` | Injetado diretamente a partir de `g.usuario["id"]` |
| **Reconhecimentos** | Criar Reconhecimento | `ReconhecimentoModel` | `registrado_por_id` | Injetado diretamente a partir de `g.usuario["id"]` |
| **Reconhecimentos** | Cancelar Reconhecimento | `ReconhecimentoModel` | `cancelado_por_id` | Injetado diretamente a partir de `g.usuario["id"]` |

---

## 2. Estratégia de Testes

### A. Testes Existentes e Reutilização
* **`test_access_scope.py`**: Mantido intacto. Cobre o escopo do CRUD básico de Colaboradores.
* **`test_issue_073_admin_auxiliary_endpoints_security.py`**: Mantido intacto. Cobre rotas de Cadastros Auxiliares (Setores, Funções, Usuários, Competências).
* **`test_issue_079_spoofing.py`**: Mantido intacto. Validou a implementação inicial da autoria a partir de JWT para os endpoints de criação.
* **`test_evolucao_colaborador.py` & `test_dashboard_mvp.py`**: Mantidos intactos. Validam a lógica operacional.

### B. Novo Arquivo de Testes: `test_issue_080_security_coverage.py`
Para garantir a cobertura de segurança exigida sem duplicar desnecessariamente testes focados em regras de negócio, criaremos uma suíte centralizada baseada em cenários de ataque, autenticação e vazamento de dados.

## 2.C. Coberturas complementares obrigatórias

Além dos cenários anteriores, a suíte deve validar:

1. acesso permitido do `COLABORADOR` aos próprios recursos;
2. bloqueio do `COLABORADOR` ao acessar recursos de outro colaborador;
3. integridade entre `pdi_id` e `acao_id`;
4. ausência de persistência para todos os módulos de escrita abrangidos;
5. operações representativas executadas com `RH`;
6. identidade exata dos registros retornados nas listagens, e não apenas a quantidade;
7. contagens, listas recentes e alertas do dashboard dentro do escopo;
8. separação do endpoint `/feedbacks/estruturar`, que possui autorização por perfil, mas não escopo de colaborador.

Os cenários já integralmente cobertos pela Issue #079 não devem ser duplicados sem necessidade. A nova suíte deve complementar a cobertura com combinações de perfil, escopo, persistência e vazamento de dados.

#### Cenários Cobertos:
1. **HTTP 401 sem autenticação (Parametrizado)**:
   - Valida que todas as rotas operacionais (POST `/avaliacoes`, POST `/metas`, GET `/colaboradores/<id>/metas`, POST `/feedbacks`, POST `/feedbacks/estruturar`, POST `/pdis`, GET `/pdis`, GET `/pdis/<id>`, PATCH `/pdis/<id>`, PATCH `/pdis/<id>/concluir`, PATCH `/pdis/<id>/cancelar`, GET `/colaboradores/<id>/pdis`, POST `/pdis/<id>/acoes`, GET `/pdis/<id>/acoes`, PATCH `/pdis/<id>/acoes/<id>`, PATCH `/pdis/<id>/acoes/<id>/concluir`, PATCH `/pdis/<id>/acoes/<id>/cancelar`, POST `/reconhecimentos`, GET `/reconhecimentos`, GET `/reconhecimentos/<id>`, PATCH `/reconhecimentos/<id>/cancelar`, GET `/colaboradores/<id>/reconhecimentos`, GET `/colaboradores/<id>/evolucao`, GET `/dashboard/mvp`) retornam `401 Unauthorized` quando chamadas sem token JWT.
2. **HTTP 403 por perfil insuficiente**:
   - Valida que um usuário com perfil `COLABORADOR` recebe `403 Forbidden` nas rotas exclusivas para liderança/admin (ex: criar metas, avaliações, feedbacks, pdis, gerenciar ações, cancelar reconhecimentos, acessar dashboard).
3. **HTTP 403 fora do escopo (Líder Cruzado)**:
   - `LIDER A` (Setor 1) tenta gerenciar/cadastrar recursos (Avaliação, Meta, Feedback, PDI, Reconhecimento) de `Colaborador B` (Setor 2) -> `403 Forbidden`.
   - `LIDER A` tenta listar/ler recursos individuais (PDI individual, metas do colaborador, reconhecimentos do colaborador, evolução) de `Colaborador B` -> `403 Forbidden`.
4. **Acesso Permitido para Perfil e Escopo Válidos**:
   - `LIDER A` gerencia `Colaborador A` (mesmo setor) -> `200` ou `201`.
   - `ADMIN` e `RH` gerenciam qualquer colaborador -> `200` ou `201`.
5. **Autoria e Spoofing Ignorado**:
   - Tenta enviar payload com ID de autoria falsificado (ex: `LIDER A` envia `LIDER B` ou `99999` nos campos `avaliador_id`, `criado_por_id`, `autor_id`, `registrado_por_id`, `cancelado_por_id`).
   - Garante que a operação conclui com sucesso, mas o ID persistido no banco de dados corresponde estritamente ao usuário autenticado (`LIDER A`).
6. **Ausência de persistência ou alteração após bloqueio**:
   - Ao receber `403` em tentativas de criação de metas, pdis ou alteração de estado (ex: concluir/cancelar PDI, cancelar reconhecimento), valida que nenhuma entrada foi adicionada ao banco e nenhum atributo foi modificado.
7. **Prevenção de vazamento entre escopos em listagens agregadas**:
   - `/pdis` (Listar): LIDER A recebe apenas os PDIs dos colaboradores do seu setor (Setor 1). COLABORADOR A recebe apenas seus próprios PDIs.
   - `/reconhecimentos` (Listar): LIDER A recebe apenas os reconhecimentos dos colaboradores do seu setor. COLABORADOR A recebe apenas os próprios.
   - `/dashboard/mvp`: LIDER A recebe dados estatísticos e agregações contendo apenas colaboradores do Setor 1.

---

## 3. Plano de Validação

### Testes Automatizados
Execução focada na nova suite e na suite completa para regressão:
```bash
cd backend
# Rodar teste específico
PYTHONPATH=. .venv/bin/pytest -v tests/test_issue_080_security_coverage.py

# Rodar suíte completa
PYTHONPATH=. .venv/bin/pytest -v
```

### Validação Estática
```bash
git diff --check
git status --short
```

## 4. Documentação

Criar ou atualizar:

- `docs/backend/implementation-plans/implementation_plan_issue_080_security_coverage.md`
- `docs/backend/walkthroughs/walkthrough_issue_080_security_coverage.md`

Caso os testes revelem falha real de segurança, registrar o problem e não declarar a issue concluída até que a decisão de correção seja tomada.
