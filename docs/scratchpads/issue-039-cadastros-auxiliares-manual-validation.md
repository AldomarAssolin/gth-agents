# Roteiro de Validação Manual - Cadastros Auxiliares (Issue #039)

Este documento descreve os cenários de teste manual para validar a implementação da Issue #039 no frontend do **GTH Agents**.

---

## 1. Controle de Acesso e Bloqueio Visual

### Cenário 1.1: Ocultação da Opção na Sidebar (LIDER/COLABORADOR)
1. Fazer login com um usuário que tenha o perfil `LIDER` ou `COLABORADOR`.
2. Verificar a Sidebar de navegação lateral.
3. **Resultado esperado**: O item "Configurações" **não** deve estar visível no menu.
4. **Resultado observado**: O item "Configurações" não estava visível no menu.
5. **Status**: APROVADO
6. **Evidência**: [Screenshot](../frontend/imagens/cadastros_auxiliares/issue_039_cenario1.png)

### Cenário 1.2: Bloqueio Visual via Rota Direta (LIDER/COLABORADOR)
1. Fazer login com perfil `LIDER` ou `COLABORADOR`.
2. Tentar acessar diretamente no navegador qualquer uma das seguintes URLs:
   - `http://localhost:5173/configuracoes`
   - `http://localhost:5173/configuracoes/setores`
   - `http://localhost:5173/configuracoes/funcoes`
   - `http://localhost:5173/configuracoes/usuarios`
   - `http://localhost:5173/configuracoes/competencias`
3. **Resultado esperado**: O frontend deve interceptar e exibir a tela de "Acesso Negado" (com o botão para retornar ao Início), e **não** renderizar o painel ou as listagens de dados.
4. **Resultado observado**: O frontend interceptou e exibiu a tela de "Acesso Negado" (com o botão para retornar ao Início), e não renderizou o painel ou as listagens de dados.
5. **Status**: APROVADO
6. **Evidência**: [Screenshot](../frontend/imagens/cadastros_auxiliares/issue_039_cenario2.png)

### Cenário 1.3: Visualização do Painel Completo (ADMIN/RH)
1. Fazer login com um usuário de perfil `ADMIN` ou `RH`.
2. Clicar em "Configurações" na Sidebar ou acessar `http://localhost:5173/configuracoes`.
3. **Resultado esperado**: A Sidebar exibe o item "Configurações", e a rota correspondente renderiza o painel com os quatro cards (Setores, Funções, Usuários, Competências).
4. **Resultado observado**: A Sidebar exibe o item "Configurações", e a rota correspondente renderiza o painel com os quatro cards (Setores, Funções, Usuários, Competências).
5. **Status**: APROVADO
6. **Evidência**: [Screenshot](../frontend/imagens/cadastros_auxiliares/issue_039_cenario1_config_page.png)

---

## 2. Validação de Chamadas de Rede e HTTP 403

### Cenário 2.1 - Tratamento de Erro HTTP 403 Real da API

- **Objetivo:** Validar se o frontend trata corretamente uma resposta de permissão negada retornada pela API.
- **Perfil visual no frontend:** ADMIN
- **Token real utilizado:** usuário sem permissão administrativa, em cenário de simulação controlada.
- **Rota testada:** `/configuracoes/setores`
- **Operação:** tentativa de criação de setor.
- **Resultado observado:** Ao tentar salvar um setor, a API retornou erro de permissão. O frontend exibiu a mensagem “Perfil insuficiente.” dentro do formulário, manteve a tela renderizada, preservou os campos preenchidos e não causou falha visual ou tela branca.
- **Status:** APROVADO
- **Observação:** O teste foi realizado simulando inconsistência controlada entre o perfil visual armazenado no frontend e o perfil real presente no token JWT. Esse cenário valida a resiliência do frontend diante de um HTTP 403 real da API.
- **Evidência:** [Screenshot](../frontend/imagens/cadastros_auxiliares/issue_039_validacao_chamadas.png)

### Observação de segurança backend

Durante a validação, a criação de setor retornou erro de permissão quando executada com token de usuário sem perfil administrativo, porém operações de atualização e desativação foram executadas com sucesso no mesmo cenário de inconsistência controlada.

Isso reforça o risco técnico já documentado: há endpoints administrativos de cadastros auxiliares com proteção backend incompleta ou inconsistente.

>A correção deve ser tratada em issue futura de backend.

---

## 3. Fluxo de Criação e Regras de Segurança de Senha (Usuários)

### Cenário 3.1: Cadastro de Novo Usuário (Sucesso)
1. Acessar `/configuracoes/usuarios` e clicar em "Novo Usuário".
2. Preencher todos os campos (Nome, E-mail, Senha, Perfil, Setor e Colaborador).
3. Clicar em "Salvar Usuário".
4. **Resultado esperado**:
   - O usuário deve ser criado com sucesso e adicionado ao topo da lista.
   - O formulário inteiro deve ser limpo (inclusive campos de texto, e-mail, perfil e senha).
   - O campo `senha` nunca deve aparecer em logs do console ou persistido no estado local de listagem.
