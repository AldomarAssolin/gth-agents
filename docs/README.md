# Documentação do Monorepo GTH Agents

Este monorepo contém os seguintes projetos e serviços:

## Estrutura de Diretórios
- `backend/`: API em Flask desenvolvida com foco em Clean Architecture.
- `frontend/`: Aplicação Web desenvolvida com React, Vite e TailwindCSS.
- `docs/`: Central de documentação e manuais do projeto.

## Execução com Docker (Desenvolvimento)
Para subir todos os serviços de desenvolvimento (PostgreSQL, Flask e React) em containers:
```bash
docker compose up -d
```

### Endereços Locais
- **Frontend (Web)**: http://localhost:5173
- **Backend (API)**: http://localhost:5000
- **Health check da API**: http://localhost:5000/health
