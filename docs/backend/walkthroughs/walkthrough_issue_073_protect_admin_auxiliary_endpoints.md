# Walkthrough — Proteger Endpoints Administrativos de Cadastros Auxiliares (Issue #073)

Este walkthrough documenta a implementação do escopo definido para a Issue #073, referente à autenticação e à autorização dos endpoints de setores, funções, usuários e competências.

A correção garante que a autorização seja determinada pelo usuário autenticado via JWT, e não por estados visuais do frontend ou informações controladas pelo cliente.

## Alterações realizadas

### Backend

#### `backend/interface/routes/cadastros_routes.py`

Foram auditadas as 24 rotas do módulo de cadastros auxiliares.

As alterações realizadas foram:

* aplicação de `@auth_required` às rotas de listagem operacional;
* aplicação de `@roles_required("ADMIN", "RH")` às rotas administrativas anteriormente desprotegidas;
* manutenção e validação dos decorators já existentes nas rotas de criação;
* preservação das listagens operacionais necessárias aos fluxos de colaboradores e avaliações.

### Matriz final de acesso

| Categoria               | Endpoints                                                                       | Perfis autorizados           |
| ----------------------- | ------------------------------------------------------------------------------- | ---------------------------- |
| Listagens operacionais  | `GET /setores`, `GET /funcoes`, `GET /competencias`                             | Qualquer usuário autenticado |
| Consultas individuais   | `GET /setores/{id}`, `GET /funcoes/{id}`, `GET /competencias/{id}`              | `ADMIN`, `RH`                |
| Rotas de usuários       | Listagem, consulta, criação, atualização, ativação e desativação                | `ADMIN`, `RH`                |
| Manutenção de cadastros | Criação, atualização, ativação e desativação de setores, funções e competências | `ADMIN`, `RH`                |

A separação entre leitura operacional e manutenção administrativa preserva os fluxos legítimos do sistema sem deixar operações de escrita acessíveis a perfis indevidos.

### Testes automatizados

#### `backend/tests/test_issue_073_admin_auxiliary_endpoints_security.py`

Foi criada uma suíte específica de segurança cobrindo:

* autenticação nas 24 rotas auditadas;
* retorno HTTP `401` para requisições sem token ou com token inválido;
* retorno HTTP `403` para `LIDER` e `COLABORADOR` nas rotas administrativas;
* acesso autorizado para `ADMIN` e `RH`;
* uso exclusivo do perfil proveniente do JWT para autorização;
* distinção entre o perfil do solicitante e o campo `perfil` de um usuário administrado;
* ausência de persistência após operações negadas;
* ausência dos campos `senha` e `senha_hash` nas respostas de usuários abrangidas pelos testes;
* manutenção do acesso de `LIDER` e `COLABORADOR` às listagens operacionais necessárias.

Os testes de atualização, ativação e desativação utilizam registros previamente preparados no banco de teste, evitando que respostas `404` ocultem o comportamento real da autorização.

## Resultados dos testes

### Suíte específica da Issue #073

Comando executado:

```bash
cd backend
PYTHONPATH=. .venv/bin/pytest \
  tests/test_issue_073_admin_auxiliary_endpoints_security.py
```

Resultado:

```text
28 passed in 57.32s
```

A suíte específica coletou e aprovou 28 testes, incluindo cenários parametrizados de autenticação e autorização e verificações específicas de persistência, serialização e regressão operacional.

### Suíte completa do backend

Comando executado:

```bash
PYTHONPATH=. .venv/bin/pytest
```

Resultado:

```text
159 passed in 121.94s
```

A suíte completa aprovou 159 testes, sem falhas nos testes existentes.

## Documentação

Foram criados ou atualizados:

```text
docs/backend/implementation-plans/
implementation_plan_issue_073_protect_admin_auxiliary_endpoints.md

docs/backend/walkthroughs/
walkthrough_issue_073_protect_admin_auxiliary_endpoints.md

docs/scratchpads/
issue-073-admin-auxiliary-endpoints-manual-validation.md
```

## Validação manual

Os cenários funcionais foram executados pelo homologador humano e registrados no Scratchpad.

Foram validados manualmente:

- retorno `401` para requisições sem token;
- retorno `403` para operações administrativas executadas por perfil insuficiente;
- operações administrativas autorizadas com perfil `ADMIN`;
- comportamento administrativo do perfil `RH` coberto pelos testes automatizados;
- proteção contra tentativa de elevação de privilégio por payload;
- ausência de `senha` e `senha_hash` nas respostas verificadas;
- manutenção das listagens operacionais para os perfis previstos.

A ausência de alterações após requisições proibidas foi validada por consulta direta ao banco ou, quando indicado no Scratchpad, pelos testes automatizados de persistência.
```text
Status: VALIDAÇÃO HUMANA CONCLUÍDA
```

[Validação manual](../../scratchpads/issue-073-admin-auxiliary-endpoints-manual-validation.md)

## Resultado técnico

A implementação, os testes automatizados e a validação manual da Issue #073 foram concluídos.

Os endpoints abrangidos pela issue agora exigem autenticação e autorização de acordo com a matriz definida. As listagens operacionais necessárias permanecem disponíveis aos usuários autenticados, enquanto consultas individuais e operações de manutenção administrativa ficam restritas aos perfis `ADMIN` e `RH`.

As tentativas de elevação de privilégio pelo payload foram rejeitadas com HTTP `403`, sem criação do registro indevido no banco. As respostas de usuários verificadas não expuseram os campos `senha` ou `senha_hash`.

```text
Status final: ISSUE VALIDADA
