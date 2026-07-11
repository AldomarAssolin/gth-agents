# Checklist de Preparação de Ambiente Demo

Este documento apresenta um guia técnico, seguro e reproduzível para a preparação e validação planejada e validação operacional de um ambiente de demonstração controlado para o **GTH Agents**.

---

## 1. Objetivo

Fornecer orientações padronizadas para implantar a pilha de serviços do GTH Agents em ambiente de demonstração (demo), visando a validação funcional por stakeholders e equipes de RH de forma isolada, sem expor dados reais ou comprometer a segurança das credenciais.

---

## 2. Limites do ambiente demo

O ambiente de demonstração possui limites rígidos de operação que o diferenciam de uma infraestrutura de produção:
- **Dados Reais Proibidos**: Sob nenhuma circunstância utilize CPFs, nomes, e-mails ou dados corporativos reais de colaboradores. Utilize exclusivamente dados gerados de forma fictícia.
- **Segurança de Borda**: O banco de dados PostgreSQL não deve ter sua porta exposta para redes públicas.
- **Ausência de SLA / Resiliência**: O ambiente demo não prevê alta disponibilidade ativa, replicação de banco de dados geográfica ou redundância de múltiplos containers da API.
- **Segredos Isolados**: Todas as credenciais de desenvolvimento (`dev-secret-change-me`, etc.) devem ser substituídas por segredos novos gerados no deploy.

---

## 3. Matriz comparativa

A tabela abaixo compara as principais características de configuração entre os três ambientes possíveis do projeto GTH Agents:

| Característica | Ambiente Local (Desenvolvimento) | Ambiente Demo (Demonstração) | Ambiente de Produção |
| :--- | :--- | :--- | :--- |
| **Público-alvo** | Desenvolvedores da equipe core | Stakeholders, RH e clientes em validação | Usuários finais da corporação |
| **Modo Debug (Flask)** | Habilitado (`FLASK_ENV=development`) | Desativado (`FLASK_ENV=production`) | Desativado (`FLASK_ENV=production`) |
| **Banco de Dados** | PostgreSQL em container de dev | PostgreSQL isolado em container ou instância dedicada ao ambiente demo | Instância gerenciada na nuvem (RDS, Cloud SQL) |
| **CORS** | Permitido `http://localhost:5173` | Origem explícita (ex: `https://demo.exemplo.com`) | Origens corporativas restritas e auditadas |
| **Portas Expostas** | Mapeamento completo no host (5000, 5173, 5432) | Apenas API (5000) e Web (80/443). Postgres fechado | Apenas porta HTTP/HTTPS pública do balanceador de carga |
| **Health Check** | Apenas liveness visual básica | Liveness básica com monitoramento de conexões | Liveness + Readiness completas no orquestrador |
| **Seed de Dados** | Execução automática de `seed_db.py` | Dados simulados, sem apagar base existente | Proibido seed padrão (cargas via migrações formais) |
| **HTTPS / TLS** | Opcional (HTTP puro) | obrigatório quando exposto fora de uma rede controlada (via Proxy Reverso/Certbot) | Gerenciado por infraestrutura cloud (ACM/Vault) |
| **Backup** | Não aplicável | pg_dump manual e restauração testada localmente | pg_dump automatizado com retenção e criptografia |

---

## 4. Pré-requisitos

Para preparar a infraestrutura básica do ambiente demo, garanta os seguintes pré-requisitos no host executor:
1. Sistema Operacional Linux (ou qualquer OS compatível com a engine do Docker).
2. **Docker Engine** instalado (versão mínima `20.10.x`).
3. **Docker Compose Plugin** instalado (versão mínima `v2.x`).
4. Utilitários locais `pg_dump` e `pg_restore` (versão 16, compatível com a imagem do PostgreSQL do projeto).
5. Acesso de rede configurado para permitir conexões de entrada nas portas públicas de simulação (ex: `80` ou `443` para o frontend web, `5000` para a API).

---

## 5. Variáveis de ambiente

Crie um arquivo `.env` para o backend e outro para o frontend no ambiente demo, preenchendo os placeholders genéricos com valores seguros gerados na hora:

### Backend (`/backend/.env` do ambiente demo)
```env
FLASK_APP=app:create_app
FLASK_ENV=production
SECRET_KEY=<valor-seguro-gerado-aleatoriamente>
JWT_SECRET_KEY=<valor-seguro-gerado-aleatoriamente>
JWT_ALGORITHM=HS256
JWT_EXPIRES_MINUTES=60
DATABASE_URL=postgresql+psycopg://<usuario-db>:<senha-db>@<host-db>:5432/<nome-db>
CORS_ORIGINS=https://demo.exemplo.com
POSTGRES_DB=<nome-db>
POSTGRES_USER=<usuario-db>
POSTGRES_PASSWORD=<senha-db>
```

