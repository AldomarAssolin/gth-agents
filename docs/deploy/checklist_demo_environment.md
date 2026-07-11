
hoje 16:38
ISSUE #81:
## Objetivo

Criar um checklist técnico para preparar um ambiente de demonstração controlado do GTH Agents.

## Contexto

O projeto está se aproximando de uma fase de demonstração para outras pessoas. Antes disso, é necessário separar claramente ambiente local, demo/homologação e produção real.

## Escopo

Documentar os requisitos mínimos para ambiente demo:

- variáveis de ambiente;
- configuração de banco;
- migrations;
- seed de demonstração;
- CORS;
- health check;
- URL pública ou domínio;
- dados fictícios;
- backup básico;
- logs mínimos;
- checklist de validação pós-deploy.

## Critérios de aceite

- Checklist criado em docs/deploy/ ou local equivalente.
- Documento diferencia ambiente local, demo e produção.
- Documento lista pré-requisitos mínimos para demonstração controlada.
- Documento indica comandos principais de validação.
- Documento usa apenas exemplos genéricos de configuração.

## Fora do escopo

- Realizar deploy efetivo.
- Contratar serviço cloud.
- Configurar domínio real.
- Implementar pipeline CI/CD.

## Classificação

- Fase: Deploy Demo
- Prioridade: P1
- Tipo: deploy/docs
- Módulo: Deploy
- Risco: Alto
- Versão alvo: v1.0-demo


Manex, a Issue #081 está bem definida e no momento correto do projeto. Depois de fechar segurança, autoria e cobertura dos recursos protegidos, preparar o ambiente de demonstração é a próxima etapa lógica. Finalmente o sistema começa a sair do confortável habitat natural do localhost, onde tudo funciona porque conhece a família inteira.

Veredito
Objetivo: APROVADO
Escopo: APROVADO
Critérios de aceite: APROVADOS
Separação entre ambientes: APROVADA
Risco Alto: JUSTIFICADO
Pronta para planejamento: SIM
Pronta para implementação direta: NÃO, primeiro deve auditar o repositório
O projeto já possui Docker, PostgreSQL, Alembic, variáveis de ambiente, autenticação JWT e health check, portanto a issue não parte do zero. Ela precisa transformar esses elementos dispersos em um procedimento reproduzível e seguro.


O que esta issue deve entregar
Eu criaria o documento:

docs/deploy/checklist_demo_environment.md
Também pode ser:

docs/deploy/demo_environment_checklist.md
Prefiro o primeiro porque mantém o nome diretamente relacionado ao critério de aceite.

A issue deve produzir documentação operacional, não apenas uma coleção de recomendações genéricas.

O leitor precisa conseguir responder:

1. O que diferencia local, demo e produção?
2. Quais configurações precisam existir?
3. Como preparar o banco?
4. Como carregar dados fictícios?
5. Como validar o ambiente depois do deploy?
6. O que fazer se algo falhar?
Estrutura recomendada do documento
1. Objetivo e limites
Explicar que o ambiente demo serve para:

apresentação controlada;

homologação funcional;

testes com usuários convidados;

demonstração do MVP;

uso exclusivo de dados fictícios.

Também deixar explícito:

Não é ambiente de produção.
Não deve conter dados reais de colaboradores.
Não possui garantias completas de alta disponibilidade.
Não substitui política formal de backup e segurança.
2. Matriz dos ambientes
Uma tabela como:

Característica	Local	Demo/Homologação	Produção
Finalidade	Desenvolvimento	Demonstração controlada	Operação real
Dados	Fictícios ou desenvolvimento	Somente fictícios	Dados reais autorizados
Debug	Permitido	Desativado	Desativado
Logs	Verbosos	Operacionais	Estruturados e monitorados
Banco	Local/container	Banco isolado	Banco gerenciado ou dedicado
Backup	Opcional	Básico obrigatório	Política formal
HTTPS	Opcional	Recomendado/obrigatório se público	Obrigatório
Segredos	.env local	Variáveis protegidas	Cofre de segredos
Acesso	Desenvolvedor	Usuários convidados	Usuários reais
Essa tabela é central. Sem ela, “demo” vira apenas produção com menos coragem.

3. Pré-requisitos mínimos
Listar:

Docker e Docker Compose
imagem ou build do backend
imagem ou build do frontend
PostgreSQL compatível
variáveis de ambiente configuradas
porta ou URL pública definida
acesso ao terminal do ambiente
mecanismo de backup/exportação do banco
Não deve escolher provedor cloud nesta issue.

4. Variáveis de ambiente
Separar por componente.

Backend
Exemplos genéricos:

FLASK_ENV=production
SECRET_KEY=<valor-seguro>
JWT_SECRET_KEY=<valor-seguro>
DATABASE_URL=postgresql+psycopg://<usuario>:<senha>@<host>:5432/<banco>
CORS_ORIGINS=https://demo.exemplo.com
Frontend
VITE_API_URL=https://api-demo.exemplo.com
Banco
POSTGRES_DB=<banco_demo>
POSTGRES_USER=<usuario_demo>
POSTGRES_PASSWORD=<senha-segura>
O documento deve dizer:

Nunca reutilizar os valores padrão de desenvolvimento.
Nunca versionar o arquivo .env.
Nunca colocar segredo real nos exemplos.
5. Banco e migrations
O checklist deve incluir algo equivalente a:

docker compose config
docker compose up -d db
docker compose run --rm api alembic upgrade head
docker compose exec api alembic current
docker compose exec api alembic heads
Mas o agente precisa primeiro confirmar os comandos reais usados no monorepo. Não vamos documentar uma CLI imaginária e depois culpar o terminal, que já sofre bastante.

Também deve verificar:

banco isolado do ambiente local;
migration head aplicada;
nenhuma migration pendente;
schema compatível com a aplicação;
usuário do banco com privilégios mínimos necessários.
6. Seed de demonstração
O documento deve determinar que o seed:

contenha somente dados fictícios;

seja idempotente, quando possível;

não dependa de IDs fixos;

crie usuários para os perfis necessários;

gere dados suficientes para os módulos principais;

possa ser removido ou recriado.

Sugestão de perfis fictícios:

ADMIN
RH
LIDER
COLABORADOR
Sugestão de conteúdo:

setores;
funções;
competências;
colaboradores;
avaliações;
metas;
PDIs e ações;
feedbacks;
reconhecimentos;
dados para dashboard e evolução.
O checklist não precisa implementar o seed se ele ainda não existir. Nesse caso, deve registrar a ausência como bloqueio ou pré-requisito para o deploy demo.

7. CORS e URLs
Verificar:

frontend acessa somente a URL correta da API;
backend permite apenas origens explicitamente configuradas;
não usar CORS_ORIGINS=*;
URL não aponta para localhost;
rotas protegidas continuam exigindo JWT.
8. Health check
Comandos esperados:

curl -i https://api-demo.exemplo.com/health
curl -I https://demo.exemplo.com
Resposta mínima da API:

{
  "status": "ok"
}
Mas o documento também deve registrar que o health check atual provavelmente comprova apenas que a aplicação responde. Ele não necessariamente garante:

banco acessível;

migrations aplicadas;

seed carregado;

serviços dependentes funcionando.

Seria útil diferenciar:

Liveness: aplicação está respondendo.
Readiness: aplicação está pronta para atender.
Não precisa implementar um readiness check nesta issue, mas pode registrá-lo como melhoria futura.

9. Logs mínimos
Definir:

data e hora;
nível do log;
método e rota;
status HTTP;
erro ou exceção;
identificador de correlação, se existir;
sem senha, token JWT ou payload sensível.
Também deve constar:

FLASK_DEBUG=False
não exibir stack trace ao usuário
não registrar Authorization header
não registrar senhas
não registrar tokens
10. Backup básico
Para demo, algo simples basta:

pg_dump \
  --host=<host> \
  --username=<usuario> \
  --dbname=<banco> \
  --format=custom \
  --file=backup_demo.dump
E restauração:

pg_restore \
  --host=<host> \
  --username=<usuario> \
  --dbname=<banco> \
  --clean \
  --if-exists \
  backup_demo.dump
O documento deve evitar credenciais reais e dizer que backup não está validado até que a restauração seja testada. Copiar arquivo não é estratégia de recuperação, é só esperança compactada.

11. Checklist pós-deploy
Eu dividiria em blocos.

Infraestrutura
[ ] Containers ou serviços estão ativos
[ ] Banco responde
[ ] API responde ao health check
[ ] Frontend responde
[ ] URL pública utiliza HTTPS, quando exposta externamente
Banco
[ ] Migration head aplicada
[ ] Seed demo executado
[ ] Dados fictícios presentes
[ ] Nenhum dado real presente
[ ] Backup inicial criado
Integração
[ ] Frontend chama a API correta
[ ] CORS aceita somente a origem demo
[ ] Login funciona
[ ] Token JWT é enviado
[ ] 401 e 403 continuam funcionando
Validação funcional mínima
[ ] Login ADMIN
[ ] Login RH
[ ] Login LIDER
[ ] Login COLABORADOR
[ ] Dashboard carrega
[ ] Colaboradores são listados conforme escopo
[ ] Evolução individual carrega
[ ] Avaliação pode ser criada
[ ] Meta pode ser criada
[ ] PDI pode ser consultado
[ ] Feedback pode ser registrado
[ ] Reconhecimento pode ser consultado
Segurança
[ ] Debug desativado
[ ] Segredos não estão no repositório
[ ] Senhas padrão foram alteradas
[ ] CORS não usa wildcard
[ ] Banco não está publicamente exposto sem necessidade
[ ] Dados são totalmente fictícios
[ ] Perfil adulterado no frontend não concede autorização
Cuidados importantes
Não misturar demo e produção
Evite descrever demo como “produção inicial”. São ambientes com riscos e responsabilidades diferentes.

Não documentar comandos antes da inspeção
O Antigravity deve conferir:

docker-compose.yml
backend/.env.example
frontend/.env.example
backend/README.md
README.md
migrations/
seed_db.py ou equivalente
endpoint /health
configuração atual de CORS
Dockerfiles
A documentação precisa refletir o repositório real.

Não transformar a issue em deploy
O escopo termina no checklist e na comprovação documental:

não criar conta cloud;
não subir aplicação;
não registrar domínio;
não configurar CI/CD;
não gerar certificado real;
não criar credenciais reais.
Instrução recomendada para o Antigravity

Planejar e implementar a ISSUE #081 — Checklist de ambiente demo
Analise e implemente a ISSUE #081 no monorepo GTH Agents.

Objetivo
Criar um checklist técnico, reproduzível e seguro para preparação de um ambiente de demonstração controlado do GTH Agents.

O documento deve diferenciar claramente:

ambiente local;

ambiente demo ou homologação;

ambiente de produção.

Não realizar deploy efetivo.

Não contratar serviço cloud.

Não configurar domínio real.

Não implementar pipeline CI/CD.

Não executar commit, push, merge ou criação de tag.

Etapa 1 — Inspeção obrigatória
Antes de escrever o documento, inspecione:

docker-compose.yml
backend/Dockerfile
frontend/Dockerfile*
README.md
backend/README.md
frontend/README.md
backend/.env.example
frontend/.env.example
backend/app.py
backend/migrations/
backend/seed_db.py
backend/tests/
Localize e confirme:

variáveis de ambiente utilizadas;
configuração real do banco;
comandos reais do Alembic;
seed existente;
configuração atual de CORS;
endpoint de health check;
portas usadas;
build de backend e frontend;
volumes do PostgreSQL;
comandos de testes;
nomes reais dos serviços Docker Compose.
Não presumir comandos ou nomes.

Caso algum item não exista, registrar a ausência como pré-requisito ou risco, sem inventar implementação.

Etapa 2 — Plano de implementação
Antes de criar o checklist, gerar:

docs/deploy/implementation_plan_issue_081_demo_environment_checklist.md
O plano deve conter:

estado atual do repositório;

artefatos encontrados;

lacunas encontradas;

estrutura proposta para o checklist;

comandos reais que serão documentados;

riscos;

arquivos que serão criados ou alterados.

Não iniciar a documentação definitiva antes de concluir o plano.

Etapa 3 — Documento principal
Criar:

docs/deploy/checklist_demo_environment.md
O documento deve incluir:

objetivo;

limites do ambiente demo;

matriz comparativa entre local, demo e produção;

pré-requisitos;

variáveis de ambiente;

banco de dados;

migrations;

seed de demonstração;

CORS;

health check;

URL pública ou domínio;

dados fictícios;

logs mínimos;

backup e restauração;

comandos de validação;

checklist pré-deploy;

checklist pós-deploy;

procedimento básico de rollback;

riscos e limitações;

itens explicitamente fora do escopo.

Regras de segurança
Usar somente exemplos genéricos:

SECRET_KEY=<valor-seguro>
JWT_SECRET_KEY=<valor-seguro>
DATABASE_URL=<url-do-banco>
CORS_ORIGINS=https://demo.exemplo.com
VITE_API_URL=https://api-demo.exemplo.com
Não incluir:

senhas reais;

tokens;

domínios reais;

endereços IP reais;

caminhos absolutos locais;

dados pessoais;

credenciais de serviços;

conteúdo de arquivos .env.

O checklist deve exigir:

debug desativado;
segredos fora do Git;
CORS restritivo;
dados exclusivamente fictícios;
senhas padrão alteradas;
banco isolado;
backup básico;
validação de restauração;
logs sem dados sensíveis;
JWT e autorização validados após deploy.
Seed de demonstração
Inspecionar o seed existente.

Documentar:

comando real de execução;

dados criados;

dependências;

comportamento em reexecução;

riscos de duplicidade;

forma de limpeza ou recriação.

Caso o seed atual não seja adequado para demo, não alterá-lo nesta issue. Registrar:

BLOQUEIO: seed de demonstração controlado ainda não disponível.
E recomendar issue futura específica.

Comandos de validação
Usar os comandos reais encontrados no projeto.

Cobrir, quando aplicável:

docker compose config
docker compose build
docker compose up -d
docker compose ps
docker compose logs
alembic upgrade head
alembic current
pytest
npm run lint
npm run build
curl /health
Não documentar comandos que não funcionem com a estrutura atual.

Checklist pós-deploy
Incluir verificações de:

serviços ativos;

banco acessível;

migrations aplicadas;

seed carregado;

API saudável;

frontend acessível;

CORS correto;

login;

JWT;

401;

403;

escopo de LIDER;

escopo de COLABORADOR;

dashboard;

fluxo mínimo de avaliação;

metas;

PDI;

feedback;

reconhecimento;

backup inicial;

ausência de dados reais;

ausência de segredos nos logs.

Validação técnica
Executar apenas validações que não configurem deploy real:

docker compose config;
inspeção dos arquivos;
validação dos comandos existentes;
busca por caminhos absolutos;
busca por segredos ou exemplos inadequados;
verificação dos links relativos;
git diff --check.
Não subir infraestrutura externa.

Walkthrough
Criar:

docs/deploy/walkthrough_issue_081_demo_environment_checklist.md
Registrar:

arquivos criados;

fontes inspecionadas;

estrutura final;

comandos validados;

lacunas identificadas;

riscos;

itens não executados por estarem fora do escopo.

O walkthrough não deve declarar que o ambiente demo foi implantado.

A conclusão correta deve ser semelhante a:

Checklist técnico concluído e pronto para orientar uma futura implantação controlada. Nenhum deploy efetivo foi realizado nesta issue.
A issue fica como porta de entrada da versão v1.0-demo. Depois dela, as próximas issues naturais seriam o seed controlado, configuração Docker de demo e o deploy efetivo, cada uma separada. Misturar tudo agora seria a maneira mais rápida de transformar “demonstração controlada” em “produção improvisada com esperança”.


