# GTH Agents

## Sistema Inteligente de Gestão do Talento Humano

O GTH Agents é uma plataforma de Gestão do Talento Humano desenvolvida para apoiar líderes, gestores e profissionais de RH na identificação, desenvolvimento e acompanhamento de colaboradores.

O sistema utiliza uma arquitetura baseada em agentes especializados para transformar avaliações, feedbacks e competências em informações estratégicas para tomada de decisão.

O objetivo é substituir processos informais, planilhas dispersas e avaliações subjetivas por um fluxo estruturado de desenvolvimento humano orientado por dados.

---

# Problema

Em muitas organizações, especialmente no ambiente industrial, o desenvolvimento de pessoas ainda depende fortemente da percepção individual dos líderes.

Isso gera dificuldades como:

* Falta de critérios claros para avaliação.
* Dificuldade em identificar talentos.
* Ausência de planos de desenvolvimento.
* Feedbacks inconsistentes.
* Falta de histórico evolutivo.
* Promoções baseadas apenas em percepção subjetiva.

O GTH Agents foi criado para enfrentar esses desafios.

---

# Objetivos do Projeto

* Centralizar informações sobre colaboradores.
* Estruturar avaliações de competências.
* Identificar talentos e potenciais lideranças.
* Gerar perfis de desenvolvimento.
* Apoiar líderes na tomada de decisão.
* Promover uma cultura de melhoria contínua.
* Criar base para iniciativas de Gestão de Pessoas alinhadas à Indústria 4.0.

---

# Fluxo Principal

O sistema segue o fluxo abaixo:

```text
Cadastro do Colaborador
          ↓
Avaliação de Competências
          ↓
Análise das Competências
          ↓
Classificação do Perfil de Talento
          ↓
Definição de Metas
          ↓
Registro de Feedbacks
          ↓
Acompanhamento da Evolução
```

---

# Agentes do MVP

A primeira versão do sistema utiliza agentes determinísticos para análise e classificação.

## Agente Avaliador

Analisa competências avaliadas e calcula:

* Média Técnica
* Média Comportamental
* Média de Liderança
* Média Geral

---

## Agente Perfilador

Classifica o colaborador em categorias como:

* Alta Performance
* Potencial Líder
* Especialista Técnico
* Talento em Desenvolvimento
* Necessita Desenvolvimento

---

## Agente Gerador de Metas

Sugere ações de desenvolvimento com base nos resultados das avaliações.

---

## Agente Estruturador de Feedback

Transforma observações livres em feedbacks estruturados contendo:

* Ponto positivo
* Ponto de melhoria
* Ação recomendada

---

# Arquitetura

O projeto segue princípios de Clean Architecture.

```text
Interface
    ↓
Application
    ↓
Domain
    ↓
Infrastructure
```

## Domain

Responsável pelas regras de negócio.

```text
domain/
├── entities
├── enums
└── services
```

---

## Application

Responsável pelos casos de uso e serviços da aplicação.

```text
application/
├── dtos
├── errors
├── ports
├── services (agents.py)
└── use_cases
```

---

## Infrastructure

Responsável pela persistência, mappers e controle transacional.

```text
infrastructure/
├── database
├── mappers
├── repositories
└── unit_of_work_sqlalchemy.py
```

---

## Interface

Responsável pela API HTTP e serialização.

```text
interface/
├── routes
├── schemas
└── error_handler
```

---

# Tecnologias

* Python 3.13
* Flask
* SQLAlchemy 2.x
* PostgreSQL
* Alembic
* Docker
* Docker Compose

---

# Executando o Projeto

## Subir aplicação

```bash
docker compose up --build
```

API disponível em:

```text
http://localhost:5000
```

---

## Parar aplicação

```bash
docker compose down
```

---

# Migrations

Criar migration:

```bash
alembic revision --autogenerate -m "initial schema"
```

Aplicar migration:

```bash
alembic upgrade head
```

---

# Endpoints Principais

## Cadastros

```text
GET  /health

GET  /usuarios
POST /usuarios

GET  /setores
POST /setores

GET  /funcoes
POST /funcoes

GET  /colaboradores
POST /colaboradores

GET  /competencias
POST /competencias
```

---

## Gestão de Talentos

```text
GET  /avaliacoes
POST /avaliacoes

GET  /colaboradores/{id}/perfil

GET  /colaboradores/{id}/evolucao

GET  /colaboradores/{id}/metas
POST /metas

GET  /feedbacks
POST /feedbacks

POST /feedbacks/estruturar
```

---

# Status Atual

## MVP v0.1.0

Implementado:

* Cadastro de usuários.
* Cadastro de setores.
* Cadastro de funções.
* Cadastro de competências.
* Cadastro de colaboradores.
* Avaliação de competências.
* Geração de perfil de talento.
* Registro de metas.
* Registro de feedbacks.
* Estrutura inicial dos agentes.

Em evolução:

* Correção do cálculo por tipo de competência.
* Hash seguro de senhas.
* Autenticação JWT.
* Dashboard Web.
* Agentes baseados em IA.

---

# Roadmap

## MVP

* Gestão de competências.
* Perfil de talento.
* Metas.
* Feedbacks.

## Versão 1.0

* JWT.
* Controle de acesso.
* Dashboard gerencial.
* Indicadores de RH.

## Versão 2.0

* Agente Avaliador IA.
* Agente Perfilador IA.
* Agente Gerador de Metas IA.
* Plano de Desenvolvimento Individual (PDI).
* Reconhecimento e recompensa.
* Potencial de liderança.

---

# Autor

Aldomar Assolin

Técnico em Soldagem | Tecnólogo em Análise e Desenvolvimento de Sistemas | Pós-graduação em Gestão da Indústria 4.0

Projeto desenvolvido com foco na integração entre Gestão de Pessoas, Tecnologia e Indústria 4.0.
