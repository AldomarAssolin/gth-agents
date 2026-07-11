# Scratchpad de Validação Manual — Proteger Endpoints Administrativos de Cadastros Auxiliares (Issue #073)

Este documento descreve os cenários de testes e validações manuais de segurança que o homologador humano deve executar (por exemplo, via Postman, Insomnia ou chamadas de API no console) para validar o comportamento do backend de cadastros auxiliares (setores, funções, usuários e competências).

**Status atual da validação:** `VALIDAÇÃO HUMANA CONCLUÍDA`

---

## Cenários de Teste Manual

### 1. Chamadas Sem Token JWT (Não Autenticado)
- **Passos**:
  1. Realize uma chamada `GET /setores`, `GET /funcoes` ou `GET /competencias` sem enviar o header `Authorization`.
  2. Realize uma chamada `POST /setores` ou `PUT /usuarios/1` sem enviar o header `Authorization`.
- **Resultado esperado**:
  - Todas as chamadas retornam HTTP `401 Unauthorized`.
  - O corpo da resposta deve conter o JSON padrão:
    ```json
    {
      "error": "UNAUTHORIZED",
      "message": "Token de acesso obrigatorio."
    }
    ```
- **Resultado Observado**:
  A requisição retornou HTTP `401 Unauthorized`.

  Corpo recebido:

  ```json
  {
    "error": "UNAUTHORIZED",
    "message": "Token de acesso obrigatorio."
  }
  ```

**Status: APROVADO**

---

### 2. Acesso Negado para Perfis de Menor Privilégio (LIDER / COLABORADOR)
- **Passos**:
  1. Efetue login na API utilizando credenciais de um usuário com perfil `COLABORADOR` ou `LIDER`.
  2. Extraia o token JWT e configure as requisições com o header `Authorization: Bearer <TOKEN>`.
  3. Tente realizar qualquer operação de escrita (exemplo: `POST /setores`, `PUT /funcoes/1`, `PATCH /usuarios/1/desativar`).
  4. Tente realizar as leituras administrativas restritas (exemplo: `GET /usuarios`, `GET /usuarios/1`, `GET /setores/1`).
- **Resultado esperado**:
  - Todas as chamadas retornam HTTP `403 Forbidden`.
  - O corpo da resposta deve conter o JSON padrão:
    ```json
    {
      "error": "FORBIDDEN",
      "message": "Perfil insuficiente."
    }
    ```
- **Resultado Observado**:
  - A requisição retorna HTTP `403 Forbidden`.
    ```json
    {
      "error": "FORBIDDEN",
      "message": "Perfil insuficiente."
    }
    ```

> Com `LIDER`, as operações administrativas testadas retornaram HTTP `403 Forbidden`.

> Com `COLABORADOR`, as operações administrativas testadas retornaram HTTP `403 Forbidden`.

**Status: APROVADO**

---

### 3. Acesso Autorizado para Perfis Administrativos (ADMIN / RH)
- **Passos**:
  1. Efetue login na API utilizando credenciais de um usuário com perfil `ADMIN` ou `RH`.
  2. Configure as requisições com o header `Authorization: Bearer <TOKEN>`.
  3. Realize operações de manutenção (exemplo: crie um setor via `POST /setores`, atualize uma função via `PUT /funcoes/{id}`, desative e ative um usuário via `PATCH /usuarios/{id}/desativar`).
- **Resultado esperado**:
  - As operações devem ser concluídas com sucesso (HTTP `200 OK` ou `201 Created`).
  - O estado da entidade é atualizado no banco de dados.

