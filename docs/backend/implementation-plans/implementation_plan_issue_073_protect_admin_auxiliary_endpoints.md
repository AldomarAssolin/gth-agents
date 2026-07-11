# Plano de Implementação — Proteger Endpoints Administrativos de Cadastros Auxiliares (Issue #073)

Auditar e corrigir a autenticação e a autorização dos endpoints de cadastros auxiliares (setores, funções, usuários, competências) no backend do GTH Agents, garantindo que operações administrativas sejam restritas diretamente no backend pelo JWT e que respostas de usuários não expõem campos sensíveis como `senha_hash`.

## Auditoria e Mapeamento de Rotas

Após análise técnica do frontend, confirmamos que:
1. As listagens gerais (`GET /setores`, `GET /funcoes`, `GET /competencias`) são consumidas por formulários operacionais e listagem de colaboradores por usuários com perfil `LIDER` e `COLABORADOR`. Portanto, devem permanecer acessíveis a qualquer usuário autenticado (`@auth_required`).
2. Os endpoints de obtenção individual (`GET /setores/{id}`, `GET /funcoes/{id}`, `GET /competencias/{id}`) **não são consumidos** pelo frontend em fluxos operacionais ou administrativos comuns. Como são puramente administrativos, eles serão restritos exclusivamente a `ADMIN/RH`.
3. O decorator `@roles_required` já encapsula a validação de presença e assinatura de token JWT internamente ao chamar `obter_usuario_da_requisicao()`. Portanto, rotas que utilizam `@roles_required` **não necessitam** ser combinadas com `@auth_required`. Caso o token seja ausente ou inválido, o decorator retorna HTTP `401`. Se o perfil for insuficiente, retorna HTTP `403`.

## Proposed Changes

### Interface de Rotas

---

#### [MODIFY] [cadastros_routes.py](../../../../backend/interface/routes/cadastros_routes.py)

- Importar `auth_required` de `interface.middlewares.auth_middleware`.
- Aplicar os decorators de autenticação e autorização conforme a matriz abaixo:

| Recurso     | Operação  | Método | Endpoint real                  | Proteção atual                | Perfis necessários | Ação                          |
| :---------- | :-------- | :----: | :----------------------------- | :---------------------------- | :----------------- | :---------------------------- |
| Setor       | Listar    |  GET   | `/setores`                     | Nenhuma (Pública)             | Autenticado        | Adicionar `@auth_required`    |
| Setor       | Obter     |  GET   | `/setores/<int:id>`            | Nenhuma (Pública)             | ADMIN, RH          | Adicionar `@roles_required("ADMIN", "RH")` |
| Setor       | Criar     |  POST  | `/setores`                     | `@roles_required("ADMIN", "RH")` | ADMIN, RH          | Auditar e Manter proteção     |
| Setor       | Atualizar |  PUT   | `/setores/<int:id>`            | Nenhuma (Pública)             | ADMIN, RH          | Adicionar `@roles_required("ADMIN", "RH")` |
| Setor       | Ativar    | PATCH  | `/setores/<int:id>/ativar`     | Nenhuma (Pública)             | ADMIN, RH          | Adicionar `@roles_required("ADMIN", "RH")` |
| Setor       | Desativar | PATCH  | `/setores/<int:id>/desativar`  | Nenhuma (Pública)             | ADMIN, RH          | Adicionar `@roles_required("ADMIN", "RH")` |
| Função      | Listar    |  GET   | `/funcoes`                     | Nenhuma (Pública)             | Autenticado        | Adicionar `@auth_required`    |
| Função      | Obter     |  GET   | `/funcoes/<int:id>`            | Nenhuma (Pública)             | ADMIN, RH          | Adicionar `@roles_required("ADMIN", "RH")` |
| Função      | Criar     |  POST  | `/funcoes`                     | `@roles_required("ADMIN", "RH")` | ADMIN, RH          | Auditar e Manter proteção     |
| Função      | Atualizar |  PUT   | `/funcoes/<int:id>`            | Nenhuma (Pública)             | ADMIN, RH          | Adicionar `@roles_required("ADMIN", "RH")` |
| Função      | Ativar    | PATCH  | `/funcoes/<int:id>/ativar`     | Nenhuma (Pública)             | ADMIN, RH          | Adicionar `@roles_required("ADMIN", "RH")` |
| Função      | Desativar | PATCH  | `/funcoes/<int:id>/desativar`  | Nenhuma (Pública)             | ADMIN, RH          | Adicionar `@roles_required("ADMIN", "RH")` |
| Usuário     | Listar    |  GET   | `/usuarios`                    | Nenhuma (Pública)             | ADMIN, RH          | Adicionar `@roles_required("ADMIN", "RH")` |
| Usuário     | Obter     |  GET   | `/usuarios/<int:id>`           | Nenhuma (Pública)             | ADMIN, RH          | Adicionar `@roles_required("ADMIN", "RH")` |
| Usuário     | Criar     |  POST  | `/usuarios`                    | `@roles_required("ADMIN", "RH")` | ADMIN, RH          | Auditar e Manter proteção     |
| Usuário     | Atualizar |  PUT   | `/usuarios/<int:id>`           | Nenhuma (Pública)             | ADMIN, RH          | Adicionar `@roles_required("ADMIN", "RH")` |
| Usuário     | Ativar    | PATCH  | `/usuarios/<int:id>/ativar`    | Nenhuma (Pública)             | ADMIN, RH          | Adicionar `@roles_required("ADMIN", "RH")` |
| Usuário     | Desativar | PATCH  | `/usuarios/<int:id>/desativar` | Nenhuma (Pública)             | ADMIN, RH          | Adicionar `@roles_required("ADMIN", "RH")` |
| Competência | Listar    |  GET   | `/competencias`                | Nenhuma (Pública)             | Autenticado        | Adicionar `@auth_required`    |
| Competência | Obter     |  GET   | `/competencias/<int:id>`       | Nenhuma (Pública)             | ADMIN, RH          | Adicionar `@roles_required("ADMIN", "RH")` |
| Competência | Criar     |  POST  | `/competencias`                | `@roles_required("ADMIN", "RH")` | ADMIN, RH          | Auditar e Manter proteção     |
| Competência | Atualizar |  PUT   | `/competencias/<int:id>`       | Nenhuma (Pública)             | ADMIN, RH          | Adicionar `@roles_required("ADMIN", "RH")` |
| Competência | Ativar    | PATCH  | `/competencias/<int:id>/ativar`| Nenhuma (Pública)             | ADMIN, RH          | Adicionar `@roles_required("ADMIN", "RH")` |
| Competência | Desativar | PATCH  | `/competencias/<int:id>/desativar`| Nenhuma (Pública)          | ADMIN, RH          | Adicionar `@roles_required("ADMIN", "RH")` |

