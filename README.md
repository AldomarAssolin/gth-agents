# GTH Agents Monorepo

Este é o repositório principal unificado (Monorepo) do projeto **GTH Agents**. Ele consolida em um único local a aplicação de backend (API Flask) e a aplicação de frontend (React/Vite).

## Estrutura do Projeto

```text
gth-agents/
├── backend/            # API Flask (Clean Architecture)
├── frontend/           # Interface React + Vite
├── docs/               # Documentação geral do projeto
├── docker-compose.yml  # Configuração de containers Docker para desenvolvimento
├── .gitignore          # Regras globais de exclusão do Git
└── README.md           # Este arquivo de documentação principal
```

## Requisitos Prévios
- Docker e Docker Compose
- Python 3.12+ (caso queira rodar local sem Docker)
- Node.js 24+ (caso queira rodar local sem Docker)

---

## Como Rodar a Aplicação

### 1. Usando Docker (Recomendado)
Para subir o banco de dados PostgreSQL, a API backend e o painel Web de uma só vez:

```bash
docker compose up --build -d
```

Após o build e inicialização dos serviços, acesse:
- **Frontend (Web)**: http://localhost:5173
- **Backend (API)**: http://localhost:5000
- **Health Check da API**: http://localhost:5000/health

Para aplicar as migrações do banco de dados dentro do container do backend:
```bash
docker compose exec api alembic upgrade head
```

### 2. Rodando Localmente (Sem Docker)

#### Backend
Acesse o diretório `backend`, configure o ambiente virtual e execute o servidor:
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
flask run
```

#### Frontend
Acesse o diretório `frontend`, instale as dependências e rode o servidor de desenvolvimento:
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

---

## Testes e Validação

### Testes do Backend
```bash
cd backend
pytest
```

### Lint e Build do Frontend
```bash
cd frontend
npm run lint
npm run build
```
