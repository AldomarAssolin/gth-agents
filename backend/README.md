# GTH Agents - Backend API

API REST desenvolvida em Python/Flask para sustentar os módulos de Gestão do Talento Humano do GTH Agents.

O backend é responsável por orquestrar regras de negócio, cálculo de competências, classificação de perfis de talento, controle de permissões, controle de acesso por escopo e persistência de dados.

A estrutura segue princípios de **Clean Architecture**, separando regras de domínio, casos de uso, infraestrutura e interface HTTP.

---

## Stack de Tecnologias

* **Linguagem**: Python
* **Framework Web**: Flask
* **Persistência**: PostgreSQL, SQLAlchemy
* **Migrações de Banco**: Alembic
* **Autenticação**: JWT
* **Ambiente de Execução**: Docker, Docker Compose
* **Testes Automatizados**: Pytest, Pytest-Cov

---

## Estrutura de Arquitetura Limpa

A divisão de responsabilidades está organizada em quatro camadas principais para melhorar testabilidade, manutenção e separação entre regras de negócio e detalhes técnicos.

```text
backend/
├── domain/            # Regras de negócio essenciais, entidades, enums e services de domínio
├── application/       # Casos de uso, DTOs, portas e erros de aplicação
├── infrastructure/    # Banco, ORM, repositórios, segurança e Unit of Work
└── interface/         # Rotas Flask, schemas, autenticação HTTP e tratamento de erros
```

---

## 1. Domain

A camada `domain/` contém os conceitos centrais do negócio, sem dependência direta de Flask, SQLAlchemy ou banco de dados.

Principais responsabilidades:

* representar entidades de negócio;
* concentrar regras essenciais do domínio;
* definir enums e classificações utilizadas pelo sistema;
* apoiar cálculos e classificações determinísticas.

Exemplos de entidades:

```text
AcaoPDI
Avaliacao
Colaborador
Competencia
Feedback
Funcao
ItemAvaliacao
Meta
PDI
PerfilTalento
Reconhecimento
Setor
Usuario
ExecucaoAgente
```

Exemplos de enums:

```text
PerfilUsuario
StatusColaborador
TipoCompetencia
TipoAvaliacao
ClassificacaoTalento
StatusMeta
PrioridadeMeta
StatusPDI
OrigemPDI
TipoReconhecimento
```

Perfis técnicos utilizados:

```text
ADMIN
RH
LIDER
COLABORADOR
```

---

## 2. Application

A camada `application/` coordena os fluxos do sistema por meio de casos de uso.

Ela recebe dados da interface, aplica regras de aplicação, chama serviços de domínio e utiliza portas de repositório para persistência, sem depender diretamente de Flask ou SQLAlchemy.

Principais responsabilidades:

* autenticar usuários;
* criar e consultar colaboradores;
* registrar avaliações;
* calcular competências;
* gerar perfis de talento;
* criar e acompanhar metas;
* criar e gerenciar PDIs;
* registrar feedbacks;
* registrar reconhecimentos;
* consolidar evolução do colaborador;
* consultar indicadores de dashboard.

Exemplos de casos de uso:

```text
login_usuario_uc.py
criar_colaborador_uc.py
registrar_avaliacao_uc.py
gerar_perfil_talento_uc.py
criar_meta_uc.py
listar_metas_uc.py
pdi_uc.py
registrar_feedback_uc.py
estruturar_feedback_uc.py
reconhecimento_uc.py
evolucao_colaborador_uc.py
dashboard_uc.py
```

Também ficam nesta camada:

```text
application/dtos/
application/ports/
application/errors.py
```

---

## 3. Infrastructure

A camada `infrastructure/` implementa os detalhes técnicos necessários para sustentar a aplicação.

Principais responsabilidades:

* mapear tabelas com SQLAlchemy;
* implementar repositórios concretos;
* gerenciar transações com Unit of Work;
* gerar e validar tokens JWT;
* integrar a aplicação com o PostgreSQL.

Estrutura típica:

```text
infrastructure/
├── database/
│   └── models/
├── repositories/
├── security/
└── unit_of_work_sqlalchemy.py
```

---

## 4. Interface

A camada `interface/` expõe os casos de uso por meio de rotas HTTP em Flask.

Principais responsabilidades:

* receber requisições;
* validar payloads;
* obter o usuário autenticado;
* chamar casos de uso;
* serializar respostas;
* padronizar erros HTTP.

Estrutura típica:

```text
interface/
├── routes/
├── schemas/
└── error_handler.py
```