---

### Testes Automatizados

#### [NEW] [test_issue_073_admin_auxiliary_endpoints_security.py](../../../../backend/tests/test_issue_073_admin_auxiliary_endpoints_security.py)

- **Testes Parametrizados**: Implementar testes parametrizados com `pytest.mark.parametrize` cobrindo todas as 24 rotas contra:
  - **Sem JWT**: Retorno HTTP `401`.
  - **Perfis proibidos (`COLABORADOR` ou `LIDER`) nas rotas administrativas**: Retorno HTTP `403`.
  - **Perfis autorizados (`ADMIN` e `RH`)**: Execução bem-sucedida.
- **Teste de Mitigação de Spoofing**: Validar que o perfil considerado pelo backend para autorização é estritamente derivado do token JWT decodificado, não se confundindo com campos de `perfil` eventualmente enviados no JSON payload (por exemplo, na criação ou atualização de outro usuário).
- **Teste de Persistência**: Verificar que após chamadas administrativas negadas (HTTP `403`), nenhuma alteração de estado é efetuada no banco de dados.
- **Teste de Serialização de Usuário**: Garantir que as rotas de usuários (criação, listagem, atualização, etc.) não expõem campos confidenciais como `senha` ou `senha_hash`.
- **Teste de Regressão Operacional**: Garantir que os fluxos de listagem (`GET /setores`, `GET /funcoes`, `GET /competencias`) permanecem acessíveis aos perfis `LIDER` e `COLABORADOR`.

## Documentação Técnica do Fechamento

Prever a criação do walkthrough em:
[walkthrough_issue_073_protect_admin_auxiliary_endpoints.md](../../walkthroughs/walkthrough_issue_073_protect_admin_auxiliary_endpoints.md)

## Verification Plan

### Automated Tests
- Executar os novos testes parametrizados e específicos de segurança:
  ```bash
  cd backend
  PYTHONPATH=. .venv/bin/pytest tests/test_issue_073_admin_auxiliary_endpoints_security.py
  ```
- Garantir a aprovação da suíte completa de testes existentes:
  ```bash
  PYTHONPATH=. .venv/bin/pytest
  ```

### Manual Verification
- Elaborar um Scratchpad de Validação Manual em:
  `docs/scratchpads/issue-073-admin-auxiliary-endpoints-manual-validation.md`
  com os cenários solicitados, marcando o status como `AGUARDANDO VALIDAÇÃO HUMANA`.