### Frontend (`/frontend/.env` do ambiente demo)
```env
VITE_API_URL=https://api-demo.exemplo.com
```

### Injeção das variáveis no container da API

A criação do arquivo `backend/.env` não disponibiliza automaticamente suas
variáveis ao container `api`.

O serviço deve carregar explicitamente as configurações por meio de:

- `env_file`; ou
- entradas individuais em `environment`.

Antes da preparação do ambiente demo, devem ser disponibilizadas ao
container, no mínimo:

- `SECRET_KEY`;
- `DATABASE_URL`;
- `JWT_SECRET_KEY`;
- `JWT_ALGORITHM`;
- `JWT_EXPIRES_MINUTES`;
- `CORS_ORIGINS`.

```yaml
services:
  api:
    env_file:
      - ./backend/.env.demo
    environment:
      FLASK_ENV: production
```

> backend/.env.demo não deve ser versionado

O `docker-compose.yml` atual não deve ser considerado adequado para uma demo
segura sem uma composição adicional ou override.

> [!WARNING]
> Nunca compartilhe ou versiona os arquivos `.env` preenchidos com credenciais reais. Utilize sempre este checklist como referência de placeholders genéricos.

---

## 6. Banco de dados

A configuração do banco de dados para a demonstração deve seguir regras estritas de isolamento:
1. A imagem base deve ser `postgres:16-alpine` conforme configurado no projeto.
2. O banco de dados deve utilizar um volume persistente nomeado para evitar perda de dados em reinicializações do container:
   ```yaml
   volumes:
     - postgres_data:/var/lib/postgresql/data
   ```
3. A porta `5432` não deve ser mapeada para a interface de rede pública do host. Remova a linha `ports: - "5432:5432"` do Docker Compose para que a base permaneça acessível exclusivamente pela rede interna do Docker criada entre o container `api` e o container `db`.

---

## 7. Migrations

As migrações de banco de dados devem ser aplicadas no momento do provisionamento do ambiente demo para criar as tabelas corretas do GTH Agents:
1. Com a pilha de containers ativa, execute o upgrade do Alembic até o último estado (`head`):
   ```bash
   docker compose exec api alembic upgrade head
   ```
2. Confirme que as migrações foram aplicadas corretamente verificando o estado atual do banco:
   ```bash
   docker compose exec api alembic current
   ```
   O hash retornado deve ser igual ao da última migração em `backend/migrations/versions/`.

---

## 8. Seed de demonstração

> [!CAUTION]
> **BLOQUEIO: seed de demonstração controlado ainda não disponível.**
> O arquivo `backend/seed_db.py` atual do projeto remove registros de forma destrutiva via operações `.delete()` e insere credenciais fracas estáticas de desenvolvimento.

**Procedimento seguro de Seed para o ambiente Demo:**
1. O script atual `backend/seed_db.py` **não deve ser executado** em um ambiente demo existente sem confirmação explícita de que o banco pode ser completamente recriado. Ele deve ser tratado estritamente como ferramenta de desenvolvimento local.
2. Na ausência de um script exclusivo `seed_demo.py` parametrizado, o operador deve:
   - Configurar o banco de dados limpo executando apenas as migrations (`alembic upgrade head`).
   - Criar manualmente o usuário administrador inicial direto no banco com uma senha forte ou hash gerado localmente, ou executar o script `seed_db.py` apenas no primeiro provisionamento do banco totalmente vazio, seguido da alteração imediata de todas as senhas geradas por meio de query SQL no banco de dados.

---

## 9. CORS

Para mitigar ataques de requisição cross-origin indevidas no ambiente de demonstração:
1. Defina explicitamente a URL do frontend na variável `CORS_ORIGINS` (ex: `CORS_ORIGINS=https://demo.exemplo.com`).
2. Caso a API e o frontend residam em domínios ou portas distintas, separe-os por vírgula (ex: `https://demo.exemplo.com,https://api-demo.exemplo.com`).
3. **Proibições**: É proibido utilizar `CORS_ORIGINS=*` ou wildcards amplos que aceitem qualquer origem.

---

## 10. Health check

O endpoint `/health` atual da API serve como uma **liveness básica** do processo Flask:
```bash
curl -i https://api-demo.exemplo.com/health
```
Resposta esperada:
```json
{"status": "ok"}
```
> [!NOTE]
> O status `ok` comprova apenas que o servidor web do Flask está ativo e respondendo chamadas HTTP. Ele **não garante** de forma isolada que a conectividade com o banco PostgreSQL está estabelecida ou que as migrations estão atualizadas. Uma validação operacional completa exige a checagem pós-deploy (ver Seção 17).