---

## Principais Endpoints da API Flask

A lista abaixo resume os principais endpoints implementados e documentados no backend. Em caso de dúvida, as rotas Flask devem ser tratadas como fonte de verdade.

### Autenticação e Saúde

* `POST /auth/login` - Valida credenciais e emite token JWT.
* `GET /health` - Health check da API.

### Dashboard

* `GET /dashboard/mvp` - Retorna indicadores gerais consolidados do MVP.

### Colaboradores

* `GET /colaboradores` - Lista colaboradores conforme perfil e escopo do usuário autenticado.
* `POST /colaboradores` - Cadastra um novo colaborador.
* `GET /colaboradores/<int:id>` - Retorna detalhes de um colaborador.
* `PUT /colaboradores/<int:id>` - Atualiza dados cadastrais de um colaborador.
* `GET /colaboradores/<int:colaborador_id>/perfil` - Retorna o perfil de talento atual do colaborador.
* `GET /colaboradores/<int:id>/evolucao` - Retorna a evolução consolidada do colaborador.
* `GET /colaboradores/<int:id>/metas` - Lista metas vinculadas a um colaborador.

### Avaliações

* `POST /avaliacoes` - Registra uma avaliação e aciona o cálculo de competências e perfil de talento.

### Metas

* `POST /metas` - Cria uma nova meta para um colaborador.
* `GET /metas` - Lista metas conforme perfil e escopo, quando disponível no backend.
* `GET /colaboradores/<int:id>/metas` - Lista metas de um colaborador específico.

### Feedbacks

* `POST /feedbacks` - Registra um feedback estruturado para um colaborador.
* `POST /feedbacks/estruturar` - Estrutura texto de feedback conforme regras do sistema, quando disponível.
* `GET /feedbacks` - Lista feedbacks conforme perfil e escopo, quando disponível no backend.
* `GET /colaboradores/<int:id>/feedbacks` - Lista feedbacks de um colaborador específico, quando disponível.

### PDIs

* `POST /pdis` - Cria um novo Plano de Desenvolvimento Individual.
* `GET /pdis` - Lista PDIs conforme perfil e escopo do usuário autenticado.
* `GET /pdis/<int:pdi_id>` - Retorna detalhes de um PDI e suas ações.
* `PATCH /pdis/<int:pdi_id>` - Atualiza dados editáveis de um PDI, quando disponível.
* `PATCH /pdis/<int:pdi_id>/concluir` - Conclui um PDI, quando as regras de negócio permitirem.
* `PATCH /pdis/<int:pdi_id>/cancelar` - Cancela um PDI, quando permitido.
* `GET /colaboradores/<int:colaborador_id>/pdis` - Lista PDIs de um colaborador específico.
* `POST /pdis/<int:pdi_id>/acoes` - Adiciona uma ação de desenvolvimento a um PDI.
* `GET /pdis/<int:pdi_id>/acoes` - Lista ações de um PDI, quando disponível como rota separada.
* `PATCH /pdis/<int:pdi_id>/acoes/<int:acao_id>` - Atualiza dados editáveis de uma ação, quando disponível.
* `PATCH /pdis/<int:pdi_id>/acoes/<int:acao_id>/concluir` - Conclui uma ação, quando disponível.
* `PATCH /pdis/<int:pdi_id>/acoes/<int:acao_id>/cancelar` - Cancela uma ação, quando disponível.

### Reconhecimentos

* `POST /reconhecimentos` - Registra um reconhecimento formal.
* `GET /reconhecimentos` - Retorna reconhecimentos visíveis para o mural interno, respeitando perfil e escopo de acesso.
* `GET /reconhecimentos/<int:reconhecimento_id>` - Retorna detalhes de um reconhecimento específico.
* `GET /colaboradores/<int:colaborador_id>/reconhecimentos` - Lista reconhecimentos recebidos por um colaborador.
* `PATCH /reconhecimentos/<int:reconhecimento_id>/cancelar` - Cancela um reconhecimento, quando permitido.

### Cadastros Básicos

* `GET /setores` - Lista setores.

* `POST /setores` - Cria um setor.

* `GET /setores/<int:id>` - Retorna detalhes de um setor.

* `PUT /setores/<int:id>` - Atualiza um setor.

* `GET /funcoes` - Lista funções.

* `POST /funcoes` - Cria uma função.

* `GET /funcoes/<int:id>` - Retorna detalhes de uma função.