- **Resultado Observado**:
  - Criando setor: 'POST /setores' - resultado alcançado (HTTP `201 Created`).
  ```json
  {
    "ativo": true,
    "criado_em": "2026-07-11T16:45:11.814445+00:00",
    "descricao": null,
    "id": 10,
    "nome": "Manutenção"
  }
  ```
  - Atualizando setor: 'PUT /setores/{id}' - resultado alcançado (HTTP `200 OK`).
  ```json
  {
    "ativo": true,
    "criado_em": "2026-07-11T16:45:11.814445+00:00",
    "descricao": null,
    "id": 10,
    "nome": "Qualidade"
  }
  ```
  - Desativando usuário: 'PATCH /usuarios/{id}/desativar' - resultado alcançado (HTTP `200 OK`).
  ```json
  {
    "ativo": false,
    "colaborador_id": null,
    "criado_em": "2026-06-28T18:26:04.689935+00:00",
    "email": "admin@test.com",
    "id": 17,
    "nome": "Admin User",
    "perfil": "ADMIN",
    "setor_id": null
  }
  ```
  - Ativando usuário: 'PATCH /usuarios/{id}/ativar' - resultado alcançado (HTTP `200 OK`).
  ```json
  {
    "ativo": true,
    "colaborador_id": null,
    "criado_em": "2026-06-28T18:26:04.689935+00:00",
    "email": "admin@test.com",
    "id": 17,
    "nome": "Admin User",
    "perfil": "ADMIN",
    "setor_id": null
  }
  ```
> A homologação manual das operações administrativas foi executada com o perfil `ADMIN`. O comportamento equivalente do perfil `RH` foi coberto pela suíte automatizada específica da Issue #073.

**Status: APROVADO**

---

### 4. Proteção contra Spoofing de Perfil (JWT vs Payload)
- **Passos**:
  1. Efetue login como `COLABORADOR`.
  2. Envie uma requisição `POST /usuarios` ou `PUT /usuarios/{id}` informando no corpo JSON:
     ```json
     {
       "nome": "Tentativa Spoofing",
       "email": "spoofing@test.com",
       "perfil": "ADMIN"
     }
     ```
- **Resultado esperado**:
  - O servidor deve rejeitar a requisição com HTTP `403 Forbidden` devido ao perfil do solicitante (que é `COLABORADOR` no token JWT).
  - O backend não deve cadastrar o novo usuário ou alterar o usuário existente.

- **Resultado Observado**:
  - A requisição retorna HTTP `403 Forbidden`.
  ```json
  {
    "error": "FORBIDDEN",
    "message": "Perfil insuficiente."
  }
  ```

  - O usuário não foi criado no banco de dados:
  ```sql
  SELECT id, nome, email, perfil FROM usuarios WHERE email = 'spoofing@test.com';
  ```

  ```bash
   id | nome | email | perfil
  ----+------+-------+--------
  (0 rows)

  ```

  > Resultado: Nenhum registro encontrado.

**Status: APROVADO**

---

### 5. Não Vazamento de Senhas (`senha` e `senha_hash`)
- **Passos**:
  1. Efetue login como `ADMIN` ou `RH`.
  2. Realize chamadas de leitura de usuários:
     - `GET /usuarios` (Listagem)
     - `GET /usuarios/{id}` (Obtenção individual)
  3. Realize chamadas de escrita de usuários:
     - `POST /usuarios` (Criação)
     - `PUT /usuarios/{id}` (Edição)
- **Resultado esperado**:
  - Em nenhuma das respostas HTTP devem estar presentes as propriedades `"senha"` ou `"senha_hash"`.
  - O JSON de retorno deve conter apenas os campos públicos e seguros do usuário (ex: `id`, `nome`, `email`, `perfil`, `ativo`, etc.).

- **Resultado Observado**:
  - As propriedades `"senha"` e `"senha_hash"` não estão presentes nas respostas HTTP.
  - O JSON de retorno contém apenas os campos públicos e seguros do usuário:
  ```json
  {
        "ativo": true,
        "colaborador_id": null,
        "criado_em": "2026-06-28T18:26:04.689935+00:00",
        "email": "admin@test.com",
        "id": 17,
        "nome": "Admin User",
        "perfil": "ADMIN",
        "setor_id": null
  }
  ```

**Status: APROVADO**

---

## 6. Listagens operacionais para LIDER e COLABORADOR

### Passos

1. Autenticar como `LIDER`.
2. Executar:
   - `GET /setores`;
   - `GET /funcoes`;
   - `GET /competencias`.
3. Repetir com perfil `COLABORADOR`.

