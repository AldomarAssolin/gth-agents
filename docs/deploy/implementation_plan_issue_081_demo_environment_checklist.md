# Plano de Implementação — Checklist de Ambiente Demo (Issue #081)

Este plano define a estrutura, os pré-requisitos, as diretrizes de segurança e os procedimentos de validação para a criação do checklist de preparação de um ambiente de demonstração controlado para a plataforma GTH Agents.

---

## User Review Required

> [!IMPORTANT]
> **BLOQUEIO: Seed de Demonstração Controlado Não Disponível**
> O arquivo `backend/seed_db.py` atual remove registros das tabelas por meio de operações `.delete()` executadas em ordem compatível com as dependências entre as entidades e, em seguida, carrega dados estáticos de desenvolvimento.
> Esse script atual não deve ser executado em um ambiente demo existente sem confirmação explícita de que o banco de dados pode ser completamente recriado. Ele deve ser tratado estritamente como ferramenta de desenvolvimento local, e não como procedimento seguro de inicialização de ambiente demo.
> Recomendamos a criação de uma issue futura para construir um script de seed parametrizável exclusivo para demonstração (ex: `backend/seed_demo.py`), que evite a remoção destrutiva de dados se executado acidentalmente em ambientes inadequados, e utilize credenciais dinâmicas ou parametrizáveis.

> [!WARNING]
> **Segurança de Credenciais no Guia**
> Conforme as regras de segurança especificadas na issue, todas as variáveis de ambiente e segredos no checklist usarão apenas placeholders genéricos (ex: `SECRET_KEY=<valor-seguro>`). Nenhuma credencial real ou padrão de desenvolvimento será exposta na documentação.

---

## Decisões adotadas

### Backup

Nesta issue serão documentados apenas procedimentos genéricos de backup e restauração utilizando `pg_dump` e `pg_restore`.

O checklist deverá exigir que a restauração seja testada de forma prática pelo operador, pois a simples criação de um arquivo de backup não comprova sua recuperabilidade.

Permanecem fora do escopo desta issue:
- upload automático para S3, Object Storage ou serviço equivalente;
- agendamento automático;
- política de retenção;
- criptografia externa;
- replicação;
- integração com serviços gerenciados de backup.

Esses itens deverão ser tratados em issue futura, caso sejam necessários.

### CORS

O checklist utilizará origens completas e explicitamente autorizadas por meio da variável de ambiente `CORS_ORIGINS`.

Não serão recomendados:
- `CORS_ORIGINS=*`;
- wildcard global;
- wildcard de subdomínio;
- liberação automática de qualquer origem.

Cada origem permitida deverá ser declarada explicitamente pelo operador conforme a topologia real do ambiente.

Exemplo genérico:
```env
CORS_ORIGINS=https://demo.exemplo.com
```

---

## Proposed Changes

### Documentation (docs/deploy/)

Criação da documentação de deploy e checklist de ambiente na pasta dedicada `docs/deploy/`.

---

#### [MODIFY] [implementation_plan_issue_081_demo_environment_checklist.md](docs/deploy/implementation_plan_issue_081_demo_environment_checklist.md)
* Este arquivo de planejamento contendo o desenho atualizado da solução documental.

#### [NEW] [checklist_demo_environment.md](docs/deploy/checklist_demo_environment.md)
* O documento principal contendo as instruções reproduzíveis divididas em 20 seções, conforme o escopo da issue.

#### [NEW] [walkthrough_issue_081_demo_environment_checklist.md](docs/deploy/walkthrough_issue_081_demo_environment_checklist.md)
* O walkthrough registrando os arquivos criados, as fontes inspecionadas e os comandos reais validados durante o processo.

---

## Estado Atual do Repositório (Inspeção)

A tabela abaixo resume as descobertas da auditoria estrutural e de arquivos realizada no repositório:

| Item | Arquivo ou origem | Estado encontrado | Implicação para demo |
| :--- | :--- | :--- | :--- |
| **Variáveis backend** | `backend/.env.example` e `docker-compose.yml` | `FLASK_APP`, `FLASK_ENV`, `SECRET_KEY`, `DATABASE_URL`, `JWT_SECRET_KEY`, `JWT_ALGORITHM`, `JWT_EXPIRES_MINUTES`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `CORS_ORIGINS` | Devem receber valores seguros e restritivos fora do Git para o ambiente demo. |
| **Variáveis frontend** | `frontend/.env.example` e `docker-compose.yml` | `VITE_API_URL` | Deve apontar explicitamente para o endpoint HTTP/HTTPS público ou privado da API da demo. |
| **CORS** | `backend/app.py` | Configurado dinamicamente com base em `CORS_ORIGINS` (default: `http://localhost:5173`). | Exige a declaração exata da origem do frontend (sem wildcard). |
| **Health Check** | `backend/interface/routes/health_routes.py` | Rota `GET /health` responde `{"status": "ok"}` | Funciona como **liveness básica** da API Flask. Não garante a conectividade com banco de dados ou prontidão funcional do frontend (não é readiness completa). |
| **Seed** | `backend/seed_db.py` | Realiza `.delete()` por entidade em ordem de dependência e carrega dados com credenciais estáticas e inadequadas para demonstração. | **BLOQUEIO para demo**. Não rodar em ambiente existente sem garantia de descarte completo. |
| **Portas internas** | `docker-compose.yml` e Dockerfiles | API Flask expõe `5000`. Frontend Dev expõe `5173`. Frontend Prod (Nginx) expõe `80` internamente. DB PostgreSQL usa a porta interna `5432`. | A porta pública ou domínio dependem da infraestrutura de rede externa, proxies reversos ou balanceadores (não expor Postgres publicamente). |
| **Build de Produção** | `frontend/Dockerfile.prod` e `nginx.conf` | `Dockerfile.prod` (Nginx + React build) e `nginx.conf` com fallback para SPA (`try_files`) presentes. | Permite a geração de build minificado estático otimizado para o demo. |
| **Composição Docker** | Diretório raiz e subpastas | `docker-compose.yml` na raiz, `/backend` e `/frontend` | **LACUNA IDENTIFICADA**: Não foi encontrada uma composição Docker específica para ambiente demo. O `docker-compose.yml` atual deve ser tratado como ambiente de desenvolvimento local. A criação de uma composição demo será tratada em issue futura. |
| **Testes** | `backend/tests/` | 208 testes integrados/unitários automatizados com pytest. | Devem ser validados localmente antes do empacotamento, mas não executados diretamente no ambiente demo. |

---

## Classificação dos comandos documentados

Para garantir a segurança e reprodutibilidade, os comandos citados no checklist definitivo serão divididos entre confirmados e exemplos genéricos:

### Comandos confirmados contra o repositório
São comandos cuja execução local no repositório foi validada e está mapeada aos diretórios específicos:
- **docker compose config** (executado na raiz do monorepo para validar a sintaxe da infraestrutura Docker).
- **docker compose build** e **docker compose up -d** (na raiz, para subir a pilha de desenvolvimento/inspeção).
- **docker compose ps** e **docker compose logs** (para monitorar a saúde e saída dos containers reais `api`, `web` e `db`).
- **alembic upgrade head** e **alembic current** (dentro do diretório `/backend` ou usando `docker compose exec api alembic...` com `FLASK_APP=app:create_app`).
- **pytest** (executado com `PYTHONPATH=. .venv/bin/pytest` no diretório `/backend` para validar regressões locais).
- **npm run lint** e **npm run build** (no diretório `/frontend` para validar sintaxe JavaScript e compilar os estáticos).
- **curl http://localhost:5000/health** (para testar a resposta do processo HTTP da API).

### Exemplos genéricos não executados
Comandos de infraestrutura externa e de utilitários que serão apresentados apenas como modelos placeholder no checklist:
- Execução de `pg_dump` e `pg_restore` contra host/banco remoto (com usuário, senha e host parametrizados genericamente).
- Configuração de URL HTTPS pública, certificados TLS via Let's Encrypt / Certbot, ou configurações de Proxy Reverso no Nginx externo.
- Ações de rollback de infraestrutura cloud ou de rede.

---

## Limites do ambiente demo

O checklist de ambiente demo declarará explicitamente os seguintes limites operacionais e de infraestrutura:
- O ambiente demo **não é produção** e não deve conter dados pessoais ou corporativos reais.
- O modo `debug` da API deve estar estritamente desativado (`FLASK_ENV=production` ou `FLASK_DEBUG=0`).
- Todas as chaves secretas (`SECRET_KEY`, `JWT_SECRET_KEY`) devem permanecer fora do código e do Git (configuradas exclusivamente via ambiente).
- As credenciais estáticas de desenvolvimento devem ser completamente substituídas no banco.
- O banco de dados deve estar isolado logicamente ou fisicamente das demais instâncias.
- CORS deve utilizar apenas origens explicitamente autorizadas na variável `CORS_ORIGINS`.
- O banco PostgreSQL não deve possuir exposição pública para a Internet (porta `5432` fechada na borda externa).
- Os logs da API não devem registrar parâmetros sensíveis (como payloads de login, tokens JWT ou cabeçalhos `Authorization`).
- Os backups gerados devem ter a sua restauração testada periodicamente em uma máquina isolada.
- O acesso à URL do frontend demo deve ser restrito aos participantes autorizados da demonstração.
- Não há garantia contratual de alta disponibilidade ou políticas de disaster recovery automático (como replicação multi-região) estabelecidas nesta issue.

