# GTH Agents - Backend MVP (v1.0.0-mvp-backend)

## Sistema Inteligente de Gestão do Talento Humano

O GTH Agents é uma plataforma de Gestão do Talento Humano desenvolvida para apoiar líderes, gestores e profissionais de RH na identificação, desenvolvimento e acompanhamento de colaboradores.

O sistema utiliza uma arquitetura baseada em agentes especializados para transformar avaliações, feedbacks e competências em informações estratégicas para a tomada de decisão, eliminando processos informais e subjetivos no desenvolvimento humano organizacional.

---

## Tecnologias Utilizadas

- **Core**: Python 3.12, Flask
- **Banco de Dados & ORM**: PostgreSQL, SQLAlchemy 2.x, Alembic Migrations
- **Autenticação**: PyJWT
- **Ambiente**: Docker, Docker Compose
- **Testes**: Pytest, Pytest-Cov

---

## Arquitetura

O projeto é estruturado seguindo os princípios de **Clean Architecture**, dividindo o sistema nas seguintes camadas:

1. **Domain**: Contém as entidades de negócio, enums e serviços puros de domínio.
2. **Application**: Contém os Casos de Uso (Use Cases), DTOs de entrada e saída, portas/interfaces dos repositórios e serviços de agentes.
3. **Infrastructure**: Implementações concretas de repositórios SQLAlchemy, Unit of Work, serviço de segurança JWT e persistência.
4. **Interface**: Controladores/rotas HTTP do Flask, serializadores e esquemas Marshmallow, além do manipulador de erros (Error Handler).

---

## Pré-requisitos

Para rodar este projeto, você precisa ter instalado na sua máquina:
- **Docker** e **Docker Compose**
- **Git**

---

## Configuração e Inicialização do Projeto

Siga os passos abaixo para preparar e executar o projeto localmente:

### 1. Configurar o Ambiente (.env)

Copie o arquivo `.env.example` para `.env`:
```bash
cp .env.example .env
```
*(Nota: Ajuste os valores no arquivo `.env` caso queira customizar as credenciais locais do banco de dados ou a chave secreta JWT)*

### 2. Subir os Containers do Docker

Execute o comando para compilar a imagem e iniciar os serviços do banco e do Flask:
```bash
docker compose up -d --build
```
Após o build, a API estará escutando na porta **5000** (`http://localhost:5000`).

### 3. Executar Migrações do Banco de Dados

Rode as migrations do Alembic para criar todas as tabelas necessárias no PostgreSQL:
```bash
docker compose run --rm -e PYTHONPATH=. api alembic upgrade head
```

### 4. Verificar a Saúde do Servidor (Health Check)

Você pode acessar o seguinte endpoint no seu navegador ou via terminal para garantir que a API está respondendo e conectando ao banco de dados:
```bash
curl http://localhost:5000/health
```
Resposta esperada:
```json
{"status": "ok"}
```

---

## Execução de Testes Automatizados e Cobertura

Para executar a suite completa de testes contendo 126 testes de integração e unitários, utilize o comando abaixo:
```bash
docker compose run --rm -e PYTHONPATH=. api pytest
```

### Relatório de Cobertura de Código

Para gerar o relatório detalhado de cobertura de testes (atualmente em **90%** do projeto), execute:
```bash
docker compose run --rm -e PYTHONPATH=. api pytest --cov=. --cov-report=term-missing
```

---

## Documentação Completa da API

A documentação detalhada do MVP backend foi dividida nos seguintes arquivos na pasta `docs/`:

- **[Visão Geral do Backend](docs/MVP_BACKEND.md)**: Visão de arquitetura, stack de tecnologias e guias do ambiente.
- **[Autenticação e Escopos](docs/AUTH.md)**: Fluxo do Token JWT, matriz de permissões por perfil (RBAC) e lógica detalhada do controle de escopo (AccessScopeService).
- **[Contratos de Endpoints](docs/API.md)**: Lista completa e detalhada de rotas HTTP com payloads reais de Request e Response JSON.
- **[Fluxo de Teste Manual (Postman)](docs/POSTMAN_FLOW.md)**: Roteiro passo a passo para execução sequencial e teste manual ponta a ponta.

A coleção e variáveis do Postman estão salvas no diretório `postman/`.

---

## Release MVP (v1.0.0-mvp-backend)

Esta versão oficializa o fechamento da primeira entrega funcional do backend do GTH Agents, integrando todos os requisitos do MVP:
- Controle de acesso fino por escopo (líderes restringidos ao setor, colaboradores aos próprios dados).
- Agentes de cálculo ponderado de competências e perfil de talentos.
- Fluxos completos de PDI, Metas, Feedbacks estruturados e Reconhecimentos rastreáveis.

---

## Autor

**Aldomar Assolin**
*Técnico em Soldagem | Tecnólogo em Análise e Desenvolvimento de Sistemas | Pós-graduação em Gestão da Indústria 4.0*
