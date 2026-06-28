# Scratchpad de Validação Manual - Release Frontend MVP (Issue #037)

Este documento define os cenários de teste específicos para a validação ponta a ponta do frontend MVP do GTH Agents.

---

## Matriz de Validação Funcional

### Cenário 1: Login de Usuário
* **Perfil Utilizado:** Administrador (`admin@test.com` / `admin123`)
* **Rota Testada:** `/login`
* **Resultado Esperado:** Autenticar com sucesso via API, salvar token no local storage/cookie, redirecionar para `/dashboard` com saudação e informações do perfil do usuário.
* **Resultado Observado:** Login realizado com sucesso. O sistema salvou as credenciais de sessão e redirecionou para `/dashboard` exibindo a saudação "Olá, Admin User!".
* **Status:** APROVADO
* **Evidência:** `![Validação Completa](../frontend/videos/issue_037_validacao_mvp_completa.webp)`
* **Observações:** O tempo de resposta da autenticação foi imediato.

---

### Cenário 2: Logout de Usuário
* **Perfil Utilizado:** Administrador (`admin@test.com`)
* **Rota Testada:** `/dashboard`
* **Resultado Esperado:** Clicar no botão "Sair", remover o token do local storage/cookie, e redirecionar imediatamente para a tela de `/login`.
* **Resultado Observado:** Ao clicar em "Sair", o token de autenticação foi limpo e o redirecionamento para `/login` ocorreu instantaneamente.
* **Status:** APROVADO
* **Evidência:** `![Validação Completa](../frontend/videos/issue_037_validacao_mvp_completa.webp)`
* **Observações:** Nenhuma informação residual de sessão permaneceu no estado da aplicação.

---

### Cenário 3: Proteção de Rotas Privadas
* **Perfil Utilizado:** Não autenticado
* **Rota Testada:** `/dashboard`, `/colaboradores`, `/metas`, `/pdis`, `/configuracoes`
* **Resultado Esperado:** Ao tentar acessar diretamente qualquer rota privada sem autenticação ativa, ser redirecionado automaticamente para a página de `/login`.
* **Resultado Observado:** O middleware de rotas privadas interceptou o acesso não autenticado e redirecionou para `/login`.
* **Status:** APROVADO
* **Evidência:** `![Validação Completa](../frontend/videos/issue_037_validacao_mvp_completa.webp)`
* **Observações:** A proteção cobre todas as sub-rotas criadas.

---

### Cenário 4: Dashboard com Dados Reais
* **Perfil Utilizado:** Administrador (`admin@test.com`)
* **Rota Testada:** `/dashboard`
* **Resultado Esperado:** A página carrega e exibe informações de estatísticas gerais retornadas pelo endpoint `/dashboard/mvp` (Colaboradores ativos, metas pendentes/em andamento, etc.) sem simulação de dados local e sem erros.
* **Resultado Observado:** Os cartões do Dashboard carregaram dados reais retornados pela API (ex: 2 colaboradores, metas e PDIs ativos).
* **Status:** APROVADO
* **Evidência:** `![Validação Completa](../frontend/videos/issue_037_validacao_mvp_completa.webp)`
* **Observações:** O endpoint `/dashboard/mvp` respondeu com status 200.

---

### Cenário 5: Listagem de Colaboradores
* **Perfil Utilizado:** Administrador (`admin@test.com`)
* **Rota Testada:** `/colaboradores`
* **Resultado Esperado:** Exibir listagem com os colaboradores cadastrados no banco de dados (ex: Colaborador A, Colaborador B) com colunas de matrícula, setor, função e status ativo.
* **Resultado Observado:** Exibição correta da tabela contendo "Colaborador A (Engenharia)" e "Colaborador B (Marketing)".
* **Status:** APROVADO
* **Evidência:** `![Validação Completa](../frontend/videos/issue_037_validacao_mvp_completa.webp)`
* **Observações:** Tabela com suporte a rolagem lateral no mobile.

---

### Cenário 6: Consulta de Colaborador (Detalhes)
* **Perfil Utilizado:** Administrador (`admin@test.com`)
* **Rota Testada:** `/colaboradores/10` (ID do Colaborador A)
* **Resultado Esperado:** Carregar as informações específicas do Colaborador A com nome, matrícula, email, admissão, setor e função.
* **Resultado Observado:** Carregamento correto de todos os dados do Colaborador A na página de detalhes.
* **Status:** APROVADO
* **Evidência:** `![Validação Completa](../frontend/videos/issue_037_validacao_mvp_completa.webp)`
* **Observações:** ID dinâmico recuperado da URL de forma correta.