### Resultado esperado

- Todas as requisições retornam HTTP `200 OK`.
- Os dados necessários aos formulários operacionais continuam disponíveis.

### Resultado observado
  - LIDER:
    - GET /setores retornou `HTTP 200 OK`
    ```json
    [
        {
            "ativo": true,
            "criado_em": "2026-06-28T18:26:04.655801+00:00",
            "descricao": "Setor de Engenharia de Software",
            "id": 8,
            "nome": "Engenharia"
        },
        {
            "ativo": true,
            "criado_em": "2026-06-28T18:26:04.655806+00:00",
            "descricao": "Setor de Marketing Digital",
            "id": 9,
            "nome": "Marketing"
        }
    ]
    ```
    - GET /funcoes retornou `HTTP 200 OK`
    ```json
    [
      {
          "ativo": true,
          "criado_em": "2026-06-28T18:26:04.664604+00:00",
          "descricao": "Desenvolvedor Full Stack",
          "id": 8,
          "nome": "Desenvolvedor"
      },
      {
          "ativo": true,
          "criado_em": "2026-06-28T18:26:04.664608+00:00",
          "descricao": "Analista de Mídias Sociais",
          "id": 9,
          "nome": "Analista de Marketing"
      }
    ]
    ```
    - GET /competencias retornou `HTTP 200 OK`
    ```json
    [
        {
            "ativo": true,
            "criado_em": "2026-06-28T18:28:50.796346+00:00",
            "descricao": "React frontend development skill",
            "id": 16,
            "nome": "React",
            "peso": "1.00",
            "tipo": "TECNICA"
        }
    ]
    ```
    **Status: APROVADO**

  - COLABORADOR:
    - GET /setores retornou `HTTP 200 OK`
    ```json
    [
      {
          "ativo": true,
          "criado_em": "2026-06-28T18:26:04.655801+00:00",
          "descricao": "Setor de Engenharia de Software",
          "id": 8,
          "nome": "Engenharia"
      },
      {
          "ativo": true,
          "criado_em": "2026-06-28T18:26:04.655806+00:00",
          "descricao": "Setor de Marketing Digital",
          "id": 9,
          "nome": "Marketing"
      }
    ]
    ```
    - GET /funcoes retornou `HTTP 200 OK`
    ```json
    [
        {
            "ativo": true,
            "criado_em": "2026-06-28T18:26:04.664604+00:00",
            "descricao": "Desenvolvedor Full Stack",
            "id": 8,
            "nome": "Desenvolvedor"
        },
        {
            "ativo": true,
            "criado_em": "2026-06-28T18:26:04.664608+00:00",
            "descricao": "Analista de Mídias Sociais",
            "id": 9,
            "nome": "Analista de Marketing"
        }
    ]
    ```
    - GET /competencias retornou `HTTP 200 OK`
    ```json
    [
      {
          "ativo": true,
          "criado_em": "2026-06-28T18:28:50.796346+00:00",
          "descricao": "React frontend development skill",
          "id": 16,
          "nome": "React",
          "peso": "1.00",
          "tipo": "TECNICA"
      }
    ]
    ```
    **Status: APROVADO**

---

## Validações Técnicas

- [x] Execução e aprovação dos novos testes de segurança específicos (`test_issue_073_admin_auxiliary_endpoints_security.py`)
- [x] Execução e aprovação de toda a suíte de testes de regressão do backend (`pytest`)

## Resultado final

| Cenário | Status |
|---|---|
| Requisições sem token | APROVADO |
| Operações administrativas com LIDER/COLABORADOR | APROVADO |
| Operações administrativas com ADMIN | APROVADO |
| Operações administrativas com RH | COBERTO POR TESTE AUTOMATIZADO |
| Spoofing de perfil | APROVADO |
| Ausência de persistência após bloqueio | COBERTO POR TESTE AUTOMATIZADO |
| Listagens operacionais para LIDER/COLABORADOR | APROVADO |
| Ausência de senha e senha_hash | APROVADO |

**Status final: VALIDAÇÃO HUMANA CONCLUÍDA**