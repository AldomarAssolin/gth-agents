# GTH Agents - Backend MVP

Este documento apresenta a visão geral do MVP backend do sistema GTH Agents.

## Visão Geral e Objetivo

O **GTH Agents** é uma plataforma inteligente para Gestão de Talento Humano (GTH) focada no ambiente industrial e orientada a dados. Ele consolida o cadastro de colaboradores, o registro de avaliações de competências, o cálculo de médias de desenvolvimento, a classificação do perfil de talentos, a definição de metas de melhoria, o acompanhamento de PDIs (Planos de Desenvolvimento Individual), o registro de reconhecimentos e feedbacks estruturados, permitindo uma análise clara da evolução técnica e comportamental de cada colaborador.

## Arquitetura

O sistema é construído utilizando os princípios de **Clean Architecture**, dividindo o projeto nas seguintes camadas bem definidas:

1. **Domain**: Contém as entidades ricas do sistema (como `Colaborador`, `Meta`, `Reconhecimento`, `PDI`), regras de negócio centrais, enums e serviços de domínio (como a `CalculadoraCompetencias` e `ClassificadorTalento`). Não possui dependência com frameworks.
2. **Application**: Define os casos de uso do sistema (como `CriarMetaUC`, `ConsultarDashboardMVP_UC`, `ListarReconhecimentosUC`), as interfaces/ports para repositórios e Unit of Work, e DTOs de dados.
3. **Infrastructure**: Implementa a infraestrutura técnica concreta, incluindo o mapeamento ORM (SQLAlchemy Models e Mappers), implementações concretas de repositórios SQL, o gerenciador de transações (`UnitOfWorkSQLAlchemy`), migrações de banco (`Alembic`) e criptografia.
4. **Interface**: Camada de fronteira do sistema, contendo as rotas HTTP (Flask Blueprints), os schemas de serialização/validação dos dados e middlewares de segurança (autenticação JWT e autorização por perfis).

## Tecnologias

- **Python 3.12/3.13** como linguagem principal.
- **Flask** para a API REST.
- **SQLAlchemy** e **Alembic** para mapeamento relacional e migrações.
- **PostgreSQL** (produção/desenvolvimento local via Docker) e **SQLite** (banco em memória para suite de testes).
- **Docker** e **Docker Compose** para containerização.
- **Pytest** para suite de testes automatizados.
- **JWT (JSON Web Tokens)** para autenticação sem estado.

## Módulos Implementados no MVP

- **Autenticação**: Registro de usuários, hash seguro de senhas com `pbkdf2:sha256` e autenticação com JWT.
- **Estruturas Organizacionais**: Cadastro de setores e funções de trabalho (ex: Soldagem, Montagem).
- **Colaboradores**: Cadastro geral de colaboradores, status de ativação (`ATIVO`, `INATIVO`, `AFASTADO`, `DESLIGADO`).
- **Competências**: Mapeamento de competências categorizadas por tipos (`TECNICA`, `COMPORTAMENTAL`, `LIDERANCA`, `ORGANIZACIONAL`) com pesos para cálculo de avaliações.
- **Avaliações**: Registro de notas de competências por colaborador e cálculo automático de médias.
- **Perfil de Talento**: Geração dinâmica de classificação baseada em matrizes de potencial e desempenho (ex: `ESPECIALISTA_TECNICO`, `POTENCIAL_LIDER`, `ALTA_PERFORMANCE`).
- **Metas**: Controle de objetivos práticos de evolução, com prazos e status.
- **Feedbacks**: Registro e estruturação inteligente de feedbacks (pontos positivos, pontos de melhoria e ações recomendadas).
- **Plano de Desenvolvimento Individual (PDI)**: Criação de planos de desenvolvimento contendo ações práticas (`LEITURA`, `TREINAMENTO`, `PRATICA_SUPERVISIONADA`, etc.) com prazos, status e origem rastreável.
- **Reconhecimentos**: Mapeamento de conquistas do colaborador vinculadas a feedbacks positivos ou metas atingidas, suportando cancelamento lógico.
- **Evolução do Colaborador**: Visão unificada individual que agrupa todo o histórico e indicadores.
- **Dashboard Geral**: Painel consolidado para liderança e RH contendo o panorama completo de colaboradores e metas.

---

## Como Executar o Projeto Localmente

### Pré-requisitos
Certifique-se de ter o Docker e Docker Compose instalados na máquina.

### 1. Subir a Aplicação
Execute o comando abaixo na raiz do repositório para baixar as imagens necessárias, compilar e iniciar os containers do banco de dados PostgreSQL e do servidor Flask:
```bash
docker compose up --build
```
A API estará rodando no endereço `http://localhost:5000` (ou porta configurada no seu arquivo `.env`).

### 2. Rodar as Migrações do Banco de Dados
Para atualizar o banco de dados local com as últimas tabelas criadas no código:
```bash
docker compose run --rm -e PYTHONPATH=. api alembic upgrade head
```

### 3. Executar os Testes Automatizados
Para garantir a integridade do código e que todas as funcionalidades estão operacionalmente verdes, execute a suíte de testes com o pytest:
```bash
docker compose run --rm -e PYTHONPATH=. api pytest
```
Para rodar um teste específico, você pode usar:
```bash
docker compose run --rm -e PYTHONPATH=. api pytest tests/test_dashboard_mvp.py
```