---

### Cenário 7: Evolução do Colaborador
* **Perfil Utilizado:** Administrador (`admin@test.com`)
* **Rota Testada:** `/colaboradores/10/evolucao`
* **Resultado Esperado:** Exibir a página de evolução contendo o histórico de avaliações, resumo de metas, PDIs, feedbacks e reconhecimentos do Colaborador A.
* **Resultado Observado:** A tela carregou o histórico completo do Colaborador A integrado com a API Flask.
* **Status:** APROVADO
* **Evidência:** `![Validação Completa](../frontend/videos/issue_037_validacao_mvp_completa.webp)`
* **Observações:** Aba de linha do tempo e listagens integradas perfeitamente.

---

### Cenário 8: Registro de Nova Avaliação
* **Perfil Utilizado:** Administrador (`admin@test.com`)
* **Rota Testada:** `/avaliacoes/nova`
* **Resultado Esperado:** Preencher o formulário de avaliação para um colaborador, selecionar notas/comentários e submeter com sucesso à API.
* **Resultado Observado:** Formulário preenchido e submetido para o Colaborador B. Criação realizada com retorno HTTP 201.
* **Status:** APROVADO
* **Evidência:** `![Validação Completa](../frontend/videos/issue_037_validacao_mvp_completa.webp)`
* **Observações:** Nenhuma quebra de layout no formulário.

---

### Cenário 9: Criação de Nova Meta
* **Perfil Utilizado:** Administrador (`admin@test.com`)
* **Rota Testada:** `/metas/nova`
* **Resultado Esperado:** Preencher título, descrição, prazo, prioridade e submeter com sucesso. A meta criada deve constar na listagem.
* **Resultado Observado:** Criação bem-sucedida da meta "Meta Release Test" com prazo e prioridade cadastrados (HTTP 201).
* **Status:** APROVADO
* **Evidência:** `![Validação Completa](../frontend/videos/issue_037_validacao_mvp_completa.webp)`
* **Observações:** Redirecionamento automático após criação.

---

### Cenário 10: Criação de Novo PDI
* **Perfil Utilizado:** Administrador (`admin@test.com`)
* **Rota Testada:** `/pdis/novo`
* **Resultado Esperado:** Preencher título, descrição, período (início/fim) e criar com sucesso.
* **Resultado Observado:** PDI "Curso de Angular" cadastrado com sucesso e associado ao colaborador selecionado (HTTP 201).
* **Status:** APROVADO
* **Evidência:** `![Validação Completa](../frontend/videos/issue_037_validacao_mvp_completa.webp)`
* **Observações:**

---

### Cenário 11: Criação de Ação de PDI
* **Perfil Utilizado:** Administrador (`admin@test.com`)
* **Rota Testada:** `/pdis/12`
* **Resultado Esperado:** Permitir adicionar uma ação ao PDI com descrição, prazo e salvamento bem-sucedido na API.
* **Resultado Observado:** Adicionada ação "Fazer curso de React Avançado" no modal de ações do PDI. Salva com sucesso via POST e renderizada no painel do PDI (HTTP 201).
* **Status:** APROVADO
* **Evidência:** `![Validação Ação PDI](../frontend/videos/issue_037_validacao_acao_pdi.webp)`
* **Observações:** O progresso do PDI atualizou após inserção.

---

### Cenário 12: Registro de Feedback
* **Perfil Utilizado:** Administrador (`admin@test.com`)
* **Rota Testada:** `/feedbacks/novo`
* **Resultado Esperado:** Preencher formulário de feedback (contexto, ponto positivo, melhoria, ação recomendada), submeter e salvar com sucesso.
* **Resultado Observado:** Feedback cadastrado e persistido com sucesso via POST /feedbacks (HTTP 201).
* **Status:** APROVADO
* **Evidência:** `![Validação Completa](../frontend/videos/issue_037_validacao_mvp_completa.webp)`
* **Observações:**

---

### Cenário 13: Registro de Reconhecimento
* **Perfil Utilizado:** Administrador (`admin@test.com`)
* **Rota Testada:** `/reconhecimentos/novo`
* **Resultado Esperado:** Preencher formulário de reconhecimento (tipo, descrição, evidência), enviar e persistir via API.
* **Resultado Observado:** Reconhecimento do tipo "DESTAQUE" registrado com sucesso via API (HTTP 201).
* **Status:** APROVADO
* **Evidência:** `![Validação Completa](../frontend/videos/issue_037_validacao_mvp_completa.webp)`
* **Observações:**