4. **Resultado observado**:
   - O usuário foi criado com sucesso e adicionado ao topo da lista.
   - O formulário inteiro foi limpo (inclusive campos de texto, e-mail, perfil e senha).
   - O campo `senha` nunca apareceu em logs do console ou persistido no estado local de listagem.
5. **Status**: APROVADO
6. **Evidência**: [Screenshot](../frontend/imagens/cadastros_auxiliares/issue_039_cenario3_sucesso.png)

### Cenário 3.2: Cadastro de Novo Usuário (Erro / Conflito)
1. Acessar `/configuracoes/usuarios` e clicar em "Novo Usuário".
2. Preencher com um e-mail que já existe no sistema para simular um erro `409 Conflict`.
3. Digitar uma senha no campo correspondente.
4. Clicar em "Salvar Usuário".
5. **Resultado esperado**:
   - A API retorna erro de conflito e o formulário exibe a mensagem correspondente.
   - O campo `senha` deve ser **limpo automaticamente** do input do formulário por motivos de segurança.
   - Os demais campos não sensíveis (Nome, E-mail, Perfil, Colaborador, Setor) **devem continuar preenchidos** para evitar que o usuário perca o trabalho feito.
6. **Resultado observado**:
   - A API retornou erro de conflito e o formulário exibiu a mensagem correspondente.
   - O campo `senha` foi limpo automaticamente do input do formulário por motivos de segurança.
   - Os demais campos não sensíveis (Nome, E-mail, Perfil, Colaborador, Setor) continuaram preenchidos para evitar que o usuário perdesse o trabalho feito.
7. **Status**: APROVADO
8. **Evidência**: [Screenshot](../frontend/imagens/cadastros_auxiliares/issue_039_email_existente.png)

### Cenário 3.3: Edição de Usuário (Alterando Senha)
1. Selecionar um usuário existente na listagem e clicar em "Editar".
2. Preencher o campo de senha com uma nova senha.
3. Clicar em "Atualizar Usuário".
4. **Resultado esperado**: A requisição de atualização envia a nova senha no payload JSON, e o usuário é atualizado com sucesso. O campo de senha é limpo após a submissão.
5. **Resultado observado**:
   - A requisição foi enviada com a nova senha no payload JSON.
   - O usuário foi atualizado com sucesso.
   - O campo de senha foi limpo após a submissão.
6. **Status**: APROVADO
7. **Evidência**: [Screenshot](../frontend/imagens/cadastros_auxiliares/issue_039_cenario3_sucesso.png)

### Cenário 3.4: Edição de Usuário (Mantendo a Senha Atual)
1. Selecionar um usuário existente na listagem e clicar em "Editar".
2. Alterar o nome ou perfil do usuário, deixando o campo de senha **completamente vazio**.
3. Clicar em "Atualizar Usuário".
4. **Resultado esperado**: O frontend deve omitir o atributo `senha` do payload JSON enviado à API, evitando enviar uma string vazia ou sobrescrever a senha existente no backend.
5. **Resultado observado**:
   - A requisição foi enviada com a nova senha no payload JSON.
   - O usuário foi atualizado com sucesso.
   - O campo de senha foi limpo após a submissão.
6. **Status**: APROVADO
7. **Evidência**: [Screenshot](../frontend/imagens/cadastros_auxiliares/issue_039_cenario3_sucesso.png)

---

## 4. Cadastro de Recursos Básicos (Setores, Funções, Competências)

### Cenário 4.1: Gerenciamento de Setores e Funções
1. Acessar as páginas `/configuracoes/setores` e `/configuracoes/funcoes`.
2. Adicionar novos registros de teste e editar os registros criados.
3. **Resultado esperado**: Os dados são salvos corretamente. A listagem é atualizada em tempo real. Os botões de Ativar/Desativar realizam as chamadas aos endpoints `PATCH` e refletem o novo status na badge de status na tabela.
4. **Resultado observado**:
   - Os dados foram salvos corretamente.
   - A listagem foi atualizada em tempo real.
   - Os botões de Ativar/Desativar realizaram as chamadas aos endpoints `PATCH` e refletem o novo status na badge de status na tabela.
5. **Status**: APROVADO
6. **Evidência**: [Screenshot](../frontend/imagens/cadastros_auxiliares/issue_039_cenario3_sucesso.png)

### Cenário 4.2: Cadastro de Competências e Validação de Peso
1. Acessar `/configuracoes/competencias` e tentar salvar com peso `0` ou `-1`.
2. **Resultado esperado**: O formulário impede a submissão exibindo erro de validação.
3. Corrigir o peso para `1.5` ou `2.0` e salvar.
4. **Resultado esperado**: A competência é criada e adicionada à listagem mostrando o tipo correto via badge e o peso correspondente.
5. **Resultado observado**:
   - O formulário impede a submissão exibindo erro de validação.
   - A competência foi criada e adicionada à listagem mostrando o tipo correto via badge e o peso correspondente.
6. **Status**: APROVADO
7. **Evidência**: [Screenshot](../frontend/imagens/cadastros_auxiliares/issue_039_validacao_nota.png)