---

## Riscos e Mitigações

| Risco | Como o checklist mitiga / registra |
| :--- | :--- |
| **Execução acidental do seed destrutivo** | O checklist proibirá explicitamente rodar `seed_db.py` em ambientes demo existentes com dados ativos e marcará o script atual com o aviso formal de `BLOQUEIO`. |
| **Uso de credenciais estáticas / fracas** | O checklist exigirá a alteração imediata de senhas padrão e fornecerá comandos genéricos para atualização de hashes de senha. |
| **CORS permissivo (`*`)** | O guia instruirá a recusa de wildcards na variável `CORS_ORIGINS`. |
| **PostgreSQL publicamente exposto** | Instrução de desativação do mapeamento de porta externa `5432:5432` no Docker Compose demo. |
| **Confusão entre portas internas e públicas** | Detalhará claramente que a API escuta na `5000` interna e o Frontend na `80` interna (Nginx), devendo o proxy reverso mapear as portas externas apropriadas (ex: 80/443 públicas). |
| **Log de dados sensíveis** | O checklist incluirá um passo para inspecionar logs do container e garantir que segredos ou cabeçalhos HTTP privados não estejam vazando no console. |
| **Falha silenciosa de backup** | O checklist pós-deploy exigirá a validação prática da integridade do arquivo gerado pelo `pg_dump` restaurando-o localmente em container temporário. |

---

## Issue futura recomendada

### Criação de Seed de Demonstração Controlado
Propõe-se a criação de um script de inicialização específico, por exemplo, `backend/seed_demo.py`, com o seguinte escopo:
- Utilizar apenas dados fictícios estruturados em cenários de negócio realistas.
- Evitar limpeza destrutiva por padrão (não rodar `.delete()` cegamente em cascata sem confirmação explícita do operador).
- Ser idempotente ou realizar validação de dados existentes para evitar duplicidade.
- Não conter credenciais fracas ou chaves privadas fixas no Git (ler do ambiente).
- Criar a matriz completa de perfis (`ADMIN`, `RH`, `LIDER`, `COLABORADOR`).
- Gerar dados históricos coerentes para popular o dashboard MVP, avaliações de competência, metas, PDIs, feedbacks e reconhecimentos.
- Impedir execução se detectar variáveis de ambiente associadas a produção.

---

## Verification Plan

### Validação estrutural e documental
Para verificar as entregas e garantir que não haja vazamentos locais, os seguintes comandos devem ser rodados localmente antes da submissão:

1. **Estrutura de arquivos criados**:
   ```bash
   find docs/deploy -maxdepth 1 -type f | sort
   ```
2. **Auditoria de caminhos absolutos locais**:
   ```bash
   grep -R -n -E "/home/|/Users/|C:\\\\Users\\\\" docs/deploy/ --include="*.md"
   ```
   *Resultado esperado*: nenhuma linha encontrada.
3. **Auditoria de credenciais ou padrões locais**:
   ```bash
   grep -R -n -E "admin123|dev-secret-change-me|postgres:postgres|Bearer [A-Za-z0-9._-]+" docs/deploy/ --include="*.md"
   ```
   *Nota*: As eventuais correspondências devem ser revisadas e permitidas apenas se estiverem descritas como exemplos conceituais de aviso/bloqueio.
4. **Validação da sintaxe do Compose**:
   ```bash
   docker compose config
   ```
5. **Checagem de lint e espaçamento no repositório**:
   ```bash
   git diff --check
   ```
6. **Presença das 20 seções obrigatórias**:
   ```bash
   grep -n "^## " docs/deploy/checklist_demo_environment.md
   ```
7. **Revisão de links relativos**:
   *Os links relativos foram revisados por inspeção estrutural.*

---

## Revisão documental

O processo de validação manual será substituído por uma **revisão documental** rigorosa dos arquivos gerados, verificando os seguintes pontos:
- Títulos e sequência das 20 seções obrigatórias no checklist final.
- Ausência de credenciais reais ou chaves expostas (uso estrito de placeholders).
- Separação visível e nítida de comandos confirmados e de exemplos genéricos.
- Coerência dos links relativos Markdown na pasta `docs/deploy/`.
- Diferenciação nítida dos escopos locais, de demonstração e de produção.
- Marcação de bloqueio no seed atual.
- Confirmação explícita de que nenhum deploy real foi efetuado.