O plano:
# Plano de Implementação — Checklist de Ambiente Demo (Issue #081)

Este plano define a estrutura, os pré-requisitos, as informações de segurança e os procedimentos de validação para a criação do checklist de preparação do ambiente de demonstração controlado da plataforma GTH Agents.

## User Review Required

> [!IMPORTANT]
> **Identificação do Status do Seed de Banco de Dados**
> Durante a inspeção do arquivo backend/seed_db.py, observamos que ele limpa o banco de dados completamente (usando .delete() em cascata na ordem de dependências) e carrega dados de teste estáticos com senhas padrão fracas como admin123.
> **BLOQUEIO: seed de demonstração controlado ainda não disponível.**
> Recomendamos a criação de uma issue futura para construir um script de seed parametrizável exclusivo para demonstração (ex: backend/seed_demo.py), que evite a remoção destrutiva de dados se rodado em produção acidentalmente, e utilize segredos seguros ou senhas temporárias geradas dinamicamente.

> [!WARNING]
> **Segurança de Credenciais no Guia**
> Conforme as regras de segurança especificadas na issue, todas as variáveis de ambiente e segredos no checklist usarão apenas placeholders genéricos (ex: SECRET_KEY=<valor-seguro>). Nenhuma credencial real ou do arquivo .env de desenvolvimento local será exposta.

## Open Questions

> [!NOTE]
> 1. Há interesse em detalhar ferramentas de backup externas específicas (como pg_dump com upload automático para S3/Storage) na issue futura, ou apenas documentar a execução local do pg_dump e pg_restore no checklist do ambiente demo?
> 2. O CORS padrão da demonstração utilizará um subdomínio específico (ex: *.exemplo.com) ou apenas variáveis de ambiente para serem configuradas dinamicamente pelo operador?

## Proposed Changes

### Documentation (docs/deploy/)

Criação da documentação de deploy e checklist de ambiente na pasta dedicada docs/deploy/.

---

#### [NEW] [implementation_plan_issue_081_demo_environment_checklist.md](docs/deploy/implementation_plan_issue_081_demo_environment_checklist.md)
* Este arquivo de planejamento detalhando as decisões de design do checklist.

#### [NEW] [checklist_demo_environment.md](docs/deploy/checklist_demo_environment.md)
* O documento principal contendo as instruções reproduzíveis divididas em 20 seções, conforme o escopo da issue.

#### [NEW] [walkthrough_issue_081_demo_environment_checklist.md](docs/deploy/walkthrough_issue_081_demo_environment_checklist.md)
* O walkthrough registrando os arquivos criados, as fontes inspecionadas e os comandos reais validados durante o processo.

## Estado Atual do Repositório (Inspeção)

* **Variáveis de Ambiente**:
  * Backend usa: FLASK_APP, FLASK_ENV, SECRET_KEY, DATABASE_URL, JWT_SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRES_MINUTES, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, CORS_ORIGINS.
  * Frontend usa: VITE_API_URL.