* `PUT /funcoes/<int:id>` - Atualiza uma função.

* `GET /usuarios` - Lista usuários.

* `POST /usuarios` - Cria um usuário.

* `GET /usuarios/<int:id>` - Retorna detalhes de um usuário.

* `PUT /usuarios/<int:id>` - Atualiza um usuário.

* `GET /competencias` - Lista competências.

* `POST /competencias` - Cria uma competência.

* `GET /competencias/<int:id>` - Retorna detalhes de uma competência.

* `PUT /competencias/<int:id>` - Atualiza uma competência.

> Observação: esta seção deve ser mantida alinhada com as rotas Flask reais. Endpoints marcados como "quando disponível" devem ser confirmados no código antes de uso por integrações externas.

---

## Autenticação, Perfis e Controle de Escopo

O backend utiliza autenticação baseada em JWT. Após o login, o cliente deve enviar o token nas requisições protegidas por meio do cabeçalho:

```http
Authorization: Bearer <token>
```

### Perfis de Acesso

```text
ADMIN
RH
LIDER
COLABORADOR
```

### Regras gerais

* **ADMIN**: perfil previsto para administração completa dos cadastros básicos e dados organizacionais.
* **RH**: perfil previsto para acompanhar colaboradores, avaliações, metas, feedbacks, PDIs, reconhecimentos e indicadores gerais.
* **LIDER**: perfil previsto para atuar sobre colaboradores dentro do seu escopo, normalmente vinculado ao setor.
* **COLABORADOR**: perfil previsto para consultar apenas seus próprios dados e recursos vinculados ao seu colaborador.

### Controle de Escopo

O controle de escopo é centralizado em `AccessScopeService`.

Regras principais:

* usuários `ADMIN` e `RH` possuem visão ampla dos dados organizacionais;
* usuários `LIDER` acessam recursos de colaboradores dentro do seu escopo ou setor;
* usuários `COLABORADOR` acessam apenas recursos vinculados ao próprio `colaborador_id`;
* tentativas de acessar recursos fora do escopo devem retornar `403 Forbidden`.

Endpoints administrativos devem ser revisados periodicamente para garantir que todos possuam proteção explícita de autenticação e autorização no backend.

---

## Banco de Dados e Migrations

O backend utiliza PostgreSQL com SQLAlchemy e Alembic.

Aplicar migrations:

```bash
alembic upgrade head
```

Criar nova migration:

```bash
alembic revision --autogenerate -m "descricao_da_migration"
```

Aplicar migrations via Docker Compose:

```bash
docker compose exec api alembic upgrade head
```

---

## Configuração e Execução

### Variáveis de Ambiente

Crie um arquivo `.env` a partir do modelo base na pasta `backend/`:

```bash
cp .env.example .env
```

As variáveis esperadas devem ser conferidas no arquivo `.env.example`.

Exemplos comuns:

```text
DATABASE_URL
SECRET_KEY
FLASK_APP
FLASK_ENV
CORS_ORIGINS
```

Nunca versione arquivos `.env` com credenciais reais.

---

## Execução Local

A partir da pasta `backend/`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
flask run --port=5000
```

No Windows, a ativação do ambiente virtual pode variar conforme o terminal utilizado.

---

## Execução com Docker

A partir da raiz do monorepo:

```bash
docker compose up --build -d
```

Aplicar migrations no container da API:

```bash
docker compose exec api alembic upgrade head
```

Ver logs:

```bash
docker compose logs -f api
```

Encerrar ambiente:

```bash
docker compose down
```

---

## Health Check

Com a API em execução:

```bash
curl http://localhost:5000/health
```

Resposta esperada:

```json
{
  "status": "ok"
}
```

---

## Testes Automatizados

Executar testes localmente, a partir de `backend/`:

```bash
pytest
```

Executar testes via Docker, a partir da raiz do monorepo:

```bash
docker compose exec api pytest
```

Gerar relatório de cobertura:

```bash
pytest --cov=. --cov-report=term-missing
```

---

## Convenções Técnicas

* Rotas Flask não devem conter regra de negócio complexa.
* Regras de domínio devem permanecer em `domain/`.
* Casos de uso devem coordenar fluxos em `application/`.
* A infraestrutura deve implementar acesso a banco e detalhes técnicos.
* A interface deve validar requisições e serializar respostas.
* Não retornar `senha_hash` em respostas da API.
* Não versionar `.env` real.
* Manter migrations revisadas antes de aplicar.
* Documentar endpoints novos quando forem implementados.