---

## 11. URL pública ou domínio

Como esta issue não prevê a contratação de domínios públicos ou DNS reais, a simulação do ambiente demo em rede local ou de testes pode utilizar:
- **Resolução Local via Hosts**: Mapeamento IP-Domínio no arquivo `/etc/hosts` da máquina de testes:
  ```text
  127.0.0.1    demo.exemplo.com
  127.0.0.1    api-demo.exemplo.com
  ```
- **Proxy Reverso Local**: Bloco de servidor Nginx configurado localmente para rotear requisições de portas externas padrão (80/443) para os respectivos containers do Docker Compose.

---

## 12. Dados fictícios

Para garantir conformidade com a segurança de dados corporativos no ambiente de demonstração:
1. Nunca execute testes operacionais com informações reais de colaboradores, salários, avaliações reais de desempenho ou feedbacks verídicos.
2. Crie uma planilha auxiliar ou roteiro com nomes fictícios padronizados (ex: "Colaborador Demo A", "Líder Técnico Demo") e use e-mails com domínios de teste (ex: `@demo-exemplo.com`).

---

## 13. Logs mínimos

A inspeção e monitoramento dos logs do GTH Agents no ambiente demo devem seguir regras de sigilo de credenciais:
1. Não configure logs em nível `DEBUG` que registrem payloads completos contendo hashes de senha, senhas em texto puro ou o cabeçalho HTTP `Authorization` contendo tokens JWT de usuários.
2. Comando para verificar logs mínimos em execução:
   ```bash
   docker compose logs --tail=100 -f api
   ```

---

## 14. Backup e restauração

Para garantir a salvaguarda e a reprodutibilidade rápida do ambiente demo, utilize utilitários nativos do PostgreSQL de forma segura:

### Comando de Geração de Backup (`pg_dump`)
Gere o backup do banco `gth_agents` em formato binário comprimido customizado:
```bash
pg_dump -h <host-db> -U <usuario-db> -d <nome-db> -F c -b -v -f /tmp/backup_gth_demo.dump
```

### Comando de Restauração (`pg_restore`)
Restaure a estrutura e dados em um banco limpo:
```bash
pg_restore -h <host-db> -U <usuario-db> -d <nome-db> -v --clean --no-owner --no-privileges /tmp/backup_gth_demo.dump
```

> [!IMPORTANT]
> **Validação Prática da Restauração**
> O operador do ambiente demo deve validar a integridade do dump restaurando-o em um container PostgreSQL temporário isolado de testes antes de considerar o backup finalizado com sucesso.

---

## 15. Comandos de validação

Os seguintes comandos reais do repositório devem ser utilizados para validar a integridade local da aplicação antes e durante o processo de preparação:

- **Validar configurações do Compose**:
  ```bash
  docker compose config
  ```
- **Compilar e buildar imagens locais**:
  ```bash
  docker compose build
  ```
- **Iniciar containers em background**:
  ```bash
  docker compose up -d
  ```
- **Verificar status dos serviços Docker**:
  ```bash
  docker compose ps
  ```
- **Checar migrações aplicadas no container**:
  ```bash
  docker compose exec api alembic current
  ```
- **Executar a suíte de testes de regressão (backend)**:
  ```bash
  docker compose exec api pytest
  ```
- **Checar lint do frontend**:
  ```bash
  npm run lint --prefix frontend
  ```
- **Executar build de produção do frontend localmente**:
  ```bash
  npm run build --prefix frontend
  ```

---

## 16. Checklist pré-deploy

Antes de iniciar os serviços no host de destino do ambiente demo, certifique-se de marcar cada item como verificado:
- [ ] O arquivo `.env` do backend foi gerado e preenchido com senhas e chaves exclusivas seguras, sem credenciais padrão.
- [ ] O arquivo `.env` do frontend aponta corretamente para a URL externa ou domínio planejado para a API.
- [ ] O mapeamento de porta externa `5432:5432` do PostgreSQL foi removido do arquivo Compose para impedir exposição na borda.
- [ ] O modo de desenvolvimento/debug foi desligado no backend (`FLASK_ENV=production`).
- [ ] A configuração do CORS em `CORS_ORIGINS` não utiliza wildcard (`*`).
- [ ] O backup do banco de demonstração anterior (se houver) foi executado e sua restauração validada em ambiente isolado.

---

## 17. Checklist pós-deploy