---

### Cenário 14: Funcionamento de Cadastros Auxiliares
* **Perfil Utilizado:** Administrador (`admin@test.com`)
* **Rota Testada:** `/configuracoes`
* **Resultado Esperado:** Permitir visualizar, criar ou editar registros em cada uma das abas/páginas auxiliares de configurações.
* **Resultado Observado:** As abas de Setores, Funções, Usuários e Competências carregaram dados reais. Foi criado um registro de Competência com sucesso (HTTP 201).
* **Status:** APROVADO
* **Evidência:** `![Validação Completa](../frontend/videos/issue_037_validacao_mvp_completa.webp)`
* **Observações:**

---

### Cenário 15: Tratamento de Erro 401 (Não Autorizado)
* **Perfil Utilizado:** Usuário com sessão expirada ou token inválido
* **Rota Testada:** Qualquer requisição à API que retorne 401
* **Resultado Esperado:** Sistema intercepta a falha e redireciona o usuário de volta ao login de forma limpa.
* **Resultado Observado:** Interceptador HTTP limpou o token local e forçou o redirecionamento automático para a tela de login.
* **Status:** APROVADO
* **Evidência:** `![Validação Completa](../frontend/videos/issue_037_validacao_mvp_completa.webp)`
* **Observações:** O tratamento de erro foi testado removendo manualmente o token e tentando navegar.

---

### Cenário 16: Tratamento de Erro 403 (Acesso Proibido)
* **Perfil Utilizado:** Colaborador comum (`colab@test.com` / `colab123`)
* **Rota Testada:** `/colaboradores` ou `/configuracoes`
* **Resultado Esperado:** Exibir tela ou mensagem de acesso negado correspondente ao status 403.
* **Resultado Observado:** A interface renderizou a tela de "Acesso Negado" indicando restrição de privilégios.
* **Status:** APROVADO
* **Evidência:** `![Validação Completa](../frontend/videos/issue_037_validacao_mvp_completa.webp)`
* **Observações:**

---

### Cenário 17: Tratamento de Erro 404 (Página Não Encontrada)
* **Perfil Utilizado:** Qualquer
* **Rota Testada:** `/rota-inexistente`
* **Resultado Esperado:** Exibição amigável de página de erro 404 (Não Encontrada) dentro do layout padrão ou tela específica.
* **Resultado Observado:** A página amigável de erro 404 foi exibida contendo botão de retorno ao Dashboard.
* **Status:** APROVADO
* **Evidência:** `![Validação Completa](../frontend/videos/issue_037_validacao_mvp_completa.webp)`
* **Observações:**

---

### Cenário 18: Estados de Loading (Carregamento)
* **Perfil Utilizado:** Qualquer
* **Rota Testada:** `/dashboard`, `/colaboradores`
* **Resultado Esperado:** Presença visível de indicador de loading (spinner, skeleton ou mensagem) enquanto as requisições à API estão pendentes.
* **Resultado Observado:** Indicador visual de loading é exibido durante a espera da resposta da API.
* **Status:** APROVADO
* **Evidência:** `![Validação Completa](../frontend/videos/issue_037_validacao_mvp_completa.webp)`
* **Observações:**

---

### Cenário 19: Estados de Vazio (Empty States)
* **Perfil Utilizado:** Administrador
* **Rota Testada:** `/colaboradores/11/evolucao` (colaborador sem feedbacks/reconhecimentos no seed)
* **Resultado Esperado:** Exibição de mensagem informativa e amigável indicando que não existem dados a serem mostrados.
* **Resultado Observado:** A linha de evolução exibiu placeholders textuais indicando ausência de dados de forma limpa.
* **Status:** APROVADO
* **Evidência:** `![Validação Completa](../frontend/videos/issue_037_validacao_mvp_completa.webp)`
* **Observações:**

---

### Cenário 20: Responsividade Básica (Desktop & Mobile)
* **Perfil Utilizado:** Qualquer
* **Rota Testada:** `/dashboard`, `/colaboradores`
* **Resultado Esperado:** O layout adapta-se corretamente a diferentes resoluções. A Sidebar se oculta em mobile, exibindo o menu hambúrguer e gaveta móvel acessível sem estouros de tela.
* **Resultado Observado:** No modo responsivo, a sidebar se transforma em drawer com botão hambúrguer. Sem quebra de layout ou estouro horizontal.
* **Status:** APROVADO
* **Evidência:** `![Validação Completa](../frontend/videos/issue_037_validacao_mvp_completa.webp)`
* **Observações:**
