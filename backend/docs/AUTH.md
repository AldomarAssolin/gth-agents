# Autenticação, Autorização e Escopos de Acesso

O GTH Agents utiliza segurança baseada em tokens JWT e duas camadas de controle de acesso: controle de acesso baseado em papéis (RBAC - Role-Based Access Control) e controle de acesso por escopo de dados (Access Scope).

---

## 1. Fluxo de Autenticação

### Login
Para autenticar-se e obter um token de acesso, envie uma requisição HTTP POST para o endpoint `/auth/login`.

**Request:**
- **URL**: `POST /auth/login`
- **Headers**: `Content-Type: application/json`
- **Body**:
  ```json
  {
    "email": "admin@empresa.com",
    "senha": "123456"
  }
  ```

**Response (200 OK):**
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

### Uso do Token JWT
Para realizar chamadas nos endpoints protegidos, o token recebido no login deve ser adicionado no cabeçalho (header) de todas as requisições HTTP:

```http
Authorization: Bearer <seu_access_token>
```

---

## 2. Perfis de Usuário (RBAC)

O sistema possui os seguintes perfis cadastrados no enum `PerfilUsuario`:

1. **ADMIN**: Administrador do sistema.
2. **RH**: Profissional de Recursos Humanos.
3. **LIDER**: Gestor ou líder de um setor específico.
4. **COLABORADOR**: Funcionário cadastrado no sistema.

---

## 3. Controle de Escopo de Acesso (Access Scope)

Apenas possuir um token de acesso válido não garante acesso completo às informações do sistema. As permissões de leitura e escrita são refinadas pelo **escopo de relacionamento** do usuário autenticado no sistema, conforme detalhado abaixo:

| Perfil | Escopo de Visualização / Leitura | Escopo de Escrita / Alterações |
|---|---|---|
| **ADMIN** | Acesso total a todos os colaboradores de todos os setores do sistema. | Permissão total de escrita e desativação de recursos. |
| **RH** | Acesso total a todos os colaboradores de todos os setores do sistema. | Permissão total de escrita e desativação de recursos. |
| **LIDER** | Acesso restrito a colaboradores que pertencem ao mesmo `setor_id` do líder. | Pode gerenciar metas, PDIs, feedbacks e reconhecimentos apenas para colaboradores do seu setor. |
| **COLABORADOR**| Acesso estritamente aos seus próprios dados de cadastro, metas, PDIs, reconhecimentos e evolução consolidada. | Nenhuma permissão de escrita ou alteração de dados. |

---

## 4. Retornos e Padrões de Erro

Caso a autenticação falhe ou o usuário tente acessar dados fora do seu escopo, a API retornará os seguintes formatos padronizados:

### Sem Token ou Token Inválido (401 Unauthorized)
```json
{
  "error": "UNAUTHORIZED",
  "message": "Token de acesso obrigatorio."
}
```

### Perfil ou Escopo Insuficiente (403 Forbidden)
```json
{
  "error": "FORBIDDEN",
  "message": "Perfil insuficiente."
}
```
ou, para restrições de escopo de dados:
```json
{
  "error": "FORBIDDEN",
  "message": "Acesso negado. O colaborador nao pertence ao escopo do usuario."
}
```
