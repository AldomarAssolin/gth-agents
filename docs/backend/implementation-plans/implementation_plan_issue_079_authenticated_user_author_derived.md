# Plano de Implementação — Issue #079 — Derivar Autoria do Usuário Autenticado

Este plano visa ajustar o backend do GTH Agents para que todos os campos de autoria, criação, registro e cancelamento sejam definidos exclusivamente a partir do usuário autenticado no JWT, mitigando o risco de falsificação de autoria (spoofing).

## 1. Matriz de Fluxos de Autoria Encontrados

| Módulo | Endpoint | Operação | Campo de Autoria | Origem Atual | Origem Final | Arquivos Envolvidos |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Avaliações** | `POST /avaliacoes` | Criar Avaliação | `avaliador_id` | Payload | `g.usuario["id"]` | `backend/interface/routes/avaliacoes_routes.py`<br>`backend/interface/schemas/avaliacao_schema.py` |
| **Metas** | `POST /metas` | Criar Meta | `criado_por_id` | Payload | `g.usuario["id"]` | `backend/interface/routes/metas_routes.py`<br>`backend/interface/schemas/meta_schema.py` |
| **Feedbacks** | `POST /feedbacks` | Registrar Feedback | `autor_id` | Payload | `g.usuario["id"]` | `backend/interface/routes/feedbacks_routes.py`<br>`backend/interface/schemas/feedback_schema.py` |
| **PDI** | `POST /pdis` | Criar PDI | `criado_por_id` | JWT (na rota) | `g.usuario["id"]` | `backend/interface/routes/pdis_routes.py`<br>`backend/interface/schemas/pdi_schema.py` |
| **Reconhecimentos** | `POST /reconhecimentos` | Criar Reconhecimento | `registrado_por_id` | JWT (na rota) | `g.usuario["id"]` | `backend/interface/routes/reconhecimentos_routes.py`<br>`backend/interface/schemas/reconhecimento_schema.py` |
| **Reconhecimentos** | `PATCH /reconhecimentos/<id>/cancelar` | Cancelar Reconhecimento | `cancelado_por_id` | JWT (na rota) | `g.usuario["id"]` | `backend/interface/routes/reconhecimentos_routes.py`<br>`backend/interface/schemas/reconhecimento_schema.py` |
| **AçãoPDI** | Vários | Todas | N/A | Não aplicável | Não aplicável | `AcaoPDIModel` não possui campos de autoria própria. |

## 2. Fonte de Autoria e Mecanismo de Autenticação

A fonte de autoria mapeada e validada no backend será o ID do usuário autenticado no request context: **`g.usuario["id"]`**.

* **Preenchimento de `g.usuario`:** O dicionário `g.usuario` é preenchido pelo middleware de autenticação (`auth_middleware.py`) que decodifica o token JWT presente no cabeçalho `Authorization: Bearer <token>`.
* **Acesso ao Banco de Dados:** Durante a execução do middleware de autenticação, **não** há consulta ao banco de dados para recuperar o usuário. A consulta para validação de existência e permissões do usuário ocorre na camada de casos de uso (Use Cases) e serviços da aplicação (ex: `self.usuarios_repo.get_by_id(dto.avaliador_id)`).
* **Validações Atuais do JWT:** O middleware chama o `JWTService.decodificar_token(token)` que, por sua vez, delega para a biblioteca PyJWT. Esta biblioteca valida a assinatura do token contra a chave `JWT_SECRET_KEY` e valida a expiração do token (claim `exp`). Caso o token esteja expirado ou com assinatura inválida, são lançadas as exceções `ExpiredSignatureError` ou `InvalidTokenError`, retornando HTTP `401 Unauthorized` para o cliente.

## 3. Estratégia Única de Compatibilidade e Schemas

A estratégia escolhida é a **Estratégia Transitória** aplicada de forma consistente em todos os módulos:
- O backend continuará aceitando temporariamente os campos de autoria no payload das requisições para compatibilidade.
- No entanto, os schemas e rotas receberão a autoria como argumento separado do payload e ignorarão completamente qualquer valor enviado no payload.

As chamadas de schema serão ajustadas da seguinte forma:
```python
parse_registrar_avaliacao(data, avaliador_id=authenticated_user_id)
parse_criar_meta(data, criado_por_id=authenticated_user_id)
parse_registrar_feedback(data, autor_id=authenticated_user_id)
```
Qualquer valor enviado para estes campos de autoria no JSON original é explicitamente ignorado e nunca utilizado na construção do DTO correspondente.

## 4. Entidades sem Autoria Própria
Como as ações de PDI (`AcaoPDI`) não possuem campos de autoria próprios em sua tabela/entidade, nenhuma autoria fictícia ou campo paralelo será criado para as ações. Isso é tratado explicitamente como **não aplicável**.

## 5. Testes de Segurança e Regressão

Será criado o arquivo `backend/tests/test_issue_079_spoofing.py` contendo:

### A. Testes de Correção de Segurança (Avaliações, Metas e Feedbacks)
- **Criação sem campo de autoria no payload:** Garante que a operação funciona com sucesso mesmo se o cliente não enviar o campo de autoria, derivando-o do JWT.
- **Envio de ID de outro usuário existente (Spoofing):** Envia um ID de usuário válido e diferente no payload e valida que o backend o ignora, persistindo a autoria correta.
- **Envio de ID de usuário inexistente (Spoofing):** Envia um ID inexistente no payload (ex: `99999`) e garante que o backend não valide ou tente usá-lo, persistindo com sucesso a autoria do JWT do usuário autenticado.
- **Persistência do usuário autenticado:** Valida que o ID persistido no banco de dados corresponde exatamente ao usuário associado ao JWT, afirmando:
  ```python
  assert registro.autoria_id == usuario_autenticado.id
  assert registro.autoria_id != autoria_enviada_no_payload
  ```
- **Manutenção de perfil e escopo:** Garante que as regras restritivas do `AccessScopeService` baseadas no perfil autenticado continuam em vigor.
- **HTTP 401 sem autenticação:** Valida que chamadas sem token falham com status `401`.
- **HTTP 403 fora do perfil ou escopo:** Valida que usuários com perfis insuficientes ou sem escopo sobre o colaborador recebem status `403`.

### B. Testes de Regressão e Consistência (PDI e Reconhecimentos)
- **Cenários de consistência da derivação:** Validar que tentativas de spoofing de `criado_por_id` em PDI, `registrado_por_id` em criação de reconhecimento, e `cancelado_por_id` no cancelamento de reconhecimento falham/são ignoradas, e que o ID do JWT autenticado é o único persistido.
- **Validação de erros de escopo e autenticação:** HTTP 401 e 403 para esses módulos.

## 6. Impacto no Frontend

Com base na inspeção, os seguintes arquivos do frontend enviam campos de autoria:
* `avaliador_id`: Enviado por `frontend/src/features/avaliacoes/AvaliacaoForm.jsx` (linha 103)
* `autor_id`: Enviado por `frontend/src/pages/NovoFeedbackPage.jsx` (linha 119)
* `criado_por_id`: Enviado por `frontend/src/pages/NovaMetaPage.jsx` (linha 117)
* `registrado_por_id`: Nenhum arquivo envia.
* `cancelado_por_id`: Nenhum arquivo envia.

**Estratégia Técnica:**
O frontend atual deverá permanecer compatível, pois os campos já enviados continuarão sendo aceitos pelo backend, embora seus valores sejam ignorados.

## 7. Pendências Futuras
- Mapeado no backlog futuro a necessidade de remoção de `avaliador_id`, `autor_id` e `criado_por_id` dos payloads enviados pelo frontend.

## 8. Riscos e Itens Fora do Escopo
- **Risco de consistência de estado do usuário:** O middleware de token JWT não realiza consultas ao banco de dados a cada requisição. Portanto, se o perfil de um usuário for alterado ou se o usuário for desativado no banco de dados, essas alterações podem não se refletir imediatamente nas requisições cujo token já tenha sido emitido e ainda seja válido.

## 9. Baseline da Suíte de Testes (Antes da Implementação)

* **Comando executado:** `PYTHONPATH=. .venv/bin/pytest` dentro da pasta `backend/`
* **Quantidade de testes coletados:** 126
* **Quantidade aprovada:** 126
* **Falhas existentes:** 0
* **Duração:** 62.38 segundos

## 10. Detalhamento de Arquivos e Dependências

### Arquivos a Modificar
* `backend/interface/routes/avaliacoes_routes.py`
* `backend/interface/schemas/avaliacao_schema.py`
* `backend/interface/routes/metas_routes.py`
* `backend/interface/schemas/meta_schema.py`
* `backend/interface/routes/feedbacks_routes.py`
* `backend/interface/schemas/feedback_schema.py`

### Arquivos Novos
* `backend/tests/test_issue_079_spoofing.py` (Suíte de testes de segurança de autoria)
* `docs/backend/walkthroughs/walkthrough_issue_079_authenticated_user_author_derived.md` (Documentação pós-implementação)

### Schemas e DTOs Afetados
* `parse_registrar_avaliacao` (`avaliacao_schema.py`): Modificado para receber `avaliador_id: int` e ignorar o payload.
* `parse_criar_meta` (`meta_schema.py`): Modificado para receber `criado_por_id: int` e ignorar o payload.
* `parse_registrar_feedback` (`feedback_schema.py`): Modificado para receber `autor_id: int` e ignorar o payload.

### Testes Afetados
* Nenhum teste existente será quebrado, pois a compatibilidade transitória garante que o recebimento de payloads legados continue funcionando.

### Necessidade de Migration
* **Nenhuma migration é necessária**, pois as colunas estruturais necessárias já existem na persistência atual.
