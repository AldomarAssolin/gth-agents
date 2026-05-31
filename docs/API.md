# API - GTH Agents MVP

Este documento descreve os contratos e endpoints expostos pela API do MVP do GTH Agents.

## Informações Gerais

- **Base URL**: `http://localhost:5000` (ou porta alternativa definida em `.env`).
- **Autenticação**: O header `Authorization: Bearer <seu_token>` é exigido em todas as rotas protegidas.
- **Content-Type**: `application/json` deve ser enviado em todas as requisições com corpo.

---

## 1. Monitoramento e Saúde

### Health Check
- **URL**: `GET /health`
- **Autenticação**: Nenhuma
- **Response (200 OK):**
  ```json
  {
    "status": "ok"
  }
  ```

---

## 2. Autenticação

### Login de Usuário
- **URL**: `POST /auth/login`
- **Autenticação**: Nenhuma
- **Request Body:**
  ```json
  {
    "email": "admin@empresa.com",
    "senha": "admin_password"
  }
  ```
- **Response (200 OK):**
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "Bearer",
    "usuario": {
      "id": 1,
      "nome": "Admin",
      "email": "admin@empresa.com",
      "perfil": "ADMIN"
    }
  }
  ```

---

## 3. Cadastros Básicos

### Criar Setor
- **URL**: `POST /setores`
- **Autenticação**: `ADMIN`, `RH`
- **Request Body:**
  ```json
  {
    "nome": "Soldagem",
    "descricao": "Setor responsável pela soldagem de estruturas."
  }
  ```
- **Response (201 Created):**
  ```json
  {
    "id": 1,
    "nome": "Soldagem",
    "descricao": "Setor responsável pela soldagem de estruturas.",
    "ativo": true
  }
  ```

### Listar Setores
- **URL**: `GET /setores`
- **Autenticação**: Nenhuma

### Criar Função
- **URL**: `POST /funcoes`
- **Autenticação**: `ADMIN`, `RH`
- **Request Body:**
  ```json
  {
    "nome": "Soldador MIG/MAG",
    "descricao": "Função responsável por processos de soldagem."
  }
  ```
- **Response (201 Created):**
  ```json
  {
    "id": 1,
    "nome": "Soldador MIG/MAG",
    "descricao": "Função responsável por processos de soldagem.",
    "ativo": true
  }
  ```

### Listar Funções
- **URL**: `GET /funcoes`
- **Autenticação**: Nenhuma

### Criar Usuário
- **URL**: `POST /usuarios`
- **Autenticação**: `ADMIN`, `RH`
- **Request Body:**
  ```json
  {
    "nome": "Carlos Líder",
    "email": "carlos.lider@empresa.com",
    "senha": "liderpassword",
    "perfil": "LIDER",
    "setor_id": 1
  }
  ```
- **Response (201 Created):**
  ```json
  {
    "id": 2,
    "nome": "Carlos Líder",
    "email": "carlos.lider@empresa.com",
    "perfil": "LIDER",
    "setor_id": 1,
    "colaborador_id": null,
    "ativo": true
  }
  ```

### Listar Usuários
- **URL**: `GET /usuarios`
- **Autenticação**: Nenhuma

### Criar Competência
- **URL**: `POST /competencias`
- **Autenticação**: `ADMIN`, `RH`
- **Request Body:**
  ```json
  {
    "nome": "Soldagem de Tubos",
    "tipo": "TECNICA",
    "descricao": "Habilidade para soldagem de tubos industriais.",
    "peso": 1.5
  }
  ```
- **Response (201 Created):**
  ```json
  {
    "id": 1,
    "nome": "Soldagem de Tubos",
    "tipo": "TECNICA",
    "descricao": "Habilidade para soldagem de tubos industriais.",
    "peso": 1.5,
    "ativo": true
  }
  ```

### Listar Competências
- **URL**: `GET /competencias`
- **Autenticação**: Nenhuma

---

## 4. Colaboradores

### Criar Colaborador
- **URL**: `POST /colaboradores`
- **Autenticação**: `ADMIN`, `RH`
- **Request Body:**
  ```json
  {
    "nome": "João Silva",
    "matricula": "M001",
    "email": "joao.silva@empresa.com",
    "data_admissao": "2026-01-10",
    "setor_id": 1,
    "funcao_id": 1
  }
  ```
- **Response (201 Created):**
  ```json
  {
    "id": 1,
    "nome": "João Silva",
    "matricula": "M001",
    "email": "joao.silva@empresa.com",
    "data_admissao": "2026-01-10",
    "status": "ATIVO",
    "setor_id": 1,
    "funcao_id": 1
  }
  ```

### Listar Colaboradores
- **URL**: `GET /colaboradores`
- **Autenticação**: Todas. LIDER vê apenas o seu setor. COLABORADOR vê apenas a si mesmo.

### Buscar Colaborador por ID
- **URL**: `GET /colaboradores/<id>`
- **Autenticação**: Todas. Respeita regras de escopo.

### Transições de Status do Colaborador
- **URL**: `PATCH /colaboradores/<id>/ativar` | `PATCH /colaboradores/<id>/inativar` | `PATCH /colaboradores/<id>/afastar` | `PATCH /colaboradores/<id>/desligar`
- **Autenticação**: `ADMIN`, `RH` ou `LIDER` (mesmo setor).

---

## 5. Gestão de Talentos e Evolução

### Registrar Avaliação de Competências
- **URL**: `POST /avaliacoes`
- **Autenticação**: `ADMIN`, `RH`, `LIDER` (mesmo setor).
- **Request Body:**
  ```json
  {
    "colaborador_id": 1,
    "tipo": "AVALIACAO_LIDER",
    "observacao_geral": "Evolução sólida na parte técnica.",
    "itens": [
      {
        "competencia_id": 1,
        "nota": 4,
        "comentario": "Domina soldagem básica."
      }
    ]
  }
  ```
- **Response (201 Created):**
  ```json
  {
    "id": 1,
    "colaborador_id": 1,
    "avaliador_id": 2,
    "tipo": "AVALIACAO_LIDER",
    "observacao_geral": "Evolução sólida na parte técnica.",
    "perfil_talento": {
      "classificacao": "ESPECIALISTA_TECNICO",
      "nivel_tecnico": "ALTO",
      "nivel_comportamental": "MEDIO",
      "potencial_lideranca": "MEDIO",
      "resumo": "Classificação automática pelo agente."
    }
  }
  ```

### Consultar Último Perfil de Talento
- **URL**: `GET /colaboradores/<colaborador_id>/perfil`
- **Autenticação**: Todas (respeitando escopo).

### Registrar Meta
- **URL**: `POST /metas`
- **Autenticação**: `ADMIN`, `RH`, `LIDER` (mesmo setor).
- **Request Body:**
  ```json
  {
    "colaborador_id": 1,
    "titulo": "Melhorar Comunicação",
    "descricao": "Participar de reuniões e relatar problemas do turno.",
    "indicador": "Ocorrências registradas no sistema",
    "prazo": "2026-08-30",
    "prioridade": "MEDIA"
  }
  ```

### Consultar Metas do Colaborador
- **URL**: `GET /colaboradores/<colaborador_id>/metas`
- **Autenticação**: Todas (respeitando escopo).

### Registrar Feedback
- **URL**: `POST /feedbacks`
- **Autenticação**: `ADMIN`, `RH`, `LIDER` (mesmo setor).
- **Request Body:**
  ```json
  {
    "colaborador_id": 1,
    "contexto": "Feedbacks periódicos de acompanhamento",
    "ponto_positivo": "Pontual e focado.",
    "ponto_melhoria": "Falar em público.",
    "acao_recomendada": "Treinar apresentações curtas."
  }
  ```

### Estruturar Feedback Livre
- **URL**: `POST /feedbacks/estruturar`
- **Autenticação**: `ADMIN`, `RH`, `LIDER`.
- **Request Body:**
  ```json
  {
    "texto_livre": "João foi muito prestativo essa semana ajudando o time no turno da noite, mas precisa prestar mais atenção nos procedimentos de segurança. Recomendo ler o manual."
  }
  ```
- **Response (200 OK):**
  ```json
  {
    "ponto_positivo": "João foi muito prestativo ajudando o time no turno da noite.",
    "ponto_melhoria": "Precisa prestar mais atenção nos procedimentos de segurança.",
    "acao_recomendada": "Recomendo ler o manual."
  }
  ```

---

## 6. Plano de Desenvolvimento Individual (PDI)

### Criar PDI
- **URL**: `POST /pdis`
- **Autenticação**: `ADMIN`, `RH`, `LIDER` (mesmo setor).
- **Request Body:**
  ```json
  {
    "colaborador_id": 1,
    "titulo": "Plano de Segurança do Trabalho",
    "descricao": "Evolução do engajamento em procedimentos de segurança.",
    "origem": "AVALIACAO",
    "data_inicio": "2026-06-01",
    "data_fim": "2026-08-31",
    "acoes": [
      {
        "tipo": "TREINAMENTO",
        "descricao": "Treinamento de Segurança Operacional",
        "prazo": "2026-06-30"
      }
    ]
  }
  ```

### Listar PDIs do Colaborador
- **URL**: `GET /colaboradores/<colaborador_id>/pdis`

### Atualizar, Concluir e Cancelar PDI
- **URL**: `PATCH /pdis/<id>` | `PATCH /pdis/<id>/concluir` | `PATCH /pdis/<id>/cancelar`

### Gerenciamento de Ações do PDI
- **Criar Ação**: `POST /pdis/<pdi_id>/acoes`
- **Listar Ações**: `GET /pdis/<pdi_id>/acoes`
- **Status da Ação**: `PATCH /pdis/<pdi_id>/acoes/<acao_id>/concluir` | `PATCH /pdis/<pdi_id>/acoes/<acao_id>/cancelar`

---

## 7. Reconhecimentos

### Criar Reconhecimento
- **URL**: `POST /reconhecimentos`
- **Autenticação**: `ADMIN`, `RH`, `LIDER` (mesmo setor).
- **Request Body:**
  ```json
  {
    "colaborador_id": 1,
    "tipo": "DESTAQUE",
    "descricao": "Reconhecimento pela proatividade e segurança.",
    "evidencia": "Zero acidentes no turno e liderança nas tarefas."
  }
  ```

### Listar Reconhecimentos do Colaborador
- **URL**: `GET /colaboradores/<colaborador_id>/reconhecimentos`

### Cancelar Reconhecimento
- **URL**: `PATCH /reconhecimentos/<id>/cancelar`
- **Request Body:**
  ```json
  {
    "motivo_cancelamento": "Erro de cadastro de colaborador."
  }
  ```

---

## 8. Relatórios e Dashboard

### Obter Evolução Consolidada do Colaborador
- **URL**: `GET /colaboradores/<id>/evolucao`
- **Autenticação**: Todas (respeitando escopo).

### Obter Dashboard MVP Geral
- **URL**: `GET /dashboard/mvp`
- **Autenticação**: `ADMIN`, `RH`, `LIDER` (mesmo setor).
- **Response (200 OK):**
  Retorna um dicionário contendo blocos de `resumo_geral`, `colaboradores`, `avaliacoes`, `metas`, `pdis`, `feedbacks`, `reconhecimentos`, `perfis_talento` e `alertas`.

---

## 9. Padrões de Retornos de Erros

A API retorna os códigos HTTP adequados e um JSON com a seguinte padronização de chaves:

- **Erro de Validação (400 Bad Request)**:
  ```json
  {
    "error": "VALIDATION_ERROR",
    "message": "Nome do colaborador é obrigatório."
  }
  ```
- **Erro de Autenticação (401 Unauthorized)**:
  ```json
  {
    "error": "UNAUTHORIZED",
    "message": "Token de acesso obrigatorio."
  }
  ```
- **Erro de Acesso Negado (403 Forbidden)**:
  ```json
  {
    "error": "FORBIDDEN",
    "message": "Perfil insuficiente."
  }
  ```
- **Erro de Recurso Não Encontrado (404 Not Found)**:
  ```json
  {
    "error": "NOT_FOUND",
    "message": "Colaborador nao encontrado."
  }
  ```