* **Banco de dados**: PostgreSQL 16 (imagem Docker postgres:16-alpine), base gth_agents, com volume nomeado postgres_data.
* **Migrations**: Executadas via Alembic com alembic upgrade head.
* **Seed**: backend/seed_db.py disponível, mas destrutivo (faz delete() de todas as tabelas).
* **CORS**: Configurado dinamicamente em backend/app.py a partir do CORS_ORIGINS (default: http://localhost:5173).
* **Health Check**: GET /health retorna {"status": "ok"}.
* **Portas**: API em 5000, Frontend dev em 5173 (produção em 80), PostgreSQL interno na porta 5432.
* **Builds**: backend/Dockerfile (Flask run) e frontend/Dockerfile.prod (Nginx + React build estático).
* **Testes**: pytest com 208 testes no backend. npm run lint e npm run build no frontend.

## Verification Plan

### Automated Tests
- Execução de busca no repositório por caminhos absolutos locais vazados na documentação recém-criada:

bash
  grep -R "/home/" docs/deploy/ --include="*.md"

- Execução de busca no repositório por segredos inadequados:

bash
  grep -R "admin123" docs/deploy/ --include="*.md"


### Manual Verification
- Revisão visual e de conteúdo dos links do Markdown para garantir que apontam para arquivos corretos via links relativos válidos.
- Validação estrutural de todos os comandos do Docker Compose e Alembic descritos no checklist.
- Confirmação de que todas as 20 seções solicitadas estão estruturadas e detalhadas no documento final.

Manex, o plano está bom, coerente com a Issue #081 e pronto para execução após alguns ajustes pequenos. Ele cumpriu o principal: inspecionou o repositório real, encontrou o risco do seed destrutivo e não tentou disfarçá-lo com um parágrafo otimista, tradição bastante popular em documentação de deploy.

Veredito
Inspeção do repositório: APROVADA
Variáveis de ambiente: APROVADAS
Banco e migrations: APROVADOS
Seed de demonstração: BLOQUEIO CORRETAMENTE IDENTIFICADO
CORS: APROVADO
Health check: APROVADO COM RESSALVA
Estrutura documental: APROVADA
Plano de verificação: APROVADO COM AJUSTES
Pode implementar: SIM
1. Resolver as Open Questions dentro do próprio plano
As duas perguntas não precisam bloquear a execução. Como a issue é exclusivamente documental e não envolve contratação ou configuração de infraestrutura externa, a decisão mais segura é:

Backup
Documentar apenas:

pg_dump
pg_restore
armazenamento local ou diretório protegido definido pelo operador
teste de restauração
Upload automático para S3, Storage ou serviço equivalente deve ficar para uma issue futura.

Acrescente ao plano:

### Decisão sobre backup

Nesta issue serão documentados apenas os procedimentos genéricos de backup e restauração com `pg_dump` e `pg_restore`.

Integração com armazenamento externo, automação de retenção, criptografia remota e agendamento de backups permanecem fora do escopo e deverão ser tratados em issue futura.
CORS
Não utilizar wildcard de subdomínio como regra padrão.

O checklist deve trabalhar com valores explícitos configurados dinamicamente:

CORS_ORIGINS=https://demo.exemplo.com
Ou, caso frontend e API tenham origens distintas:

CORS_ORIGINS=https://app-demo.exemplo.com
O backend deve aceitar apenas as origens enumeradas. Nada de *.exemplo.com por conveniência, porque segurança adora morrer em nome da conveniência.

Use:

### Decisão sobre CORS

O checklist utilizará variáveis de ambiente com origens completas e explicitamente permitidas.

Não será recomendado wildcard global ou wildcard de subdomínio. O operador deverá informar cada origem autorizada conforme a topologia real do ambiente.
Com essas decisões, a seção Open Questions pode virar Decisões adotadas.

2. Refinar a descrição do seed destrutivo
O plano diz:

limpa o banco de dados completamente usando .delete() em cascata

Se o script realiza vários .delete() manualmente na ordem das dependências, “em cascata” pode sugerir que o banco usa ON DELETE CASCADE.

Melhor escrever:

O script remove os registros das tabelas por meio de operações `.delete()` executadas em ordem compatível com as dependências e, em seguida, carrega dados estáticos de desenvolvimento.
O bloqueio está correto:

BLOQUEIO: seed de demonstração controlado ainda não disponível.
Também recomendo registrar explicitamente:

O backend/seed_db.py não deve ser executado em ambiente demo existente
sem confirmação de que o banco pode ser completamente recriado.
3. Não transformar a senha admin123 em segredo proibido de mencionar
A busca:

grep -R "admin123" docs/deploy/ --include="*.md"
é útil, mas há uma sutileza. O walkthrough pode precisar registrar que o seed atual contém uma senha fraca, sem reproduzir o valor.

Portanto, o esperado da busca deve ser nenhuma ocorrência do valor literal, não ausência de alertas sobre senhas fracas.

No documento, use:

O seed atual utiliza credenciais estáticas e inadequadas para demonstração.
Sem informar a senha.

Além disso, amplie a busca:

grep -R -n -E \
"admin123|postgres:postgres|dev-secret-change-me|localhost:[0-9]+.*senha" \
docs/deploy/ --include="*.md"
Com cuidado para não proibir exemplos técnicos legítimos. O objetivo é localizar valores indevidos para revisão humana, não declarar que todo resultado do grep é automaticamente uma vulnerabilidade.

4. O health check precisa ser descrito como liveness
O endpoint atual:

GET /health
retorna:

{"status": "ok"}
Isso comprova que o processo Flask está respondendo. Não comprova necessariamente:

conexão com PostgreSQL;

migrations aplicadas;

seed disponível;

prontidão completa da aplicação.

Inclua:

O endpoint `/health` atual funciona como verificação básica de disponibilidade da API.

Ele não deve ser interpretado isoladamente como comprovação de que o banco está acessível, que as migrations foram aplicadas ou que o ambiente está funcionalmente pronto.
No checklist pós-deploy, combine:

GET /health
alembic current
consulta funcional autenticada
validação do frontend
Isso forma uma verificação de prontidão operacional mais confiável.

5. Ajustar a afirmação sobre a porta de produção
O plano diz:

Frontend dev em 5173, produção em 80

Mais precisamente, o Nginx provavelmente escuta na porta 80 dentro do container. A porta pública depende do mapeamento definido no Compose, no serviço cloud ou no proxy reverso.

Troque por:

- Frontend de desenvolvimento: Vite na porta interna/publicada `5173`.
- Frontend de produção: Nginx escutando na porta interna `80`; a porta ou URL pública depende da infraestrutura de implantação.
Esse detalhe evita alguém concluir que todo ambiente demo obrigatoriamente precisa publicar :80.

6. Fortalecer o Verification Plan
As duas buscas são boas, mas insuficientes para validar toda a documentação.

Acrescente:

docker compose config
git diff --check
Para confirmar os arquivos criados:

find docs/deploy -maxdepth 1 -type f | sort
Para procurar caminhos locais comuns:

grep -R -n -E \
"/home/|/Users/|C:\\\\Users\\\\" \
docs/deploy/ --include="*.md"
Para verificar placeholders e possíveis valores sensíveis:

grep -R -n -E \
"admin123|dev-secret-change-me|postgres:postgres|Bearer [A-Za-z0-9._-]+" \
docs/deploy/ --include="*.md"
Para confirmar as seções obrigatórias, pode ser feita uma revisão estruturada dos títulos:

grep -n "^## " docs/deploy/checklist_demo_environment.md
Não precisa transformar isso em um teste automatizado mirabolante. Uma checklist continua sendo documentação, não um compilador de políticas públicas.

7. Separar comandos validados de comandos apenas exemplificados
O walkthrough deve distinguir:

Validados contra o repositório
docker compose config
alembic upgrade head
alembic current
pytest
npm run lint
npm run build
GET /health
Exemplos genéricos não executados
pg_dump contra ambiente remoto
pg_restore contra ambiente remoto
URL HTTPS pública
proxy reverso
domínio
certificado TLS
Assim o walkthrough não declara que um backup remoto ou deploy público foi validado quando nenhum ambiente externo existe.

8. Incluir o risco do Docker de produção
O checklist deve confirmar se existe uma composição específica para produção/demo ou apenas:

frontend/Dockerfile.prod
docker-compose.yml de desenvolvimento
Ter um Dockerfile.prod não significa automaticamente que existe uma configuração completa de demo.

O plano deve registrar uma destas situações:

Existe configuração Compose compatível com o build de produção.
ou:

LACUNA: existe Dockerfile de produção para o frontend, mas ainda não há
arquivo Compose específico para ambiente demo.
Isso pode virar outra issue futura, sem ampliar a #081.

Versão recomendada das decisões
Substitua Open Questions por:

## Decisões adotadas

### Backup

O checklist documentará os comandos genéricos de `pg_dump` e `pg_restore`, incluindo a necessidade de testar a restauração.

Automação de upload, retenção, criptografia externa e integração com serviços de armazenamento ficam fora do escopo desta issue.

### CORS

O checklist utilizará origens completas configuradas por variável de ambiente.

Não serão recomendados `*` nem wildcard de subdomínio. Cada origem autorizada deverá ser declarada explicitamente pelo operador.
Conclusão
O plano já pode ser aprovado com estes refinamentos:

✓ manter o bloqueio do seed demo;
✓ documentar apenas pg_dump/pg_restore;
✓ usar CORS com origens explícitas;
✓ tratar /health como liveness básica;
✓ diferenciar porta interna do container e exposição pública;
✓ ampliar as verificações documentais;
✓ separar comandos realmente validados de exemplos genéricos;
✓ registrar se falta uma composição Docker específica para demo.
Depois disso, o Antigravity pode criar os três documentos. A conclusão correta continuará sendo:

Checklist técnico concluído e pronto para orientar uma futura implantação controlada. Nenhum deploy efetivo foi realizado.

Crie a instrução completa de correção do plano de implementação para o antigravity.

Manex, use esta instrução inteira no Antigravity. Ela corrige o plano sem autorizar implementação, porque primeiro o plano precisa parar de deixar decisões importantes penduradas como se infraestrutura aceitasse “vemos depois”.

Corrigir o Plano de Implementação da ISSUE #081 — Checklist de Ambiente Demo
Revise e corrija exclusivamente o plano de implementação da ISSUE #081 — Checklist de Ambiente Demo no monorepo GTH Agents.

Arquivo alvo:

docs/deploy/implementation_plan_issue_081_demo_environment_checklist.md
Objetivo desta tarefa
Ajustar o plano de implementação para que ele:

reflita com precisão o estado atual do repositório;

elimine perguntas abertas que já podem ser decididas;

diferencie fatos confirmados, comandos validados e exemplos genéricos;

registre corretamente as limitações do seed atual;

trate o endpoint /health apenas como verificação básica de disponibilidade;

esclareça portas internas de containers e exposição pública;

fortaleça o plano de validação documental;

registre eventuais lacunas de configuração para ambiente demo;

permaneça estritamente dentro do escopo documental da Issue #081.

Não criar ainda o checklist definitivo.

Não criar ainda o walkthrough definitivo.

Não implementar seed novo.

Não alterar Dockerfiles, Docker Compose, backend, frontend, migrations ou arquivos de ambiente.

Não executar deploy.

Não executar commit, push, merge, tag ou alteração de branch.

1. Preservar a inspeção já realizada
Manter no plano as informações confirmadas durante a inspeção do repositório, desde que estejam corretas:

Backend:
- FLASK_APP
- FLASK_ENV
- SECRET_KEY
- DATABASE_URL
- JWT_SECRET_KEY
- JWT_ALGORITHM
- JWT_EXPIRES_MINUTES
- POSTGRES_DB
- POSTGRES_USER
- POSTGRES_PASSWORD
- CORS_ORIGINS

Frontend:
- VITE_API_URL

Banco:
- PostgreSQL 16
- imagem postgres:16-alpine
- banco padrão gth_agents
- volume nomeado postgres_data

Migrations:
- Alembic
- alembic upgrade head

Health check:
- GET /health
- resposta {"status": "ok"}

Portas:
- API em 5000
- frontend Vite em 5173
- PostgreSQL em 5432 dentro da rede Docker

Builds:
- backend/Dockerfile
- frontend/Dockerfile.prod

Validações:
- pytest no backend
- npm run lint no frontend
- npm run build no frontend
Não alterar informações confirmadas sem nova evidência obtida diretamente no repositório.

2. Substituir “Open Questions” por “Decisões adotadas”
Remover a seção:

Open Questions
Substituí-la por:

## Decisões adotadas
Adicionar as seguintes decisões.

2.1 Backup do ambiente demo
Registrar:

### Backup

Nesta issue serão documentados apenas procedimentos genéricos de backup e restauração utilizando `pg_dump` e `pg_restore`.

O checklist deverá exigir que a restauração seja testada, pois a simples criação de um arquivo de backup não comprova sua recuperabilidade.

Permanecem fora do escopo desta issue:

- upload automático para S3, Object Storage ou serviço equivalente;
- agendamento automático;
- política de retenção;
- criptografia externa;
- replicação;
- integração com serviços gerenciados de backup.

Esses itens deverão ser tratados em issue futura, caso sejam necessários.
2.2 CORS do ambiente demo
Registrar:

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

---

# 3. Corrigir a descrição do seed atual

Na seção de revisão obrigatória, substituir descrições que possam sugerir exclusão em cascata automática pelo banco.

Não usar:

```text
delete em cascata
a menos que o banco realmente esteja configurado com ON DELETE CASCADE e isso tenha sido comprovado.

Usar formulação equivalente a:

O arquivo `backend/seed_db.py` remove registros das tabelas por meio de operações `.delete()` executadas em ordem compatível com as dependências entre as entidades e, em seguida, carrega dados estáticos de desenvolvimento.
Manter claramente:

BLOQUEIO: seed de demonstração controlado ainda não disponível.
Acrescentar:

O script atual não deve ser executado em um ambiente demo existente sem confirmação explícita de que o banco pode ser completamente recriado.

O seed atual deve ser tratado como ferramenta de desenvolvimento local, não como procedimento seguro de inicialização de ambiente demo.
Registrar também os riscos:

- exclusão destrutiva de dados existentes;
- credenciais estáticas inadequadas para demonstração;
- dependência de dados fixos;
- risco de duplicidade ou inconsistência em reexecuções;
- ausência de proteção contra execução no ambiente incorreto;
- ausência de parametrização específica para demo.
Não reproduzir no plano a senha literal encontrada no seed.

Usar apenas:

credenciais estáticas e inadequadas para demonstração
4. Registrar uma issue futura para seed de demonstração
Adicionar ao plano uma recomendação de issue futura com escopo semelhante a:

### Issue futura recomendada

Criar um seed exclusivo para demonstração, por exemplo:

```text
backend/seed_demo.py
Esse script deverá:

utilizar somente dados fictícios;

evitar limpeza destrutiva por padrão;

exigir confirmação explícita para recriação total;

ser idempotente ou detectar dados existentes;

não conter senhas fracas versionadas;

aceitar credenciais por variáveis de ambiente;

criar usuários dos perfis necessários à demonstração;

gerar dados suficientes para dashboard, avaliações, metas, PDI, feedbacks e reconhecimentos;

registrar claramente quando não deve ser executado.


Não implementar essa issue nesta tarefa.

---

# 5. Corrigir a interpretação do health check

Na seção de estado atual, manter:

```http
GET /health
e:

{"status": "ok"}
Mas acrescentar explicitamente:

O endpoint `/health` atual funciona como uma verificação básica de disponibilidade do processo da API.

Ele comprova que a aplicação Flask está respondendo, mas não garante isoladamente:

- conectividade com PostgreSQL;
- migrations aplicadas;
- compatibilidade do schema;
- seed carregado;
- funcionamento da autenticação;
- prontidão funcional do frontend;
- disponibilidade completa do ambiente.
Classificar o endpoint como:

liveness básica
Não classificá-lo como readiness completa.

Registrar que a futura validação operacional deverá combinar:

- GET /health;
- docker compose ps;
- verificação das migrations;
- consulta funcional autenticada;
- validação do frontend;
- validação do banco;
- validação do CORS.
Não implementar novo endpoint de readiness nesta issue.

Pode registrar essa implementação como melhoria futura.

6. Corrigir a descrição das portas
Substituir afirmações absolutas como:

frontend de produção na porta 80
por uma descrição tecnicamente precisa:

- Backend: porta interna/publicada `5000` na configuração atual de desenvolvimento.
- Frontend de desenvolvimento: servidor Vite na porta interna/publicada `5173`.
- Frontend de produção: Nginx escutando na porta interna `80` dentro do container.
- A porta pública, URL externa ou domínio dependem da infraestrutura de implantação, proxy reverso ou mapeamento configurado no ambiente demo.
- PostgreSQL utiliza a porta interna `5432` na rede Docker e não deve ser publicamente exposto sem necessidade operacional comprovada.
Não afirmar que a porta pública da demonstração será obrigatoriamente 80.

7. Auditar a configuração Docker disponível
O plano deve confirmar se existe:

- Dockerfile de produção do frontend;
- Dockerfile adequado do backend;
- Docker Compose específico para demo ou produção;
- apenas Docker Compose de desenvolvimento.
Inspecionar novamente, quando necessário:

find . -maxdepth 3 -type f \
  \( -iname "dockerfile*" -o -iname "*compose*.yml" -o -iname "*compose*.yaml" \) \
  | sort
Registrar uma das conclusões:

Caso exista composição específica para demo
Existe uma composição Docker específica compatível com o ambiente demo e com o build de produção do frontend.
Caso não exista
### Lacuna identificada

Existe um `Dockerfile.prod` para o frontend, porém não foi encontrada uma composição Docker específica para ambiente demo.

O `docker-compose.yml` atual deve ser tratado conforme sua finalidade real, provavelmente desenvolvimento local.

A criação de uma composição específica para demo deverá ser tratada em issue futura e não será implementada na Issue #081.
Não presumir que a existência de Dockerfile.prod torna o ambiente demo completo.

8. Diferenciar comandos reais e exemplos genéricos
Adicionar ao plano uma seção:

## Classificação dos comandos documentados
Dividir os comandos em dois grupos.

8.1 Comandos confirmados contra o repositório
Incluir apenas os comandos realmente compatíveis com a estrutura atual, como:

docker compose config
docker compose build
docker compose up
docker compose ps
docker compose logs
alembic upgrade head
alembic current
pytest
npm run lint
npm run build
curl para /health
Antes de colocá-los como validados, confirmar:

diretório correto de execução;

nome real dos serviços;

necessidade de docker compose exec;

uso de ambiente virtual;

uso de PYTHONPATH;

variável FLASK_APP;

comando de inicialização real do backend.

8.2 Exemplos genéricos não executados
Classificar explicitamente como exemplos:

pg_dump de banco remoto
pg_restore de banco remoto
URL HTTPS pública
domínio
proxy reverso
certificado TLS
armazenamento externo
rollback em infraestrutura cloud
Acrescentar:

Esses comandos serão apresentados apenas como modelos genéricos e não serão descritos como executados ou validados contra infraestrutura externa.
9. Reforçar o plano de verificação
Atualizar a seção:

Verification Plan
para conter as verificações abaixo.

9.1 Estrutura dos documentos
find docs/deploy -maxdepth 1 -type f | sort
9.2 Caminhos absolutos locais
grep -R -n -E \
"/home/|/Users/|C:\\\\Users\\\\" \
docs/deploy/ \
--include="*.md"
Resultado esperado:

nenhum caminho local absoluto
9.3 Valores sensíveis ou inadequados
grep -R -n -E \
"admin123|dev-secret-change-me|postgres:postgres|Bearer [A-Za-z0-9._-]+" \
docs/deploy/ \
--include="*.md"
A ocorrência de qualquer padrão deve ser revisada.

Não tratar todo resultado automaticamente como vulnerabilidade, pois um documento pode mencionar um padrão apenas para alertar que ele é proibido.

O plano deve exigir revisão contextual.

9.4 Validação do Docker Compose
docker compose config
Registrar o resultado real.

9.5 Validação do diff
git diff --check
Resultado esperado:

nenhuma saída
9.6 Estrutura das seções obrigatórias
grep -n "^## " docs/deploy/checklist_demo_environment.md
A revisão deve confirmar a presença das 20 seções solicitadas pela issue.

9.7 Links relativos
Executar revisão dos links relativos Markdown.

Não declarar que todos os links foram testados caso tenha sido feita apenas inspeção visual.

Usar formulação precisa, como:

Os links relativos foram revisados por inspeção estrutural.
Caso cada link seja realmente aberto ou validado por ferramenta, registrar o método utilizado.

10. Corrigir a seção de validação manual
A seção atual chamada:

Manual Verification
deve ser renomeada para:

## Revisão documental
Ela deve conter:

- revisão dos títulos e da sequência das 20 seções;
- confirmação de que os exemplos utilizam placeholders;
- confirmação de que não existem credenciais reais;
- confirmação de que comandos executados estão separados de exemplos genéricos;
- revisão dos links relativos;
- confirmação de que o documento diferencia local, demo e produção;
- confirmação de que o seed atual está marcado como bloqueio;
- confirmação de que nenhum deploy foi declarado como realizado.
Não usar esta etapa para simular deploy, login em ambiente externo ou validação de domínio real.

11. Registrar os limites do ambiente demo
Adicionar ao plano que o checklist definitivo deverá declarar:

- ambiente demo não é produção;
- dados reais são proibidos;
- debug deve estar desativado;
- segredos devem permanecer fora do Git;
- credenciais padrão devem ser substituídas;
- o banco deve ser isolado;
- CORS deve usar origens explícitas;
- o PostgreSQL não deve ser publicamente exposto sem necessidade;
- logs não devem registrar senhas, tokens ou Authorization;
- backup deve ter restauração testada;
- o acesso deve ser restrito aos participantes da demonstração;
- o ambiente pode possuir disponibilidade limitada;
- não há garantia formal de alta disponibilidade;
- não há política completa de disaster recovery nesta issue.
12. Preservar a estrutura dos arquivos propostos
Manter como entregas futuras da implementação:

docs/deploy/implementation_plan_issue_081_demo_environment_checklist.md

docs/deploy/checklist_demo_environment.md

docs/deploy/walkthrough_issue_081_demo_environment_checklist.md
Nesta tarefa, alterar somente o plano já existente.

Não criar ainda os outros dois documentos.

13. Atualizar o estado atual do repositório
Na seção de inspeção, organizar o conteúdo em uma tabela ou blocos claros:

Item
Arquivo ou origem
Estado encontrado
Implicação para demo
Exemplo:

Item	Estado encontrado	Implicação
Variáveis backend	Definidas em .env.example e Compose	Precisam receber valores seguros no demo
CORS	Configurável por CORS_ORIGINS	Deve usar origens explícitas
Health check	/health básico	Não comprova readiness completa
Seed	Destrutivo e estático	Bloqueio para ambiente demo
Frontend prod	Dockerfile.prod encontrado	Confirmar composição demo
Banco	PostgreSQL com volume	Exigir isolamento e backup
Migrations	Alembic disponível	Aplicar e validar head
Logs	Confirmar comportamento atual	Definir requisitos mínimos no checklist
Não inventar informação para preencher a tabela.

Quando algo não for encontrado, registrar:

NÃO CONFIRMADO
ou:

LACUNA IDENTIFICADA
14. Atualizar os riscos do plano
Adicionar ou revisar a seção de riscos com:

- execução acidental do seed destrutivo;
- uso de credenciais estáticas;
- reutilização de segredos de desenvolvimento;
- CORS permissivo;
- debug habilitado;
- banco publicamente exposto;
- ausência de composição específica para demo;
- confusão entre porta interna e porta pública;
- considerar `/health` como readiness completa;
- ausência de teste de restauração;
- presença acidental de dados reais;
- logs contendo dados sensíveis;
- frontend apontando para API incorreta;
- migrations pendentes;
- uso de comandos genéricos não compatíveis com o repositório.
Para cada risco, indicar no plano como o checklist o mitigará ou registrará.

15. Resultado esperado da correção
Ao terminar a revisão, o plano deve:

- não conter perguntas abertas sem decisão;
- manter o bloqueio do seed demo;
- não reproduzir a senha fraca literal;
- documentar backup apenas com pg_dump e pg_restore;
- adotar CORS com origens explícitas;
- classificar /health como liveness básica;
- diferenciar porta interna e exposição pública;
- informar se existe ou não composição específica para demo;
- diferenciar comandos validados e exemplos genéricos;
- possuir um plano de verificação mais completo;
- não afirmar que qualquer deploy foi realizado;
- permanecer limitado à documentação da Issue #081.
16. Relatório final desta tarefa
Após corrigir o plano, apresentar um resumo contendo:

- arquivo alterado;
- seções modificadas;
- decisões adotadas;
- lacunas registradas;
- verificações realizadas;
- resultado de git diff --check;
- confirmação de que nenhum outro arquivo foi alterado;
- confirmação de que nenhum deploy foi executado;
- confirmação de que commit e push não foram executados.
A conclusão deve ser semelhante a:

Plano de implementação da Issue #081 corrigido e pronto para nova revisão. Nenhum checklist definitivo, walkthrough ou deploy foi criado nesta etapa.
Depois da execução, revise o plano corrigido antes de autorizar os outros dois documentos. Até documentação merece controle de qualidade, embora humanos frequentemente a tratem como o texto que se escreve cinco minutos antes do merge.



Markdown(1).md colado
Arquivo
O plano de implementação está pronto?

Manex, sim, o plano de implementação está pronto para execução. Ele incorporou corretamente as correções solicitadas e agora apresenta decisões fechadas, riscos, limitações e critérios verificáveis, em vez de deixar a infraestrutura depender de interpretação criativa do próximo ser humano.


Veredito
Inspeção do repositório: APROVADA
Decisões sobre backup e CORS: APROVADAS
Bloqueio do seed atual: CORRETAMENTE REGISTRADO
Separação local/demo/produção: APROVADA
Docker e portas: APROVADOS
Health check como liveness: APROVADO
Riscos e mitigações: APROVADOS
Plano de verificação: APROVADO
Escopo documental: PRESERVADO
Pronto para implementar checklist e walkthrough: SIM
O plano agora:

substitui perguntas abertas por decisões;

limita o backup a pg_dump e pg_restore;

exige CORS com origens explícitas;

identifica corretamente o seed atual como destrutivo e inadequado para demo;

distingue porta interna do container de exposição pública;

classifica /health como liveness básica;

registra a ausência de um Compose específico para demo;

separa comandos confirmados de exemplos genéricos;

prevê auditoria de caminhos, segredos, estrutura e formatação;

deixa claro que nenhum deploy será realizado.


Dois ajustes pequenos durante a implementação
Eles não bloqueiam o plano, mas devem ser observados na geração do checklist.

1. Não recomendar atualização manual de hashes no banco
Na mitigação de credenciais fracas aparece:

“fornecerá comandos genéricos para atualização de hashes de senha.”

Eu evitaria comandos SQL ou scripts improvisados para alterar senha_hash. O checklist deve recomendar:

- criar usuários por fluxo suportado pela aplicação;
- utilizar um futuro seed_demo parametrizado;
- alterar senhas pela camada de aplicação;
- nunca gravar senha ou hash manualmente no banco sem procedimento oficial.
Isso mantém as regras de hashing centralizadas no sistema. Atualizar hash diretamente no banco é o tipo de atalho que funciona até alguém trocar o algoritmo e todos descobrirem durante a apresentação.

2. Não chamar comandos de “validados” sem execução comprovada
A seção de comandos confirmados afirma que foram validados localmente. No walkthrough final, o Antigravity deve registrar exatamente quais comandos executou e seus resultados.

Por exemplo:

docker compose config        → executado e aprovado
git diff --check             → executado e aprovado
npm run build                → apenas confirmado no projeto, se não executado
pg_dump / pg_restore         → exemplo genérico, não executado
O documento não deve transformar “existe no README” em “foi testado nesta issue”.

Próxima instrução para o Antigravity
Plano aprovado.

Implemente a ISSUE #081 seguindo o plano revisado.

Crie:
- docs/deploy/checklist_demo_environment.md
- docs/deploy/walkthrough_issue_081_demo_environment_checklist.md

Execute apenas as validações documentais e locais previstas no plano.

No walkthrough, diferencie claramente:
- comandos efetivamente executados;
- comandos apenas confirmados no repositório;
- exemplos genéricos não executados.

Não implemente seed_demo.
Não altere Docker, backend ou frontend.
Não realize deploy.
Não execute commit nem push.
O plano está suficientemente completo para avançar. O bloqueio do seed não impede a documentação, mas deverá aparecer no checklist como pré-requisito pendente para uma implantação demo segura.



Markdown(2).md colado
Arquivo
Checklist, achei  bom.

Também achei bom, Manex. O checklist ficou bem acima de uma documentação genérica de deploy. Ele diferencia local, demo e produção, deixa explícita a proibição de dados reais, trata CORS, segredos, banco, backup e seed com a seriedade correta. Milagre administrativo: um documento que tenta impedir problemas antes de eles virarem reunião urgente.


O ponto mais forte é que ele não vende o ambiente demo como “produção simplificada”. A matriz comparativa deixa claras as diferenças de finalidade, debug, banco, portas, HTTPS, seed e backup. Também está correto bloquear o seed_db.py atual para demo, já que ele remove dados e usa credenciais inadequadas para exposição controlada.


Eu faria apenas quatro refinamentos editoriais no walkthrough ou antes do commit:

Em “deploy simulado”, usaria “preparação e validação planejada”, porque a issue não realiza deploy.

Em “PostgreSQL isolado em container ou local”, trocaria “local” por “instância dedicada ao ambiente demo”, evitando confusão com banco de desenvolvimento.

A exigência de HTTPS obrigatório está correta para acesso externo. Para uma demonstração restrita apenas à rede local, pode ser descrito como “obrigatório quando exposto fora de uma rede controlada”.

Não recomendaria comandos diretos para atualizar hashes no banco. Usuários e senhas devem ser criados pela aplicação ou pelo futuro seed_demo.py.

Veredito
Estrutura: APROVADA
Separação dos ambientes: APROVADA
Segurança: APROVADA
Banco e migrations: APROVADOS
Seed demo: BLOQUEIO CORRETAMENTE REGISTRADO
Backup e restauração: APROVADOS
Checklist pós-deploy: APROVADO
Pronto para walkthrough e fechamento: SIM
Agora o walkthrough precisa apenas provar o que foi realmente inspecionado e executado, distinguindo:

comandos executados
comandos confirmados no repositório
exemplos genéricos não executados
A Issue #081 pode avançar para a revisão do walkthrough.


Passo a passo:
# Walkthrough — Checklist de Ambiente Demo (Issue #081)

Este documento registra a entrega documental e as validações técnicas realizadas para a **Issue #081**, visando a criação de um guia reproduzível e seguro de preparação de ambiente demo.

---

## Resumo da implementação

Foi estruturado o checklist de provisionamento para ambiente de demonstração controlado da plataforma GTH Agents. O checklist define a separação entre ambientes (local, demo e produção), pré-requisitos, variáveis de ambiente seguras com placeholders, isolamento de banco de dados, checagens operacionais pós-deploy e procedimentos básicos de backup e restauração.

---

## Arquivos criados e alterados

Todos os arquivos estão localizados no diretório de deploy:
- [docs/deploy/implementation_plan_issue_081_demo_environment_checklist.md](docs/deploy/implementation_plan_issue_081_demo_environment_checklist.md) — O plano de implementação revisado e auditado.
- [docs/deploy/checklist_demo_environment.md](docs/deploy/checklist_demo_environment.md) — O checklist técnico contendo as 20 seções obrigatórias estruturadas.
- [docs/deploy/walkthrough_issue_081_demo_environment_checklist.md](docs/deploy/walkthrough_issue_081_demo_environment_checklist.md) — Este documento de registro final.

---

## Fontes inspecionadas

Para garantir a coerência dos comandos e variáveis descritos no checklist, as seguintes fontes do repositório foram inspecionadas:
- docker-compose.yml (raiz) — Verificação das portas padrão (5000 API, 5173 Web dev, 5432 DB) e volumes persistentes (postgres_data).
- backend/Dockerfile — Verificação do comando de inicialização Flask.
- frontend/Dockerfile.prod e nginx.conf — Verificação da compilação estática do React e suporte a SPA no Nginx na porta 80.
- backend/seed_db.py — Auditoria do comportamento destrutivo de carga de dados.
- backend/app.py — Inspeção da lógica de interceptação e checagem de CORS.
- backend/interface/routes/health_routes.py — Verificação do payload retornado pelo endpoint /health.
- backend/migrations/ — Confirmação do uso do Alembic para migrations.

---

## Decisões técnicas e lacunas identificadas

1. **Bloqueio do Seed**: O seed atual (backend/seed_db.py) realiza remoções diretas no banco de dados e utiliza credenciais estáticas de desenvolvimento. Portanto, foi registrado um **bloqueio formal** no checklist, proibindo sua execução direta em demo sem descarte planejado do banco, e recomendando-se uma issue futura para um seed dedicado parametrizável (seed_demo.py).
2. **Classificação do Health Check**: O /health foi classificado estritamente como **liveness básica** da API Flask, explicando-se no checklist que ele não garante a conectividade do banco de dados de forma isolada.
3. **CORS restritivo**: Exigência de declaração exata da origem na variável CORS_ORIGINS, vedando explicitamente o uso de wildcard *.
4. **Isolamento do DB**: Instrução no checklist para remover o mapeamento de portas públicas externas para a base PostgreSQL, mantendo o tráfego restrito à rede interna de containers.
5. **Lacuna Docker**: Identificou-se que não existe composição Docker Compose específica para o build de produção (com o frontend empacotado no Nginx). O checklist documenta essa lacuna e trata o docker-compose.yml existente como infraestrutura local de desenvolvimento.

---

## Comandos validados e sua classificação

Abaixo constam a classificação dos comandos descritos na documentação, divididos conforme o nível de execução e teste realizado nesta issue:

### 1. Comandos efetivamente executados
Estes comandos foram executados localmente na máquina durante esta tarefa para validar a integridade dos arquivos e da aplicação:
- **find docs/deploy -maxdepth 1 -type f | sort** (validou a presença dos 3 arquivos de deploy).
- **grep -R -n -E "/home/|/Users/|C:\\\\Users\\\\" docs/deploy/ --include="*.md"** (validou que nenhuma linha vazou caminhos absolutos locais de desenvolvimento).
- **grep -R -n -E "admin123|dev-secret-change-me|postgres:postgres|Bearer [A-Za-z0-9._-]+" docs/deploy/ --include="*.md"** (validou que nenhuma credencial ou chave privada foi versionada na documentação).
- **docker compose config** (validou que a sintaxe do arquivo de composição Docker está correta e coerente).
- **git diff --check** (validou a ausência de espaços em branco indevidos e conflitos de caracteres).
- **grep -n "^## " docs/deploy/checklist_demo_environment.md** (validou a presença das 20 seções obrigatórias).
- **PYTHONPATH=. .venv/bin/pytest** (executado no diretório /backend, passando todos os 208 testes da suíte automatizada sem regressões).
- **npm run lint** (executado em /frontend, garantindo a ausência de erros de formatação de código).
- **npm run build** (executado em /frontend, garantindo que a compilação de produção dos ativos estáticos funciona perfeitamente).

### 2. Comandos apenas confirmados no repositório
Estes comandos pertencem à estrutura existente no repositório do GTH Agents e seu funcionamento foi confirmado no código-fonte, mas eles não foram executados nesta issue por não haver deploy ou alteração de código operacional:
- docker compose build e docker compose up -d (pilha padrão de execução).
- docker compose ps e docker compose logs (utilitários de monitoramento).
- docker compose exec api alembic upgrade head e alembic current (comandos de migração do banco de dados).
- curl http://localhost:5000/health (resposta HTTP confirmada diretamente na rota do backend).

### 3. Exemplos genéricos não executados
Comandos conceituais descritos como modelos genéricos no checklist de deploy, cuja execução não foi realizada localmente ou contra infraestruturas externas:
- Geração de backup com pg_dump remoto/local de simulação.
- Restauração de backup com pg_restore no host ou container temporário.
- Mapeamento IP-domínio no arquivo local /etc/hosts (ex: 127.0.0.1 demo.exemplo.com).
- Configurações de Proxy Reverso em servidores Nginx externos.
- Procedimentos de rollback e restauração baseados em imagens ou tags Git em ambientes de nuvem.

---

## Conclusão

Checklist técnico concluído e pronto para orientar uma futura implantação controlada. Nenhum deploy efetivo foi realizado nesta issue.

Manex, o walkthrough está bem estruturado e quase pronto, mas há algumas inconsistências que precisam ser corrigidas antes do commit. A documentação está boa; só tentou conquistar poderes de auditoria que alguns comandos não possuem. O terminal é útil, não clarividente.

Veredito
Entrega documental: APROVADA
Separação dos comandos: APROVADA
Registro das lacunas: APROVADO
Precisão das validações: APROVADA COM AJUSTES
Links Markdown: PRECISAM DE CORREÇÃO
Pronto para commit: APÓS PEQUENOS REFINAMENTOS
1. Os links relativos estão incorretos
O walkthrough está dentro de:

docs/deploy/
Mas os links usam:

[...](docs/deploy/arquivo.md)
A partir desse diretório, isso pode ser resolvido como:

docs/deploy/docs/deploy/arquivo.md
Use links relativos ao próprio diretório:

- [Plano de implementação](implementation_plan_issue_081_demo_environment_checklist.md) — Plano revisado e auditado.
- [Checklist do ambiente demo](checklist_demo_environment.md) — Checklist técnico com as seções obrigatórias.
- [Walkthrough da Issue #081](walkthrough_issue_081_demo_environment_checklist.md) — Registro final da entrega.
Ou:

[Plano](./implementation_plan_issue_081_demo_environment_checklist.md)
2. A auditoria de credenciais pode estar contraditória
O checklist apresentado anteriormente continha literalmente:

dev-secret-change-me
na explicação sobre substituição das credenciais de desenvolvimento.

Portanto, este comando:

grep -R -n -E \
"admin123|dev-secret-change-me|postgres:postgres|Bearer [A-Za-z0-9._-]+" \
docs/deploy/ --include="*.md"
não deveria necessariamente retornar vazio.

O walkthrough afirma:

validou que nenhuma credencial ou chave privada foi versionada

Mas o grep procura também exemplos públicos de credenciais fracas, não apenas segredos reais.

A formulação correta seria:

- O comando de auditoria de padrões sensíveis foi executado.
- As correspondências encontradas, quando existentes, foram revisadas contextualmente.
- Nenhum segredo real, token válido ou credencial operacional foi identificado.
- Valores conhecidos de desenvolvimento aparecem apenas como exemplos de padrões proibidos, quando necessário.
Caso o comando realmente não tenha retornado nada porque o literal foi removido do checklist, mantenha o resultado vazio, mas registre a saída real.

3. git diff --check não valida “conflitos de caracteres”
Troque:

validou a ausência de espaços em branco indevidos e conflitos de caracteres

por:

- **`git diff --check`** — validou a ausência de erros de whitespace no diff, como espaços no final das linhas.
Ele não é um validador geral de caracteres nem substitui uma inspeção de conflitos de merge.

4. O grep dos títulos não comprova sozinho as 20 seções
Este comando:

grep -n "^## " docs/deploy/checklist_demo_environment.md
lista os títulos de segundo nível. Para dizer que confirmou 20 seções, é necessário revisar a saída ou contar:

grep -c "^## " docs/deploy/checklist_demo_environment.md
Porém, até a contagem pode incluir títulos auxiliares que não correspondam às seções obrigatórias.

Use:

- **`grep -n "^## " ...`** — listou os títulos de segundo nível.
- A saída foi revisada para confirmar a presença e a sequência das 20 seções previstas.
5. Ajustar as afirmações sobre lint e build
Troque:

npm run lint garantindo a ausência de erros de formatação de código

por:

- **`npm run lint`** — executado com sucesso, sem erros reportados pelas regras configuradas no projeto.
Lint não necessariamente valida toda a formatação, dependendo da configuração.

Troque:

garantindo que a compilação de produção dos ativos estáticos funciona perfeitamente

por:

- **`npm run build`** — executado com sucesso, gerando o build de produção sem erros.
“Perfeitamente” é uma palavra corajosa demais para um build. Ele comprova compilação, não toda a experiência funcional.

6. Corrigir a classificação do curl /health
O comando:

curl http://localhost:5000/health
não teve o funcionamento confirmado, pois não foi executado. O que foi confirmado por inspeção é o contrato da rota.

Use:

- `curl http://localhost:5000/health` — comando compatível com a rota encontrada no backend, mas não executado nesta issue.
- O endpoint e o payload esperado foram confirmados por inspeção do código-fonte.
Evite:

resposta HTTP confirmada diretamente na rota

Uma resposta HTTP só é confirmada por uma requisição real. O código confirma a implementação prevista.

7. Refinar a frase sobre o seed
A decisão está correta, mas esta frase:

proibindo sua execução direta em demo

pode ser mais precisa:

O checklist não recomenda a execução do `backend/seed_db.py` em ambiente demo persistente. Sua utilização somente seria aceitável em uma base descartável, com confirmação explícita de recriação total.
Isso fica alinhado com o próprio bloqueio, que permite apenas um cenário deliberadamente descartável.

8. Acrescentar o resultado numérico das validações
Já que foram executadas, registre:

Backend: 208 testes aprovados
Frontend lint: aprovado
Frontend build: aprovado
Docker Compose config: aprovado
git diff --check: aprovado
Deploy externo: não realizado
Para lint e build, inclua a saída resumida real, caso esteja disponível. Não invente quantidade de módulos ou duração.

Trecho corrigido para os comandos executados
### 1. Comandos efetivamente executados

Os seguintes comandos foram executados localmente durante esta issue:

- `find docs/deploy -maxdepth 1 -type f | sort`
  Confirmou a presença dos três documentos da Issue #081.

- `grep -R -n -E "/home/|/Users/|C:\\\\Users\\\\" docs/deploy/ --include="*.md"`
  Não identificou caminhos absolutos locais nos documentos finais.

- `grep -R -n -E "admin123|dev-secret-change-me|postgres:postgres|Bearer [A-Za-z0-9._-]+" docs/deploy/ --include="*.md"`
  As correspondências foram revisadas contextualmente. Nenhum segredo real, token válido ou credencial operacional foi identificado.

- `docker compose config`
  Validou a sintaxe e a resolução da composição Docker de desenvolvimento existente.

- `git diff --check`
  Não identificou erros de whitespace no diff.

- `grep -n "^## " docs/deploy/checklist_demo_environment.md`
  Listou os títulos de segundo nível, cuja saída foi revisada para confirmar a presença e a sequência das 20 seções previstas.

- `PYTHONPATH=. .venv/bin/pytest`
  Executado em `backend/`, com 208 testes aprovados.

- `npm run lint`
  Executado em `frontend/`, sem erros reportados pelas regras configuradas.

- `npm run build`
  Executado em `frontend/`, gerando o build de produção sem erros.
Conclusão recomendada
## Conclusão

A Issue #081 foi concluída dentro de seu escopo documental.

Foram entregues o plano revisado, o checklist técnico e este walkthrough. As validações locais e documentais previstas foram executadas, incluindo a suíte completa do backend, lint e build do frontend, validação do Docker Compose e inspeções contra caminhos locais e dados sensíveis.

O checklist está pronto para orientar uma futura preparação controlada de ambiente demo.

Nenhum ambiente externo foi provisionado, nenhum deploy efetivo foi realizado e os procedimentos genéricos de backup, restauração, proxy reverso e rollback não foram executados nesta issue.
Com essas correções, o walkthrough fica pronto para commit e fechamento da Issue #081.


Peça para o antigravity fazer as edições.

Use esta instrução completa no Antigravity. Ela manda ajustar apenas o walkthrough, sem começar a reformar o sistema inteiro porque encontrou uma vírgula torta.


Corrigir o Walkthrough da Issue #081 — Checklist de Ambiente Demo
Revise e corrija exclusivamente o walkthrough da:

ISSUE #081 — Checklist de Ambiente Demo
Arquivo alvo:

docs/deploy/walkthrough_issue_081_demo_environment_checklist.md
Objetivo
Refinar o walkthrough para que ele descreva com precisão:

os arquivos entregues;

as fontes inspecionadas;

as decisões técnicas adotadas;

os comandos efetivamente executados;

os comandos apenas confirmados no repositório;

os exemplos genéricos não executados;

os resultados reais das validações;

as limitações e lacunas identificadas;

o fato de que nenhum deploy efetivo foi realizado.

Não alterar nesta tarefa:

backend/
frontend/
docker-compose.yml
Dockerfiles
migrations
seed_db.py
arquivos .env
checklist_demo_environment.md
implementation_plan_issue_081_demo_environment_checklist.md
Não executar:

deploy
commit
push
merge
tag
alteração de branch
1. Corrigir os links relativos
O walkthrough está localizado dentro de:

docs/deploy/
Portanto, não utilizar links com o caminho completo repetido:

(docs/deploy/arquivo.md)
Substituir a seção de arquivos criados e alterados por links relativos ao próprio diretório:

## Arquivos criados e alterados

Todos os arquivos da Issue #081 estão localizados em `docs/deploy/`:

- [Plano de implementação](implementation_plan_issue_081_demo_environment_checklist.md) — Plano revisado e auditado.
- [Checklist do ambiente demo](checklist_demo_environment.md) — Checklist técnico contendo as seções obrigatórias.
- [Walkthrough da Issue #081](walkthrough_issue_081_demo_environment_checklist.md) — Registro final da entrega e das validações realizadas.
Confirmar que os links apontam para arquivos realmente existentes.

2. Refinar a descrição do seed
Na seção sobre o seed, evitar formulações absolutas que possam sugerir que ele nunca poderia ser executado em nenhuma circunstância.

Utilizar formulação equivalente a:

1. **Bloqueio do seed atual**: O arquivo `backend/seed_db.py` realiza remoções diretas de registros e carrega dados estáticos de desenvolvimento.

   O checklist não recomenda sua execução em ambiente demo persistente.

   Sua utilização somente seria aceitável em uma base explicitamente descartável, com confirmação de que o banco pode ser completamente recriado.

   Foi registrada como melhoria futura a criação de um `backend/seed_demo.py` parametrizável, não destrutivo por padrão e adequado à demonstração.
Não reproduzir senhas literais encontradas no seed.

3. Corrigir a descrição da auditoria de padrões sensíveis
O comando abaixo pode localizar exemplos conceituais de padrões proibidos:

grep -R -n -E \
"admin123|dev-secret-change-me|postgres:postgres|Bearer [A-Za-z0-9._-]+" \
docs/deploy/ \
--include="*.md"
Portanto, não afirmar automaticamente que ele retornou vazio, a menos que isso tenha realmente ocorrido.

Substituir a explicação por:

- **Auditoria de padrões sensíveis**

  ```bash
  grep -R -n -E \
  "admin123|dev-secret-change-me|postgres:postgres|Bearer [A-Za-z0-9._-]+" \
  docs/deploy/ \
  --include="*.md"
As correspondências encontradas, quando existentes, foram revisadas contextualmente.

Nenhum segredo real, token válido ou credencial operacional foi identificado nos documentos finais.

Valores conhecidos de desenvolvimento somente podem aparecer como exemplos de padrões proibidos ou alertas técnicos, nunca como credenciais recomendadas.


Registrar a saída real observada durante a execução.

Não inventar resultado vazio.

---

# 4. Corrigir a descrição do `git diff --check`

Substituir:

```text
validou a ausência de espaços em branco indevidos e conflitos de caracteres
por:

- **`git diff --check`** — não identificou erros de whitespace no diff, como espaços no final das linhas.
Não atribuir ao comando validação de:

conflitos de merge
caracteres inválidos
sintaxe Markdown
links
conteúdo técnico
5. Corrigir a validação das 20 seções
O comando:

grep -n "^## " docs/deploy/checklist_demo_environment.md
apenas lista os títulos de segundo nível.

Substituir a explicação por:

- **Estrutura das seções**

  ```bash
  grep -n "^## " docs/deploy/checklist_demo_environment.md
O comando listou os títulos de segundo nível.

A saída foi revisada para confirmar a presença e a sequência das 20 seções previstas no escopo da Issue #081.


Se também tiver sido executado:

```bash
grep -c "^## " docs/deploy/checklist_demo_environment.md
registrar o resultado real.

Não afirmar que a simples execução do grep comprova sozinha a qualidade ou completude das seções.

6. Corrigir as afirmações sobre lint
Substituir:

garantindo a ausência de erros de formatação de código
por:

- **`npm run lint`** — executado no diretório `frontend/`, sem erros reportados pelas regras configuradas no projeto.
Não afirmar que o lint valida toda a formatação, a menos que exista ferramenta específica configurada para isso.

7. Corrigir as afirmações sobre build
Substituir:

garantindo que a compilação de produção dos ativos estáticos funciona perfeitamente
por:

- **`npm run build`** — executado no diretório `frontend/`, gerando o build de produção sem erros.
Não usar:

perfeitamente
totalmente validado
pronto para produção
O build comprova a compilação, não todos os fluxos funcionais.

8. Corrigir a classificação do health check
O comando:

curl http://localhost:5000/health
não foi executado nesta issue.

Portanto, substituir a descrição por:

- `curl http://localhost:5000/health` — comando compatível com a rota encontrada no backend, mas não executado nesta issue.

- O endpoint `GET /health` e o payload esperado foram confirmados por inspeção do código-fonte em `backend/interface/routes/health_routes.py`.

- Como não houve requisição real nesta tarefa, nenhuma resposta HTTP foi declarada como validada.
Manter a classificação:

liveness básica
Não descrever /health como readiness completa.

9. Refinar a validação do Docker Compose
Na seção de comandos executados, utilizar:

- **`docker compose config`** — executado na raiz do monorepo, validando a sintaxe e a resolução da composição Docker de desenvolvimento existente.
Não declarar que esse comando validou:

execução dos containers
saúde da aplicação
conectividade com o banco
build de produção
deploy demo
Esses itens não foram executados nesta issue.

10. Registrar corretamente os testes backend
Manter:

- **`PYTHONPATH=. .venv/bin/pytest`** — executado no diretório `backend/`, com 208 testes aprovados.
Não usar expressões como:

100% de cobertura
validação completa
garantia total
A menos que essas métricas tenham sido efetivamente produzidas.

11. Reescrever a seção de comandos executados
Substituir a seção atual por uma versão equivalente a:

### 1. Comandos efetivamente executados

Os seguintes comandos foram executados localmente durante esta issue:

- `find docs/deploy -maxdepth 1 -type f | sort`
  Confirmou a presença dos três documentos da Issue #081.

- `grep -R -n -E "/home/|/Users/|C:\\\\Users\\\\" docs/deploy/ --include="*.md"`
  Não identificou caminhos absolutos locais nos documentos finais.

- `grep -R -n -E "admin123|dev-secret-change-me|postgres:postgres|Bearer [A-Za-z0-9._-]+" docs/deploy/ --include="*.md"`
  As correspondências foram revisadas contextualmente. Nenhum segredo real, token válido ou credencial operacional foi identificado.

- `docker compose config`
  Validou a sintaxe e a resolução da composição Docker de desenvolvimento existente.

- `git diff --check`
  Não identificou erros de whitespace no diff.

- `grep -n "^## " docs/deploy/checklist_demo_environment.md`
  Listou os títulos de segundo nível. A saída foi revisada para confirmar a presença e a sequência das 20 seções previstas.

- `PYTHONPATH=. .venv/bin/pytest`
  Executado em `backend/`, com 208 testes aprovados.

- `npm run lint`
  Executado em `frontend/`, sem erros reportados pelas regras configuradas no projeto.

- `npm run build`
  Executado em `frontend/`, gerando o build de produção sem erros.
Preservar apenas resultados realmente observados.

12. Manter separação entre os três tipos de comando
O walkthrough deve continuar separando claramente:

Comandos efetivamente executados
Exemplos:

find
grep
docker compose config
git diff --check
pytest
npm run lint
npm run build
Comandos apenas confirmados no repositório
Exemplos:

docker compose build
docker compose up -d
docker compose ps
docker compose logs
docker compose exec api alembic upgrade head
alembic current
curl /health
Acrescentar para esta categoria:

Esses comandos foram considerados compatíveis com a estrutura atual do repositório por inspeção dos arquivos e configurações, mas não foram executados nesta issue.
Exemplos genéricos não executados
Manter:

pg_dump
pg_restore
/etc/hosts
proxy reverso
TLS
rollback
infraestrutura cloud
Acrescentar:

Esses comandos e procedimentos foram documentados apenas como modelos genéricos e não foram validados contra infraestrutura externa.
13. Refinar os termos sobre deploy
Evitar no walkthrough expressões que possam sugerir implantação real, como:

deploy validado
ambiente implantado
infraestrutura provisionada
pós-deploy executado
produção simulada
Usar:

preparação documental
validação local
orientação para futura implantação
comandos de referência
checklist pós-implantação futura
Manter explicitamente:

Nenhum deploy efetivo foi realizado nesta issue.
14. Atualizar o resumo das validações
Adicionar próximo à conclusão:

## Resultado consolidado das validações

```text
Documentos da Issue #081: 3 arquivos confirmados
Backend: 208 testes aprovados
Frontend lint: aprovado
Frontend build: aprovado
Docker Compose config: aprovado
git diff --check: aprovado
Caminhos absolutos locais: não identificados
Segredos reais ou tokens válidos: não identificados
Deploy externo: não realizado
Backup e restauração: não executados
Proxy reverso e TLS: não configurados

Não incluir duração, quantidade de módulos compilados ou outras métricas sem evidência real.

---

# 15. Substituir a conclusão

Utilizar uma conclusão equivalente a:

```md
## Conclusão

A Issue #081 foi concluída dentro de seu escopo documental.

Foram entregues o plano revisado, o checklist técnico e este walkthrough. As validações locais e documentais previstas foram executadas, incluindo a suíte completa do backend, lint e build do frontend, validação do Docker Compose e inspeções contra caminhos locais e dados sensíveis.

O checklist está pronto para orientar uma futura preparação controlada de ambiente demo.

Nenhum ambiente externo foi provisionado, nenhum deploy efetivo foi realizado e os procedimentos genéricos de backup, restauração, proxy reverso, TLS e rollback não foram executados nesta issue.
16. Validações após a edição
Após corrigir o walkthrough, executar:

find docs/deploy -maxdepth 1 -type f | sort

grep -R -n -E \
"/home/|/Users/|C:\\\\Users\\\\" \
docs/deploy/ \
--include="*.md"

grep -R -n -E \
"admin123|dev-secret-change-me|postgres:postgres|Bearer [A-Za-z0-9._-]+" \
docs/deploy/ \
--include="*.md"

grep -n "^## " \
docs/deploy/walkthrough_issue_081_demo_environment_checklist.md

git diff --check
Revisar contextualmente qualquer correspondência encontrada.

Confirmar também os links relativos:

implementation_plan_issue_081_demo_environment_checklist.md
checklist_demo_environment.md
walkthrough_issue_081_demo_environment_checklist.md
17. Relatório final
Ao concluir, apresentar:

- arquivo alterado;
- links relativos corrigidos;
- seções revisadas;
- afirmações técnicas refinadas;
- resultados reais dos comandos de validação;
- correspondências encontradas nas buscas;
- confirmação de que nenhum segredo real foi identificado;
- resultado do git diff --check;
- confirmação de que somente o walkthrough foi alterado;
- confirmação de que nenhum deploy foi executado;
- confirmação de que commit e push não foram executados.
A conclusão do relatório deve ser semelhante a:

Walkthrough da Issue #081 corrigido e pronto para revisão final. Nenhum deploy, commit ou push foi executado.
Depois disso, basta revisar a versão corrigida e partir para o commit. Humanos conseguiram transformar até documentação de não deploy em uma pequena auditoria, mas neste caso vale a pena.


E agora?
# Walkthrough — Checklist de Ambiente Demo (Issue #081)

Este documento registra a entrega documental e as validações técnicas realizadas para a **Issue #081**, visando a criação de um guia reproduzível e seguro de preparação de ambiente de demonstração controlado para o GTH Agents.

---

## Resumo da implementação

Foi estruturado o checklist de provisionamento para ambiente de demonstração controlado da plataforma GTH Agents. O checklist define a separação entre ambientes (local, demo e produção), pré-requisitos, variáveis de ambiente seguras com placeholders, isolamento de banco de dados, checagens operacionais pós-deploy e procedimentos básicos de backup e restauração.

---

## Arquivos criados e alterados

Todos os arquivos da Issue #081 estão localizados em docs/deploy/:

- [Plano de implementação](implementation_plan_issue_081_demo_environment_checklist.md) — Plano revisado e auditado.
- [Checklist do ambiente demo](checklist_demo_environment.md) — Checklist técnico contendo as seções obrigatórias.
- [Walkthrough da Issue #081](walkthrough_issue_081_demo_environment_checklist.md) — Registro final da entrega e das validações realizadas.

---

## Fontes inspecionadas

Para garantir a coerência dos comandos e variáveis descritos no checklist, as seguintes fontes do repositório foram inspecionadas:
- docker-compose.yml (raiz) — Verificação das portas padrão (5000 API, 5173 Web dev, 5432 DB) e volumes persistentes (postgres_data).
- backend/Dockerfile — Verificação do comando de inicialização Flask.
- frontend/Dockerfile.prod e nginx.conf — Verificação da compilação estática do React e suporte a SPA no Nginx na porta 80.
- backend/seed_db.py — Auditoria do comportamento de carga e deleção de dados.
- backend/app.py — Inspeção da lógica de interceptação e checagem de CORS.
- backend/interface/routes/health_routes.py — Verificação do payload retornado pelo endpoint /health.
- backend/migrations/ — Confirmação do uso do Alembic para migrations.

---

## Decisões técnicas e lacunas identificadas

1. **Bloqueio do seed atual**: O arquivo backend/seed_db.py realiza remoções diretas de registros e carrega dados estáticos de desenvolvimento. O checklist não recomenda sua execução em ambiente demo persistente. Sua utilização somente seria aceitável em uma base explicitamente descartável, com confirmação de que o banco pode ser completamente recriado. Foi registrada como melhoria futura a criação de um backend/seed_demo.py parametrizável, não destrutivo por padrão e adequado à demonstração.
2. **Classificação do Health Check**: O /health foi classificado estritamente como **liveness básica** da API Flask, explicando-se no checklist que ele não garante a conectividade do banco de dados de forma isolada.
3. **CORS restritivo**: Exigência de declaração exata da origem na variável CORS_ORIGINS, vedando explicitamente o uso de wildcard *.
4. **Isolamento do DB**: Instrução no checklist para remover o mapeamento de portas públicas externas para a base PostgreSQL, mantendo o tráfego restrito à rede interna de containers.
5. **Lacuna Docker**: Identificou-se que não existe composição Docker Compose específica para o build de produção (com o frontend empacotado no Nginx). O checklist documenta essa lacuna e trata o docker-compose.yml existente como infraestrutura local de desenvolvimento. A criação de uma composição demo será tratada em issue futura.

---

## Comandos validados e sua classificação

Abaixo consta a classificação dos comandos descritos na documentação, divididos conforme o nível de execução e teste realizado nesta issue:

### 1. Comandos efetivamente executados

Os seguintes comandos foram executados localmente durante esta issue:

- find docs/deploy -maxdepth 1 -type f | sort
  Confirmou a presença dos três documentos da Issue #081.

- grep -R -n -E "/home/|/Users/|C:\\\\Users\\\\" docs/deploy/ --include="*.md"
  Não identificou caminhos absolutos locais nos documentos finais (a correspondência encontrada foi na própria linha de instrução de busca no plano de implementação).

- grep -R -n -E "admin123|dev-secret-change-me|postgres:postgres|Bearer [A-Za-z0-9._-]+" docs/deploy/ --include="*.md"
  As correspondências encontradas foram revisadas contextualmente:
  * docs/deploy/checklist_demo_environment.md:19 (menção técnica para substituição do segredo dev-secret-change-me).
  * docs/deploy/implementation_plan_issue_081_demo_environment_checklist.md:178 (registro do comando de auditoria em si).
  * docs/deploy/walkthrough_issue_081_demo_environment_checklist.md:53 (registro do comando de auditoria no walkthrough).
  Nenhum segredo real, token válido ou credencial operacional foi identificado. Valores conhecidos de desenvolvimento aparecem apenas como exemplos de padrões proibidos ou alertas técnicos, nunca como credenciais recomendadas.

- docker compose config
  Validou a sintaxe e a resolução da composição Docker de desenvolvimento existente.

- git diff --check
  Não identificou erros de whitespace no diff, como espaços no final das linhas.

- grep -n "^## " docs/deploy/checklist_demo_environment.md
  Listou os títulos de segundo nível. A saída foi revisada para confirmar a presença e a sequência das 20 seções previstas no escopo da Issue #081. Adicionalmente, o comando grep -c "^## " docs/deploy/checklist_demo_environment.md confirmou a contagem de 20 seções.

- PYTHONPATH=. .venv/bin/pytest
  Executado em backend/, com 208 testes aprovados.

- npm run lint
  Executado em frontend/, sem erros reportados pelas regras configuradas no projeto.

- npm run build
  Executado em frontend/, gerando o build de produção sem erros.

---

### 2. Comandos apenas confirmados no repositório

Esses comandos foram considerados compatíveis com a estrutura atual do repositório por inspeção dos arquivos e configurações, mas não foram executados nesta issue:
- docker compose build e docker compose up -d (pilha de containers de desenvolvimento).
- docker compose ps e docker compose logs (monitoramento de containers).
- docker compose exec api alembic upgrade head e alembic current (atualização e checagem de migrations no container).
- curl http://localhost:5000/health — comando compatível com a rota encontrada no backend, mas não executado nesta issue. O endpoint GET /health e o payload esperado foram confirmados por inspeção do código-fonte em backend/interface/routes/health_routes.py. Como não houve requisição real nesta tarefa, nenhuma resposta HTTP foi declarada como validada.

---

### 3. Exemplos genéricos não executados

Esses comandos e procedimentos foram documentados apenas como modelos genéricos e não foram validados contra infraestrutura externa:
- Geração de backup local/remoto via pg_dump.
- Restauração de backup via pg_restore (incluindo testes em container temporário).
- Configuração de domínio e mapeamentos DNS no arquivo /etc/hosts local.
- Configuração de Proxy Reverso, roteamento Nginx e instalação de certificados TLS/HTTPS.
- Ações de rollback de código ou infraestrutura cloud.

---

## Resultado consolidado das validações

text
Documentos da Issue #081: 3 arquivos confirmados
Backend: 208 testes aprovados
Frontend lint: aprovado
Frontend build: aprovado
Docker Compose config: aprovado
git diff --check: aprovado
Caminhos absolutos locais: não identificados
Segredos reais ou tokens válidos: não identificados
Deploy externo: não realizado
Backup e restauração: não executados
Proxy reverso e TLS: não configurados


---

## Conclusão

A Issue #081 foi concluída dentro de seu escopo documental.

Foram entregues o plano revisado, o checklist técnico e este walkthrough. As validações locais e documentais previstas foram executadas, incluindo a suíte completa do backend, lint e build do frontend, validação do Docker Compose e inspeções contra caminhos locais e dados sensíveis.

O checklist está pronto para orientar uma futura preparação controlada de ambiente demo.

Nenhum ambiente externo foi provisionado, nenhum deploy efetivo foi realizado e os procedimentos genéricos de backup, restauração, proxy reverso, TLS e rollback não foram executados nesta issue.

Agora sim, Manex. O walkthrough ficou coerente, preciso e pronto para commit.

Veredito final
Entrega documental: APROVADA
Plano de implementação: APROVADO
Checklist técnico: APROVADO
Walkthrough: APROVADO
Links relativos: CORRETOS
Classificação dos comandos: CORRETA
Validações locais: COMPROVADAS
Limitações registradas: CORRETAS
Deploy efetivo: NÃO REALIZADO
Pronto para commit: SIM
Os pontos problemáticos da versão anterior foram corrigidos:

os links agora são relativos ao diretório docs/deploy/;

o seed está corretamente tratado como inadequado para demo persistente;

as correspondências do grep foram registradas e revisadas contextualmente;

git diff --check foi descrito apenas como validação de whitespace;

as 20 seções foram confirmadas com listagem e contagem;

lint e build foram descritos sem exageros;

/health foi separado entre inspeção de código e execução HTTP;

comandos executados, confirmados e genéricos estão claramente diferenciados;

a conclusão não sugere que houve provisionamento ou deploy real.

Um único refinamento editorial opcional
No resumo aparece:

“Foi estruturado o checklist de provisionamento”

Como nenhum ambiente foi provisionado, eu usaria:

Foi estruturado o checklist de preparação de um ambiente de demonstração controlado da plataforma GTH Agents.
Isso evita uma pequena ambiguidade. Não é bloqueio para commit.

Próximo passo
Na raiz do monorepo:

cd ~/Workspaces/projects/antigravity/gth-agents

git branch --show-current
git status
git diff --stat
git diff --check
Confira os arquivos:

git status --short
Esperado:

docs/deploy/implementation_plan_issue_081_demo_environment_checklist.md
docs/deploy/checklist_demo_environment.md
docs/deploy/walkthrough_issue_081_demo_environment_checklist.md
Adicione apenas os documentos da Issue #081:

git add \
  docs/deploy/implementation_plan_issue_081_demo_environment_checklist.md \
  docs/deploy/checklist_demo_environment.md \
  docs/deploy/walkthrough_issue_081_demo_environment_checklist.md
Revise o stage:

git diff --cached --stat
git diff --cached --check
git diff --cached
Mensagem recomendada:

git commit -m "docs(deploy): add demo environment checklist"
Depois:

git status
git log -1 --oneline
A Issue #081 está documentalmente concluída. Nenhum deploy foi feito, nenhum ambiente demo nasceu magicamente, mas ao menos o próximo humano terá instruções melhores do que “suba os containers e veja no que dá”.


No comando 'git diff --cached --check' apresentou vários espaços em vários arquivo, como resolvo?

Manex, isso normalmente significa espaços ou tabs no final das linhas dos arquivos já adicionados ao stage. O Git resolveu exercer sua função de fiscal de rodapé, porque alguém precisa.

Primeiro veja exatamente quais linhas estão com problema:

git diff --cached --check
A saída costuma aparecer assim:

docs/deploy/checklist_demo_environment.md:42: trailing whitespace.
+Texto da linha··
Correção recomendada
Como são apenas os três documentos da Issue #081, remova-os temporariamente do stage sem perder as alterações:

git restore --staged docs/deploy/
Agora elimine espaços e tabs no final das linhas:

sed -i 's/[[:space:]]\+$//' \
  docs/deploy/implementation_plan_issue_081_demo_environment_checklist.md \
  docs/deploy/checklist_demo_environment.md \
  docs/deploy/walkthrough_issue_081_demo_environment_checklist.md
Depois confira o diff não staged:

git diff --check
Se não houver saída, adicione os arquivos novamente:

git add \
  docs/deploy/implementation_plan_issue_081_demo_environment_checklist.md \
  docs/deploy/checklist_demo_environment.md \
  docs/deploy/walkthrough_issue_081_demo_environment_checklist.md
E valide:

git diff --cached --check
Resultado esperado:

nenhuma saída
Atenção com Markdown
Em Markdown, dois espaços no final de uma linha podem ser usados intencionalmente para criar quebra de linha:

Primeira linha··
Segunda linha
O comando sed removerá esses espaços. Nos documentos do projeto, prefira uma linha em branco entre parágrafos:

Primeira linha

Segunda linha
Ou use <br> quando uma quebra explícita for realmente necessária:

Primeira linha<br>
Segunda linha
Isso evita manter whitespace invisível, essa extraordinária forma de o texto parecer correto enquanto o Git protesta.

Conferência final
git status --short
git diff --cached --stat
git diff --cached --check
Se o último comando não imprimir nada, pode seguir para:

git commit -m "docs(deploy): add demo environment checklist"

O Pull request, como fica?

Para essa Issue #081, eu usaria um PR documental, sem fingir que nasceu uma infraestrutura demo pronta. Porque documentação boa descreve o que existe, não o universo paralelo onde o deploy já aconteceu.

Título do Pull Request
docs(deploy): add demo environment checklist
Descrição do Pull Request
Objetivo
Adicionar a documentação técnica necessária para orientar a futura preparação de um ambiente de demonstração controlado do GTH Agents.

Closes #81

Contexto
Antes de disponibilizar o sistema para demonstrações, era necessário consolidar em um único checklist os requisitos mínimos de configuração, segurança, banco de dados, migrations, validação operacional, backup e rollback.

Esta issue possui escopo exclusivamente documental.

Nenhum ambiente externo foi provisionado e nenhum deploy efetivo foi realizado.

Entregas
Foram adicionados os seguintes documentos:

docs/deploy/implementation_plan_issue_081_demo_environment_checklist.md
docs/deploy/checklist_demo_environment.md
docs/deploy/walkthrough_issue_081_demo_environment_checklist.md
Plano de implementação
Registra:

inspeção do estado atual do repositório;

variáveis de ambiente existentes;

estrutura Docker;

comportamento do seed atual;

decisões sobre CORS;

estratégia básica de backup e restauração;

riscos e lacunas identificadas;

critérios de validação documental.

Checklist de ambiente demo
O checklist contém 20 seções cobrindo:

objetivo e limites do ambiente;

comparação entre local, demo e produção;

pré-requisitos;

variáveis de ambiente;

geração e armazenamento de segredos;

banco de dados isolado;

migrations Alembic;

dados fictícios;

bloqueio do seed atual;

build do backend e frontend;

portas internas e exposição pública;

CORS;

HTTPS e proxy reverso;

logs;

health check;

validação funcional;

backup;

restauração;

rollback;

encerramento e limpeza do ambiente.

Walkthrough
Registra:

fontes do repositório inspecionadas;

decisões técnicas adotadas;

lacunas identificadas;

comandos efetivamente executados;

comandos apenas confirmados no repositório;

exemplos genéricos não executados;

resultados consolidados das validações.

Decisões técnicas
Seed atual
O arquivo backend/seed_db.py foi classificado como inadequado para um ambiente demo persistente porque:

remove registros existentes;

carrega dados estáticos de desenvolvimento;

utiliza uma estratégia incompatível com preservação segura da base.

Sua execução somente é aceitável em uma base explicitamente descartável e com confirmação de recriação total.

Foi registrada como melhoria futura a criação de um backend/seed_demo.py parametrizável e não destrutivo por padrão.

Health check
O endpoint:

GET /health
foi classificado como uma verificação básica de liveness da API Flask.

Ele não comprova isoladamente:

conectividade com PostgreSQL;

migrations aplicadas;

autenticação;

disponibilidade funcional completa;

readiness do ambiente.

CORS
O checklist exige origens completas e explícitas por meio de:

CORS_ORIGINS=https://demo.exemplo.com
Não são recomendados wildcard global ou liberação irrestrita de origens.

Banco de dados
O PostgreSQL deve permanecer acessível somente pela rede interna dos containers, sem exposição pública desnecessária da porta 5432.

Docker
Foi identificada uma lacuna:

existe frontend/Dockerfile.prod;

não existe uma composição Docker Compose específica para ambiente demo utilizando o frontend empacotado com Nginx.

O docker-compose.yml atual foi documentado como infraestrutura de desenvolvimento local.

A criação de uma composição específica para demo permanece fora do escopo desta issue.

Validações executadas
Documentação
✓ três arquivos da Issue #081 confirmados
✓ 20 seções obrigatórias confirmadas
✓ links relativos revisados
✓ caminhos absolutos locais não identificados
✓ padrões sensíveis revisados contextualmente
✓ nenhum segredo real ou token válido identificado
✓ git diff --check aprovado
Backend
208 testes aprovados
Comando:

cd backend
PYTHONPATH=. .venv/bin/pytest
Frontend
npm run lint  → aprovado
npm run build → aprovado
Docker Compose
docker compose config → aprovado
O comando validou a sintaxe e a resolução da composição de desenvolvimento existente.

Comandos não executados
Os seguintes procedimentos foram documentados apenas como referência:

docker compose build;

docker compose up -d;

migrations em ambiente demo;

requisição real ao /health;

pg_dump;

pg_restore;

configuração de proxy reverso;

configuração de domínio;

TLS/HTTPS;

rollback em infraestrutura externa.

Fora do escopo
Não foram implementados nesta issue:

ambiente demo real;

deploy externo;

Docker Compose específico para demo;

seed dedicado para demonstração;

automação de backup;

retenção e criptografia de backups;

readiness check completo;

proxy reverso;

domínio;

TLS;

infraestrutura cloud.

Resultado
A documentação está pronta para orientar uma futura preparação controlada do ambiente demo, deixando explícitos os pré-requisitos, riscos, bloqueios e verificações necessárias.

Nenhum deploy efetivo foi realizado.

Antes de abrir o PR, confira:

git status
git log -1 --oneline
git push -u origin HEAD
No GitHub:

base: main
compare: branch da Issue #081
Esse PR pode ser marcado como pronto para revisão, não como draft, já que a entrega documental e as validações foram concluídas.


Comentario do @Codex:
P1 Badge Export JWT and CORS settings to the API container

When this checklist is followed with the Docker Compose commands later in the guide, putting these values only in /backend/.env does not make them visible inside api: both compose files pass only FLASK_APP, FLASK_ENV, SECRET_KEY, and DATABASE_URL, while the code falls back to JWT_SECRET_KEY=dev-jwt-secret-change-me and CORS_ORIGINS=http://localhost:5173. Docker's Compose docs state that a container's environment is not set until the service has an explicit environment or env_file entry, so an exposed demo would either keep forgeable development JWTs or reject the real demo origin unless the guide also adds env_file: ./backend/.env/explicit entries or uses a compose file that exports these variables.

Pensou por 13s
O Codex está correto. É um comentário P1 válido e precisa ser corrigido antes do merge.

O problema é que o arquivo:

backend/.env
não entra automaticamente no ambiente do container api. O Compose usa .env principalmente para interpolar valores no próprio YAML. Para uma variável existir dentro do container, o serviço precisa recebê-la por environment, env_file ou outro mecanismo explícito. Quando environment e env_file coexistem, environment possui precedência.

Risco real
Se o serviço api recebe somente:

environment:
  FLASK_APP: ...
  FLASK_ENV: ...
  SECRET_KEY: ...
  DATABASE_URL: ...
então estas variáveis não chegam ao processo Flask:

JWT_SECRET_KEY
JWT_ALGORITHM
JWT_EXPIRES_MINUTES
CORS_ORIGINS
POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD
Consequentemente, o backend pode utilizar os fallbacks de desenvolvimento:

JWT_SECRET_KEY=dev-jwt-secret-change-me
CORS_ORIGINS=http://localhost:5173
O primeiro representa risco de segurança. O segundo faria o frontend publicado em outro domínio falhar no CORS. Um belo ambiente “demo seguro” usando segredo falsificável e bloqueando o próprio frontend, combinação quase artística.

Correção recomendada
Como a Issue #081 é documental e já identificou que não existe Compose específico para demo, eu não alteraria silenciosamente o Compose atual de desenvolvimento.

Corrija o checklist para declarar:

O docker-compose.yml atual não está pronto para ambiente demo.

Criar apenas backend/.env não injeta automaticamente todas as variáveis no container.

Antes de qualquer demo, deverá existir um Compose adicional ou override que forneça explicitamente as variáveis ao serviço api.

O operador deve validar a configuração resolvida antes de subir os containers.

Exemplo documental recomendado
services:
  api:
    env_file:
      - ./backend/.env
    environment:
      FLASK_APP: ${FLASK_APP:-app:create_app}
      FLASK_ENV: ${FLASK_ENV:-production}
Nesse modelo, as demais variáveis presentes em backend/.env entram no container pelo env_file.

Outra opção é enumerar tudo:

services:
  api:
    environment:
      FLASK_APP: ${FLASK_APP:-app:create_app}
      FLASK_ENV: ${FLASK_ENV:-production}
      SECRET_KEY: ${SECRET_KEY:?SECRET_KEY obrigatória}
      DATABASE_URL: ${DATABASE_URL:?DATABASE_URL obrigatória}
      JWT_SECRET_KEY: ${JWT_SECRET_KEY:?JWT_SECRET_KEY obrigatória}
      JWT_ALGORITHM: ${JWT_ALGORITHM:-HS256}
      JWT_EXPIRES_MINUTES: ${JWT_EXPIRES_MINUTES:-60}
      CORS_ORIGINS: ${CORS_ORIGINS:?CORS_ORIGINS obrigatória}
Eu prefiro uma composição específica:

docker-compose.demo.yml
ou:

compose.demo.yml
com:

services:
  api:
    env_file:
      - ./backend/.env.demo
E execução:

docker compose \
  -f docker-compose.yml \
  -f docker-compose.demo.yml \
  config
O docker compose config permite inspecionar a configuração final resultante, incluindo merges e interpolações. Porém, o relatório não deve exibir valores secretos resolvidos.

Importante sobre segredos
Um arquivo de ambiente protegido é aceitável para uma demo controlada, mas segredos não devem ser incorporados à imagem Docker nem versionados. Para uma infraestrutura mais madura, Docker Compose também oferece secrets, com acesso concedido explicitamente aos serviços.

Texto para responder ao Codex
Concordo. O checklist pressupunha incorretamente que as variáveis definidas em backend/.env seriam disponibilizadas automaticamente ao container api.

O docker-compose.yml atual exporta apenas parte das configurações necessárias, o que permitiria ao backend utilizar os fallbacks de desenvolvimento para JWT_SECRET_KEY e CORS_ORIGINS.

Vou ajustar a documentação para:

classificar o Compose atual como inadequado para uma demo segura sem override;

informar que backend/.env precisa ser associado explicitamente ao serviço por env_file ou por entradas em environment;

incluir um exemplo de composição/override específico para demo;

exigir a validação da configuração resolvida com docker compose config;

manter segredos e arquivos .env fora do Git.

A correção permanecerá dentro do escopo documental da Issue #081; nenhuma alteração operacional no Compose será incluída neste PR.

Ajustes necessários nos documentos
Atualize os três arquivos:

docs/deploy/implementation_plan_issue_081_demo_environment_checklist.md
docs/deploy/checklist_demo_environment.md
docs/deploy/walkthrough_issue_081_demo_environment_checklist.md
No walkthrough, registre a lacuna assim:

### Injeção de variáveis no container da API

Durante a revisão foi identificado que o `docker-compose.yml` atual não
disponibiliza ao serviço `api` todas as variáveis necessárias para uma
demonstração segura.

A criação isolada de `backend/.env` não garante que seus valores estejam
presentes no ambiente do container.

Antes de uma implantação demo, deverá ser criada uma composição adicional
ou override que utilize `env_file` ou declare explicitamente, no mínimo:

- `JWT_SECRET_KEY`;
- `JWT_ALGORITHM`;
- `JWT_EXPIRES_MINUTES`;
- `CORS_ORIGINS`.

Enquanto essa configuração não existir, o Compose atual deve ser tratado
exclusivamente como infraestrutura de desenvolvimento local.
Veredito
Comentário Codex: PROCEDENTE
Prioridade P1: JUSTIFICADA
Risco de JWT inseguro: REAL
Risco de CORS incorreto: REAL
PR pronto para merge: NÃO
Ação: corrigir plano, checklist e walkthrough
Alteração de código/Compose nesta issue: NÃO
Depois da correção, execute novamente:

git diff --check
git diff --cached --check
E atualize o PR sem mudar sua natureza documental.


Já fiz o merge e agora??

Calma, Manex. O merge não transforma o repositório em material radioativo. Como o problema está na documentação, a correção certa agora é abrir uma issue de correção documental e um PR pequeno sobre a main.

Não reverta o merge inteiro. Isso apagaria documentos úteis só porque um trecho ficou tecnicamente incompleto, a versão Git de demolir a casa porque esqueceram uma tomada.

1. Atualize a main
cd ~/Workspaces/projects/antigravity/gth-agents

git switch main
git pull origin main
git status
O esperado é a árvore limpa.

2. Crie uma branch de correção
git switch -c fix/issue-081-document-compose-env-injection
3. Abra uma issue complementar
Título recomendado:

fix(docs): corrigir injeção de variáveis JWT e CORS no ambiente demo
Descrição resumida:

## Problema

A documentação da Issue #081 orienta a criação de `backend/.env`, mas o
`docker-compose.yml` atual não injeta automaticamente todas essas variáveis
no container `api`.

Sem `env_file` ou entradas explícitas em `environment`, o backend pode usar
os valores padrão de desenvolvimento para:

- `JWT_SECRET_KEY`;
- `JWT_ALGORITHM`;
- `JWT_EXPIRES_MINUTES`;
- `CORS_ORIGINS`.

## Risco

- JWTs assinados com segredo padrão de desenvolvimento;
- domínio real da demonstração rejeitado pelo CORS;
- falsa impressão de que o Compose atual está pronto para demo.

## Escopo

Corrigir exclusivamente:

- plano de implementação da Issue #081;
- checklist do ambiente demo;
- walkthrough da Issue #081.

Não alterar o Compose neste momento.

## Critérios de aceite

- deixar explícito que `backend/.env` não é injetado automaticamente;
- exigir `env_file` ou declaração explícita em `environment`;
- incluir exemplo de override demo;
- classificar o Compose atual como desenvolvimento;
- manter segredos fora do Git.
4. Corrija os três documentos
docs/deploy/implementation_plan_issue_081_demo_environment_checklist.md
docs/deploy/checklist_demo_environment.md
docs/deploy/walkthrough_issue_081_demo_environment_checklist.md
No checklist, inclua uma seção semelhante a esta:

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

O `docker-compose.yml` atual não deve ser considerado adequado para uma demo
segura sem uma composição adicional ou override.
Inclua um exemplo não operacional e sem segredos reais:

services:
  api:
    env_file:
      - ./backend/.env.demo
    environment:
      FLASK_ENV: production
E deixe claro:

backend/.env.demo não deve ser versionado
5. Atualize o walkthrough
Registre que a lacuna foi identificada após a revisão do PR:

### Correção posterior à revisão

Após o merge inicial da Issue #081, foi identificado que o checklist não
explicava adequadamente a necessidade de injetar as variáveis do arquivo de
ambiente no container `api`.

A documentação foi corrigida em PR complementar. Nenhuma configuração
operacional do Docker Compose foi alterada nesta correção.
Não esconda que foi pós-merge. Isso mostra maturidade do processo, não fracasso.

6. Valide
git diff --check

grep -R -n \
  -E "JWT_SECRET_KEY|JWT_ALGORITHM|JWT_EXPIRES_MINUTES|CORS_ORIGINS|env_file" \
  docs/deploy

git status
git diff
Depois:

git add \
  docs/deploy/implementation_plan_issue_081_demo_environment_checklist.md \
  docs/deploy/checklist_demo_environment.md \
  docs/deploy/walkthrough_issue_081_demo_environment_checklist.md

git diff --cached --check
git diff --cached
7. Commit
git commit -m "fix(docs): clarify demo container environment injection"
Depois publique:

git push -u origin fix/issue-081-document-compose-env-injection
8. Novo Pull Request
Título:

fix(docs): clarify demo API environment injection
Descrição:

## Objetivo

Corrigir a documentação do ambiente demo após identificar que a criação de
`backend/.env` não injeta automaticamente todas as variáveis no container
`api`.

## Correção

- documenta a necessidade de `env_file` ou `environment`;
- lista as variáveis JWT e CORS que precisam chegar ao container;
- inclui exemplo genérico de override para demo;
- reforça que arquivos de ambiente não devem ser versionados;
- mantém o Compose atual classificado como infraestrutura de desenvolvimento.

## Escopo

Esta correção é exclusivamente documental.

Nenhum Docker Compose, backend, frontend ou ambiente externo foi alterado.

Closes #<NÚMERO_DA_NOVA_ISSUE>
Também responda ao comentário do Codex informando que o apontamento foi corrigido em um PR complementar. O erro relevante agora não é ter feito o merge. Seria conhecer o problema e deixar a documentação errada na main, essa tradição corporativa bastante mais difícil de defender.


P1 Badge Remove env_file-only override guidance

When this snippet is used as the “override” recommended below, it does not replace the API values already declared in docker-compose.yml:5-9: Docker documents that merged Compose mappings keep existing keys and that environment has higher precedence than env_file (merge rules, precedence rules). As a result, SECRET_KEY: ${SECRET_KEY:-dev-secret-change-me} and the default DATABASE_URL from the root Compose file still win unless the operator also sets root .env/shell variables or resets/redeclares those keys, leaving a demo that follows the checklist with the dev secret/default DB URL despite backend/.env.demo.

O Codex está certo de novo. A orientação anterior com um override contendo apenas env_file é insuficiente quando o Compose base já declara as mesmas chaves em environment.

No Compose, valores definidos em environment têm precedência sobre env_file. Além disso, na mesclagem de arquivos Compose, os mapas são combinados, então as chaves existentes no environment do arquivo base continuam presentes. Resultado: SECRET_KEY e DATABASE_URL do Compose raiz continuariam vencendo os valores de backend/.env.demo.

O risco concreto
Se o arquivo base contém:

services:
  api:
    environment:
      SECRET_KEY: ${SECRET_KEY:-dev-secret-change-me}
      DATABASE_URL: ${DATABASE_URL:-postgresql+psycopg://postgres:postgres@db:5432/gth_agents}
e o override contém apenas:

services:
  api:
    env_file:
      - ./backend/.env.demo
o container ainda receberá os valores vindos de environment, porque eles têm precedência maior.

Portanto, esta orientação deve ser removida:

services:
  api:
    env_file:
      - ./backend/.env.demo
como solução isolada.

Correção recomendada
Há duas formas válidas para uma futura demo.

Opção A: usar --env-file para interpolar o Compose base
Essa é a solução documental mais simples, desde que o Compose base já declare explicitamente todas as variáveis necessárias:

docker compose \
  --env-file backend/.env.demo \
  config
E depois:

docker compose \
  --env-file backend/.env.demo \
  up -d
O arquivo backend/.env.demo precisa conter, no mínimo:

FLASK_ENV=production
SECRET_KEY=<valor-forte>
DATABASE_URL=<url-do-banco-demo>
JWT_SECRET_KEY=<valor-forte>
JWT_ALGORITHM=HS256
JWT_EXPIRES_MINUTES=60
CORS_ORIGINS=https://demo.exemplo.com
Mas há um detalhe inconveniente, porque Docker Compose nunca perde a oportunidade de criar uma segunda camada de entendimento: isso só funciona para as variáveis que o Compose base realmente referencia no bloco environment.

Se o Compose atual não contém:

JWT_SECRET_KEY: ${JWT_SECRET_KEY}
JWT_ALGORITHM: ${JWT_ALGORITHM}
JWT_EXPIRES_MINUTES: ${JWT_EXPIRES_MINUTES}
CORS_ORIGINS: ${CORS_ORIGINS}
então usar --env-file não as injeta automaticamente no container. O --env-file fornece valores para interpolação do Compose; ele não adiciona sozinho novas chaves ao ambiente do serviço.

Opção B: override redeclarando explicitamente o environment
Para manter a ideia de override, o arquivo precisa redeclarar as chaves:

services:
  api:
    env_file:
      - ./backend/.env.demo
    environment:
      FLASK_APP: ${FLASK_APP:-app:create_app}
      FLASK_ENV: ${FLASK_ENV:-production}
      SECRET_KEY: ${SECRET_KEY:?SECRET_KEY obrigatória}
      DATABASE_URL: ${DATABASE_URL:?DATABASE_URL obrigatória}
      JWT_SECRET_KEY: ${JWT_SECRET_KEY:?JWT_SECRET_KEY obrigatória}
      JWT_ALGORITHM: ${JWT_ALGORITHM:-HS256}
      JWT_EXPIRES_MINUTES: ${JWT_EXPIRES_MINUTES:-60}
      CORS_ORIGINS: ${CORS_ORIGINS:?CORS_ORIGINS obrigatória}
Execução:

docker compose \
  --env-file backend/.env.demo \
  -f docker-compose.yml \
  -f docker-compose.demo.yml \
  config
Depois:

docker compose \
  --env-file backend/.env.demo \
  -f docker-compose.yml \
  -f docker-compose.demo.yml \
  up -d
Aqui o env_file disponibiliza variáveis ao container, enquanto o bloco environment também redefine explicitamente as chaves herdadas do Compose base. Como environment vence env_file, ambos devem apontar para os valores corretos.

Melhor decisão para a Issue #081
Como a issue é documental e não cria realmente docker-compose.demo.yml, o checklist não deve apresentar um override simplificado como solução pronta.

Ele deve afirmar:

Um override que apenas adicione `env_file` não é suficiente quando o
Compose base já define as mesmas variáveis no bloco `environment`.

Antes da demo, a composição específica deve:

1. redeclarar explicitamente todas as variáveis herdadas que precisam mudar;
2. adicionar as variáveis ausentes ao ambiente do serviço `api`;
3. utilizar valores fornecidos pelo shell ou por `--env-file`;
4. usar a sintaxe `${VAR:?mensagem}` para impedir fallback inseguro;
5. ser validada pela configuração final resolvida.
Trecho correto para o checklist
### Configuração do container da API

O `docker-compose.yml` de desenvolvimento já declara algumas variáveis no
bloco `environment` do serviço `api`.

Em uma composição formada por arquivo base e override, essas chaves são
mescladas e permanecem presentes. Além disso, valores declarados em
`environment` têm precedência sobre valores recebidos por `env_file`.

Portanto, um override que somente acrescente:

```yaml
env_file:
  - ./backend/.env.demo
não garante a substituição de SECRET_KEY, DATABASE_URL ou de outras
variáveis já declaradas no arquivo base.

A futura composição demo deverá redeclarar explicitamente todas as
configurações necessárias, sem fallback de desenvolvimento:

services:
  api:
    environment:
      FLASK_ENV: production
      SECRET_KEY: ${SECRET_KEY:?SECRET_KEY obrigatória}
      DATABASE_URL: ${DATABASE_URL:?DATABASE_URL obrigatória}
      JWT_SECRET_KEY: ${JWT_SECRET_KEY:?JWT_SECRET_KEY obrigatória}
      JWT_ALGORITHM: ${JWT_ALGORITHM:-HS256}
      JWT_EXPIRES_MINUTES: ${JWT_EXPIRES_MINUTES:-60}
      CORS_ORIGINS: ${CORS_ORIGINS:?CORS_ORIGINS obrigatória}
Os valores poderão ser fornecidos por arquivo não versionado usando:

docker compose \
  --env-file backend/.env.demo \
  -f docker-compose.yml \
  -f docker-compose.demo.yml \
  config
O arquivo backend/.env.demo não deve ser versionado.


## Validação obrigatória

Não basta rodar apenas:

```bash
docker compose config
Use os mesmos arquivos e o mesmo arquivo de ambiente previstos para a demo:

docker compose \
  --env-file backend/.env.demo \
  -f docker-compose.yml \
  -f docker-compose.demo.yml \
  config
Depois confirme apenas a presença das chaves, sem publicar os valores:

docker compose \
  --env-file backend/.env.demo \
  -f docker-compose.yml \
  -f docker-compose.demo.yml \
  config |
grep -E "JWT_SECRET_KEY|JWT_ALGORITHM|JWT_EXPIRES_MINUTES|CORS_ORIGINS|SECRET_KEY|DATABASE_URL"
Evite colar a saída completa no walkthrough, porque docker compose config pode mostrar os segredos resolvidos. Humanos adoram proteger o .env e depois publicar seu conteúdo dentro do log do PR, uma eficiência curiosa.

Resposta ao Codex
Concordo. Um override contendo apenas env_file não substitui as chaves já declaradas em environment no Compose base.

Como environment possui precedência sobre env_file e os mapas são mesclados, os valores padrão de SECRET_KEY e DATABASE_URL continuariam ativos.

Vou corrigir a documentação para remover a orientação de env_file isolado e exigir que a futura composição demo:

redeclare explicitamente as variáveis herdadas;

adicione as variáveis JWT e CORS ausentes;

utilize valores fornecidos por --env-file ou pelo ambiente do operador;

use ${VAR:?mensagem} para impedir fallback de desenvolvimento;

seja validada com a configuração completa e os mesmos arquivos utilizados na futura execução.

A correção continuará exclusivamente documental.

Veredito
Comentário Codex: PROCEDENTE
Prioridade P1: JUSTIFICADA
Orientação env_file isolado: INCORRETA
PR complementar atual: PRECISA DE CORREÇÃO
Solução: redeclarar environment ou criar Compose demo completo
Não faça merge desse PR complementar enquanto o exemplo de env_file isolado continuar presente.



Markdown(3).md colado
Arquivo
Corrija o arquivo do checklist:

Corrigi o checklist. O trecho com env_file isolado foi removido e substituído por uma orientação tecnicamente correta sobre precedência e mesclagem do Docker Compose.


Principais ajustes:

exige composição específica para demo;

redeclara explicitamente SECRET_KEY, DATABASE_URL, JWT e CORS;

usa ${VAR:?mensagem} para impedir fallback inseguro;

valida com os mesmos --env-file e arquivos -f usados no up -d;

alerta para não publicar a saída completa de docker compose config;

adiciona verificações pré e pós-deploy;

registra o risco de precedência do Compose;

remove a recomendação de alterar hashes diretamente por SQL;

corrige pequenos problemas de redação.

checklist_demo_environment_corrigido.md



Biblioteca
/
Multiagentes Gestao de Pessoas
/
checklist_demo_environment_corrigido.md


# Checklist de Preparação de Ambiente Demo

Este documento apresenta um guia técnico, seguro e reproduzível para a preparação planejada e a validação operacional de um ambiente de demonstração controlado para o **GTH Agents**.

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

A criação de `backend/.env.demo` não disponibiliza automaticamente suas
variáveis ao container `api`.

O `docker-compose.yml` de desenvolvimento já declara algumas configurações
no bloco `environment`. Quando um arquivo Compose base é combinado com um
override, os mapas são mesclados e as chaves existentes permanecem ativas.
Além disso, valores definidos em `environment` têm precedência sobre valores
recebidos por `env_file`.

Portanto, um override que apenas acrescente:

```yaml
env_file:
  - ./backend/.env.demo
```

**não é suficiente** para substituir valores já declarados no Compose base,
como `SECRET_KEY` e `DATABASE_URL`.

A futura composição específica para demo deverá redeclarar explicitamente
todas as configurações necessárias ao serviço `api`, sem fallbacks de
desenvolvimento:

```yaml
services:
  api:
    environment:
      FLASK_APP: ${FLASK_APP:-app:create_app}
      FLASK_ENV: production
      SECRET_KEY: ${SECRET_KEY:?SECRET_KEY obrigatória}
      DATABASE_URL: ${DATABASE_URL:?DATABASE_URL obrigatória}
      JWT_SECRET_KEY: ${JWT_SECRET_KEY:?JWT_SECRET_KEY obrigatória}
      JWT_ALGORITHM: ${JWT_ALGORITHM:-HS256}
      JWT_EXPIRES_MINUTES: ${JWT_EXPIRES_MINUTES:-60}
      CORS_ORIGINS: ${CORS_ORIGINS:?CORS_ORIGINS obrigatória}
```

Os valores deverão ser fornecidos pelo ambiente do operador ou por arquivo
não versionado, por exemplo:

```bash
docker compose \
  --env-file backend/.env.demo \
  -f docker-compose.yml \
  -f docker-compose.demo.yml \
  config
```

A mesma combinação de arquivos e de `--env-file` utilizada na validação
deverá ser usada ao iniciar a pilha:

```bash
docker compose \
  --env-file backend/.env.demo \
  -f docker-compose.yml \
  -f docker-compose.demo.yml \
  up -d
```

> [!IMPORTANT]
> O arquivo `backend/.env.demo` não deve ser versionado.

> [!WARNING]
> O `docker-compose.yml` atual deve ser tratado exclusivamente como
> infraestrutura de desenvolvimento. Ele não é adequado para uma demo segura
> sem uma composição adicional que redeclare as variáveis herdadas e injete
> as configurações JWT e CORS ausentes.

> [!WARNING]
> Nunca compartilhe ou versione arquivos `.env` preenchidos com credenciais reais. Utilize sempre este checklist como referência de placeholders genéricos.

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
   - Criar o usuário administrador inicial por um fluxo suportado pela aplicação ou por uma ferramenta administrativa dedicada.
   - Não manipular hashes de senha diretamente por SQL como procedimento operacional padrão.
   - Executar `seed_db.py` somente em uma base explicitamente descartável, com confirmação de recriação total e alteração posterior das credenciais por um fluxo suportado pela aplicação.

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

- **Validar a configuração final da composição demo**:
  ```bash
  docker compose \
    --env-file backend/.env.demo \
    -f docker-compose.yml \
    -f docker-compose.demo.yml \
    config
  ```
  Utilize exatamente os mesmos arquivos e o mesmo `--env-file` previstos para
  a execução. Não copie a saída completa para documentação ou logs públicos,
  pois os valores resolvidos podem conter segredos.
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
- [ ] Existe uma composição específica para demo que redeclara explicitamente `SECRET_KEY`, `DATABASE_URL`, `JWT_SECRET_KEY`, `JWT_ALGORITHM`, `JWT_EXPIRES_MINUTES` e `CORS_ORIGINS` no serviço `api`.
- [ ] A composição final foi validada com os mesmos parâmetros `--env-file` e `-f` que serão utilizados no `up -d`, sem fallbacks de desenvolvimento.
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
- [ ] **Configuração efetiva da API**: O container `api` iniciou sem fallbacks de desenvolvimento para JWT, CORS, `SECRET_KEY` ou `DATABASE_URL`. A verificação foi feita sem imprimir os valores dos segredos.
- [ ] **Logs seguros**: Logs do container não exibem a string do token JWT ou hashes de senha das requisições interceptadas.
- [ ] **Backup inicial**: Executado dump de segurança inicial pós-provisionamento.

---

## 18. Procedimento básico de rollback

Em caso de falha crítica durante ou após o deploy do ambiente demo, execute o seguinte procedimento estruturado de rollback:
1. Pare e remova os containers ativos, mantendo os volumes persistentes:
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
- **Risco de Precedência do Compose**: Um override que apenas adicione `env_file` não substitui chaves já declaradas em `environment` no Compose base. A composição demo deve redeclarar explicitamente essas variáveis.
- **Limitação de Performance**: A configuração padrão Docker do banco e da API não é otimizada para concorrência pesada de acessos ou grandes volumes de dados de stress test.

---

## 20. Itens explicitamente fora do escopo

As seguintes tarefas **permanecem fora do escopo** da Issue #081 e não devem ser executadas pelo operador:
- Provisionamento automatizado de servidores em nuvem (AWS, GCP, Azure, Heroku, etc.).
- Registro ou compra de domínios públicos reais ou DNS externos.
- Geração ou instalação de certificados SSL/TLS públicos emitidos por CA oficial em domínios reais (com exceção de simulações com Certbot local/Self-signed).
- Criação e configuração de pipelines automatizadas de CI/CD (GitHub Actions, GitLab CI, Jenkins) para build e deploy automático.
- Alteração ou reescrita dos scripts de seed (`seed_db.py`) ou arquivos de infraestrutura da aplicação.
Biblioteca
/
Multiagentes Gestao de Pessoas
/
checklist_demo_environment_corrigido.md


# Checklist de Preparação de Ambiente Demo

Este documento apresenta um guia técnico, seguro e reproduzível para a preparação planejada e a validação operacional de um ambiente de demonstração controlado para o **GTH Agents**.

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

A criação de `backend/.env.demo` não disponibiliza automaticamente suas
variáveis ao container `api`.

O `docker-compose.yml` de desenvolvimento já declara algumas configurações
no bloco `environment`. Quando um arquivo Compose base é combinado com um
override, os mapas são mesclados e as chaves existentes permanecem ativas.
Além disso, valores definidos em `environment` têm precedência sobre valores
recebidos por `env_file`.

Portanto, um override que apenas acrescente:

```yaml
env_file:
  - ./backend/.env.demo
```

**não é suficiente** para substituir valores já declarados no Compose base,
como `SECRET_KEY` e `DATABASE_URL`.

A futura composição específica para demo deverá redeclarar explicitamente
todas as configurações necessárias ao serviço `api`, sem fallbacks de
desenvolvimento:

```yaml
services:
  api:
    environment:
      FLASK_APP: ${FLASK_APP:-app:create_app}
      FLASK_ENV: production
      SECRET_KEY: ${SECRET_KEY:?SECRET_KEY obrigatória}
      DATABASE_URL: ${DATABASE_URL:?DATABASE_URL obrigatória}
      JWT_SECRET_KEY: ${JWT_SECRET_KEY:?JWT_SECRET_KEY obrigatória}
      JWT_ALGORITHM: ${JWT_ALGORITHM:-HS256}
      JWT_EXPIRES_MINUTES: ${JWT_EXPIRES_MINUTES:-60}
      CORS_ORIGINS: ${CORS_ORIGINS:?CORS_ORIGINS obrigatória}
```

Os valores deverão ser fornecidos pelo ambiente do operador ou por arquivo
não versionado, por exemplo:

```bash
docker compose \
  --env-file backend/.env.demo \
  -f docker-compose.yml \
  -f docker-compose.demo.yml \
  config
```

A mesma combinação de arquivos e de `--env-file` utilizada na validação
deverá ser usada ao iniciar a pilha:

```bash
docker compose \
  --env-file backend/.env.demo \
  -f docker-compose.yml \
  -f docker-compose.demo.yml \
  up -d
```

> [!IMPORTANT]
> O arquivo `backend/.env.demo` não deve ser versionado.

> [!WARNING]
> O `docker-compose.yml` atual deve ser tratado exclusivamente como
> infraestrutura de desenvolvimento. Ele não é adequado para uma demo segura
> sem uma composição adicional que redeclare as variáveis herdadas e injete
> as configurações JWT e CORS ausentes.

> [!WARNING]
> Nunca compartilhe ou versione arquivos `.env` preenchidos com credenciais reais. Utilize sempre este checklist como referência de placeholders genéricos.

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
   - Criar o usuário administrador inicial por um fluxo suportado pela aplicação ou por uma ferramenta administrativa dedicada.
   - Não manipular hashes de senha diretamente por SQL como procedimento operacional padrão.
   - Executar `seed_db.py` somente em uma base explicitamente descartável, com confirmação de recriação total e alteração posterior das credenciais por um fluxo suportado pela aplicação.

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

- **Validar a configuração final da composição demo**:
  ```bash
  docker compose \
    --env-file backend/.env.demo \
    -f docker-compose.yml \
    -f docker-compose.demo.yml \
    config
  ```
  Utilize exatamente os mesmos arquivos e o mesmo `--env-file` previstos para
  a execução. Não copie a saída completa para documentação ou logs públicos,
  pois os valores resolvidos podem conter segredos.
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
- [ ] Existe uma composição específica para demo que redeclara explicitamente `SECRET_KEY`, `DATABASE_URL`, `JWT_SECRET_KEY`, `JWT_ALGORITHM`, `JWT_EXPIRES_MINUTES` e `CORS_ORIGINS` no serviço `api`.
- [ ] A composição final foi validada com os mesmos parâmetros `--env-file` e `-f` que serão utilizados no `up -d`, sem fallbacks de desenvolvimento.
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
- [ ] **Configuração efetiva da API**: O container `api` iniciou sem fallbacks de desenvolvimento para JWT, CORS, `SECRET_KEY` ou `DATABASE_URL`. A verificação foi feita sem imprimir os valores dos segredos.
- [ ] **Logs seguros**: Logs do container não exibem a string do token JWT ou hashes de senha das requisições interceptadas.
- [ ] **Backup inicial**: Executado dump de segurança inicial pós-provisionamento.

---

## 18. Procedimento básico de rollback

Em caso de falha crítica durante ou após o deploy do ambiente demo, execute o seguinte procedimento estruturado de rollback:
1. Pare e remova os containers ativos, mantendo os volumes persistentes:
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
- **Risco de Precedência do Compose**: Um override que apenas adicione `env_file` não substitui chaves já declaradas em `environment` no Compose base. A composição demo deve redeclarar explicitamente essas variáveis.
- **Limitação de Performance**: A configuração padrão Docker do banco e da API não é otimizada para concorrência pesada de acessos ou grandes volumes de dados de stress test.

---

## 20. Itens explicitamente fora do escopo

As seguintes tarefas **permanecem fora do escopo** da Issue #081 e não devem ser executadas pelo operador:
- Provisionamento automatizado de servidores em nuvem (AWS, GCP, Azure, Heroku, etc.).
- Registro ou compra de domínios públicos reais ou DNS externos.
- Geração ou instalação de certificados SSL/TLS públicos emitidos por CA oficial em domínios reais (com exceção de simulações com Certbot local/Self-signed).
- Criação e configuração de pipelines automatizadas de CI/CD (GitHub Actions, GitLab CI, Jenkins) para build e deploy automático.
- Alteração ou reescrita dos scripts de seed (`seed_db.py`) ou arquivos de infraestrutura da aplicação.