Após subir a pilha do GTH Agents no host da demonstração, execute a lista completa de validação operacional:
- [ ] **Serviços ativos**: Containers `api`, `web` e `db` constam com status `Up` ou `healthy` no `docker compose ps`.
- [ ] **Liveness básica**: `GET /health` responde HTTP 200 com JSON `{"status": "ok"}`.
- [ ] **Banco acessível**: Logs da API não exibem erros de conexão de banco (`ConnectionRefusedError`, etc.).
- [ ] **Migrations confirmadas**: A saída de `alembic current` corresponde ao último hash da pasta de migrations do backend.
- [ ] **Frontend acessível**: O painel web carrega no navegador através da URL ou domínio simulado.
- [ ] **Autenticação**: O login falha ao enviar credenciais incorretas (HTTP 401) e funciona ao enviar credenciais corretas (HTTP 200), retornando o JWT de acesso.
- [ ] **Escopo de RH/ADMIN**: Usuário RH consegue listar todos os colaboradores da base.
- [ ] **Escopo de LIDER**: Usuário LIDER tem acesso de listagem apenas para colaboradores de seu respectivo setor. Requisições para setores externos retornam HTTP 403.
- [ ] **Escopo de COLABORADOR**: Usuário COLABORADOR consegue consultar apenas o seu próprio perfil e histórico. Requisições a endpoints com IDs de outros colaboradores retornam HTTP 403.
- [ ] **Metas e PDI**: Fluxo mínimo de criação e edição de Metas e PDIs concluído sem erros de requisição no console do navegador.
- [ ] **Feedbacks e Reconhecimentos**: Mural de reconhecimentos carrega e o envio de novo reconhecimento/feedback registra os dados fictícios corretamente.
- [ ] **CORS verificado**: Nenhuma requisição assíncrona falha devido a erros de cabeçalho CORS no console do desenvolvedor no navegador.
- [ ] **Logs seguros**: Logs do container não exibem a string do token JWT ou hashes de senha das requisições interceptadas.
- [ ] **Backup inicial**: Executado dump de segurança inicial pós-provisionamento.

---

## 18. Procedimento básico de rollback

Em caso de falha crítica durante ou após o deploy do ambiente demo, execute o seguinte procedimento estruturado de rollback:
1. Pare e limpa os containers ativos mantendo os volumes persistentes:
   ```bash
   docker compose down
   ```
2. Se a falha for relacionada a modificações de código recentes, volte o repositório para o commit ou tag estável anterior no Git:
   ```bash
   git checkout <hash-estavel-anterior>
   ```
3. Caso o banco de dados tenha sido corrompido, execute a recriação do banco limpo e aplique a restauração do último dump estável:
   ```bash
   docker compose up -d db
   # Aguardar db ficar healthy
   pg_restore -h localhost -U <usuario-db> -d gth_agents -v --clean /tmp/backup_gth_demo_estavel.dump
   ```
4. Suba novamente os serviços do backend e frontend com a base restaurada:
   ```bash
   docker compose up -d api web
   ```
5. Repita o **Checklist pós-deploy** (Seção 17) para assegurar o retorno ao estado saudável.

---

## 19. Riscos e limitações

Ao manter o ambiente demo, os operadores devem estar cientes dos seguintes riscos:
- **Risco de Vazamento de Segredos**: Segredos versionados acidentalmente no Git se os arquivos `.env` não forem adicionados ao `.gitignore` local.
- **Risco de Perda de Dados**: Limpeza indevida do banco caso o script `seed_db.py` seja executado acidentalmente (mitigado pelo aviso de bloqueio na Seção 8).
- **Risco de CORS Incorreto**: O frontend não conseguir se comunicar com a API devido a erros de digitação na variável `CORS_ORIGINS`.
- **Limitação de Performance**: A configuração padrão Docker do banco e da API não é otimizada para concorrência pesada de acessos ou grandes volumes de dados de stress test.

---

## 20. Itens explicitamente fora do escopo

As seguintes tarefas **permanecem fora do escopo** da Issue #081 e não devem ser executadas pelo operador:
- Provisionamento automatizado de servidores em nuvem (AWS, GCP, Azure, Heroku, etc.).
- Registro ou compra de domínios públicos reais ou DNS externos.
- Geração ou instalação de certificados SSL/TLS públicos emitidos por CA oficial em domínios reais (com exceção de simulações com Certbot local/Self-signed).
- Criação e configuração de pipelines automatizadas de CI/CD (GitHub Actions, GitLab CI, Jenkins) para build e deploy automático.
- Alteração ou reescrita dos scripts de seed (`seed_db.py`) ou arquivos de infraestrutura da aplicação.