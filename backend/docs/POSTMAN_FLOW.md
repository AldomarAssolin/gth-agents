# Fluxo de Testes com o Postman

Este documento serve como roteiro prático para guiar a execução ponta a ponta do fluxo de testes manuais da API do GTH Agents no Postman.

---

## 1. Configurando o Ambiente (Environment)

Antes de rodar as requisições, certifique-se de importar o arquivo de ambiente localizado em:
`postman/GTH_Agents_MVP.postman_environment.json`.

Esse ambiente inicializa as seguintes variáveis globais necessárias:
- `base_url`: `http://localhost:5000` (URL base da API).
- `access_token`: Armazena dinamicamente o Bearer Token JWT obtido no login.

---

## 2. Sequência Recomendada de Execução

Execute as requisições na ordem abaixo para preencher as variáveis e criar os vínculos necessários:

### Passo 00: Saúde do Servidor
- Execute a chamada `GET /health` na pasta **00 - Health** para garantir que a API está no ar.

### Passo 01: Login e Autenticação
- Acesse a pasta **01 - Auth** e execute `POST /auth/login` informando as credenciais de administrador padrão (geralmente geradas pelos seeds iniciais, ex: `admin@empresa.com` / `123456`).
- **Automação**: O script contido em `Tests` da requisição salvará automaticamente o `access_token` no ambiente do Postman.

### Passo 02: Cadastros Básicos
Abra a pasta **03 - Cadastro Base** e execute:
1. `POST /setores` (Salva automaticamente o `setor_id` nas variáveis do ambiente).
2. `POST /funcoes` (Salva automaticamente o `funcao_id` nas variáveis do ambiente).
3. `POST /usuarios` (Cria um usuário com o perfil `LIDER` associado ao `setor_id`).

### Passo 03: Cadastros de Colaboradores e Competências
1. Acesse **04 - Colaboradores** e chame `POST /colaboradores` (Usa `setor_id` e `funcao_id` das variáveis e salva o `colaborador_id` criado).
2. Acesse **05 - Competências** e crie pelo menos uma competência do tipo `TECNICA` e outra do tipo `COMPORTAMENTAL` (Chame `POST /competencias`, salvando os respectivos IDs).

### Passo 04: Avaliação e Perfil de Talento
1. Acesse **06 - Avaliações** e chame `POST /avaliacoes` passando o `colaborador_id` e os IDs das competências criadas.
- **Automação**: Esta requisição executa os agentes de avaliação e perfil de talento e armazena os resultados.
2. Acesse **07 - Perfil de Talento** e execute `GET /colaboradores/{{colaborador_id}}/perfil` para visualizar a classificação final calculada pelo agente.

### Passo 05: Gestão de Desenvolvimento
A partir do perfil calculado, você pode criar metas e registrar feedbacks para o colaborador:
1. Acesse **08 - Metas** e envie `POST /metas`.
2. Acesse **09 - Feedbacks** e envie `POST /feedbacks`.
3. Experimente estruturar um texto de feedback informal usando `POST /feedbacks/estruturar`.

### Passo 06: PDI e Ações
1. Acesse **10 - PDI** e crie um Plano de Desenvolvimento Individual usando `POST /pdis`. O ID do PDI criado será armazenado como `pdi_id`.
2. Adicione uma ação ao plano usando `POST /pdis/{{pdi_id}}/acoes`.
3. Teste a conclusão de uma ação chamando `PATCH /pdis/{{pdi_id}}/acoes/{{acao_id}}/concluir`.

### Passo 07: Reconhecimentos e Cancelamentos
1. Acesse **11 - Reconhecimentos** e envie `POST /reconhecimentos` para registrar uma conquista ativa.
2. Se necessário, teste o fluxo de cancelamento de um reconhecimento com a rota `PATCH /reconhecimentos/{{reconhecimento_id}}/cancelar`.

### Passo 08: Visualização de Dashboards e Evolução
1. Acesse **12 - Evolução do Colaborador** e chame `GET /colaboradores/{{colaborador_id}}/evolucao` para ver a consolidação de todo o histórico do colaborador.
2. Acesse **13 - Dashboard MVP** e chame `GET /dashboard/mvp` para visualizar o dashboard executivo consolidado com contagens de status e alertas.

---

## 3. Scripts Utilizados nas Requests do Postman

Para garantir que os testes rodem em cadeia perfeitamente, os seguintes scripts foram inseridos nas abas de teste do Postman:

### Salvar Token no Login
```javascript
const responseJson = pm.response.json();
if (responseJson.access_token) {
    pm.environment.set("access_token", responseJson.access_token);
}
```

### Salvar IDs dos Cadastros
```javascript
const responseJson = pm.response.json();
if (responseJson.id) {
    pm.environment.set("setor_id", responseJson.id); // ou funcao_id, colaborador_id, etc.
}
```
