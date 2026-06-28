# GTH Agents - Frontend Web

Interface web responsiva desenvolvida em React para o painel de gestão e acompanhamento de talentos do monorepo **GTH Agents**.

A aplicação permite que líderes, profissionais de RH, administradores e colaboradores acompanhem informações relacionadas a competências, avaliações, metas, PDIs, feedbacks, reconhecimentos e evolução do colaborador de forma centralizada.

O frontend consome a API REST do backend Flask, utiliza autenticação via JWT e organiza suas funcionalidades em módulos de negócio.

---

## Stack de Tecnologias

* **Biblioteca Core**: React
* **Ferramental de Build**: Vite
* **Roteamento**: React Router / React Router DOM
* **Estilização**: Tailwind CSS
* **Cliente HTTP**: Axios
* **Controle de Sessão**: JWT persistido em `localStorage`
* **Ambiente de Desenvolvimento**: Docker e Docker Compose

> As versões exatas das dependências devem ser conferidas no arquivo `package.json`.

---

## Estrutura de Pastas e Componentes

A aplicação utiliza uma estrutura organizada por **features**, separando módulos de negócio, páginas, componentes reutilizáveis e serviços de integração com a API.

```python
frontend/
├── src/
│   ├── assets/       # Recursos estáticos e estilos globais
│   ├── components/   # Componentes compartilhados sem regra de negócio
│   │   ├── layout/   # Sidebar, Topbar, PageHeader e elementos estruturais
│   │   └── ui/       # Button, Card, Badge, Input, Table, EmptyState, Loading etc.
│   ├── features/     # Módulos de negócio com services, componentes e formulários
│   │   ├── auth/            # Autenticação, sessão e rotas protegidas
│   │   ├── colaboradores/   # Listagem, cadastro, detalhe e dados do colaborador
│   │   ├── avaliacoes/      # Registro de avaliações e exibição de resultados
│   │   ├── metas/           # Criação, listagem e acompanhamento de metas
│   │   ├── pdis/            # Planos de desenvolvimento e ações de PDI
│   │   ├── feedbacks/       # Registro e consulta de feedbacks
│   │   ├── reconhecimentos/ # Mural interno e registro de reconhecimentos
│   │   ├── dashboard/       # Indicadores consolidados do MVP
│   │   ├── evolucao/        # Evolução consolidada do colaborador
│   │   └── configuracoes/   # Cadastros auxiliares administrativos
│   ├── layouts/      # AppLayout e AuthLayout
│   ├── pages/        # Telas completas mapeadas nas rotas
│   ├── routes/       # Definição das rotas públicas e privadas
│   ├── services/     # Instância central do Axios e configuração da API
│   └── utils/        # Funções auxiliares e formatadores
```

---

## Organização por Features

Cada módulo de negócio concentra seus próprios componentes, serviços, formatadores e tratamento de erros quando necessário.

Exemplos:

```text
features/
├── auth/
├── dashboard/
├── colaboradores/
├── avaliacoes/
├── metas/
├── pdis/
├── feedbacks/
├── reconhecimentos/
├── evolucao/
└── configuracoes/
```

Essa organização evita que a aplicação concentre lógica de diferentes módulos em páginas gigantes ou arquivos genéricos demais. O frontend agradece. O próximo humano que fizer manutenção também.

---

## Integração com a API Backend

A comunicação com o backend é centralizada em:

```text
src/services/api.js
```

Essa instância do Axios é responsável por:

* definir a URL base da API;
* enviar o token JWT nas requisições autenticadas;
* tratar respostas de erro globais, como `401 Unauthorized`;
* manter um ponto único de configuração para chamadas HTTP.

A URL da API é configurada pela variável:

```text
VITE_API_URL
```

Exemplo:

```http
VITE_API_URL=http://localhost:5000
```

---

## Principais Endpoints Consumidos

A aplicação consome endpoints da API Flask conforme os módulos implementados.

### Autenticação

* `POST /auth/login`

### Dashboard

* `GET /dashboard/mvp`

### Colaboradores

* `GET /colaboradores`
* `POST /colaboradores`
* `GET /colaboradores/<int:id>`
* `PUT /colaboradores/<int:id>`
* `GET /colaboradores/<int:id>/evolucao`
* `GET /colaboradores/<int:id>/metas`

### Avaliações

* `POST /avaliacoes`

### Metas

* `POST /metas`
* `GET /metas`, quando disponível no backend
* `GET /colaboradores/<int:id>/metas`

### PDIs

* `POST /pdis`
* `GET /pdis`
* `GET /pdis/<int:pdi_id>`
* `PATCH /pdis/<int:pdi_id>`, quando disponível
* `PATCH /pdis/<int:pdi_id>/concluir`, quando disponível
* `PATCH /pdis/<int:pdi_id>/cancelar`, quando disponível
* `GET /colaboradores/<int:colaborador_id>/pdis`
* `POST /pdis/<int:pdi_id>/acoes`
* `GET /pdis/<int:pdi_id>/acoes`, quando disponível como rota separada
* `PATCH /pdis/<int:pdi_id>/acoes/<int:acao_id>`, quando disponível
* `PATCH /pdis/<int:pdi_id>/acoes/<int:acao_id>/concluir`, quando disponível
* `PATCH /pdis/<int:pdi_id>/acoes/<int:acao_id>/cancelar`, quando disponível

### Feedbacks

* `POST /feedbacks`
* `POST /feedbacks/estruturar`, quando disponível
* `GET /feedbacks`, quando disponível
* `GET /colaboradores/<int:id>/feedbacks`, quando disponível

### Reconhecimentos

* `POST /reconhecimentos`
* `GET /reconhecimentos`
* `GET /reconhecimentos/<int:reconhecimento_id>`
* `GET /colaboradores/<int:colaborador_id>/reconhecimentos`
* `PATCH /reconhecimentos/<int:reconhecimento_id>/cancelar`, quando disponível

### Cadastros Administrativos

* `/setores`
* `/funcoes`
* `/usuarios`
* `/competencias`

> A lista acima deve permanecer alinhada com os contratos reais do backend. Endpoints marcados como "quando disponível" devem ser confirmados nas rotas Flask antes de serem consumidos em novas integrações.

---

## Segurança e Controle de Acesso

A aplicação utiliza autenticação via JWT e mantém a sessão do usuário no navegador.

### AuthContext / useAuth

O contexto de autenticação centraliza os dados da sessão do usuário, como:

```sql
id
nome
email
perfil
colaborador_id
setor_id
```

Perfis técnicos utilizados:

```text
ADMIN
RH
LIDER
COLABORADOR
```

### PrivateRoute

As rotas internas da aplicação são protegidas por componentes de rota privada.

Comportamento esperado:

* usuário autenticado acessa as páginas internas;
* usuário não autenticado é redirecionado para `/login`;
* rotas administrativas podem aplicar bloqueio visual por perfil;
* o backend continua sendo a autoridade final de autorização.

### Axios Interceptor

A instância global do Axios adiciona automaticamente o cabeçalho de autorização quando existe token salvo:

```http
Authorization: Bearer <token>
```

Também trata respostas `401 Unauthorized`, normalmente relacionadas a token ausente, inválido ou expirado.

Respostas `403 Forbidden` devem ser tratadas como falta de permissão, sem encerrar obrigatoriamente a sessão do usuário.

---

## Rotas Principais

Rotas principais da aplicação:

```text
/login
/dashboard
/colaboradores
/colaboradores/novo
/colaboradores/:id
/colaboradores/:id/evolucao
/avaliacoes
/avaliacoes/nova
/metas
/metas/nova
/pdis
/pdis/novo
/pdis/:id
/colaboradores/:id/pdis
/feedbacks
/feedbacks/novo
/reconhecimentos
/reconhecimentos/novo
/configuracoes
```

A disponibilidade visual de algumas rotas pode variar conforme o perfil do usuário autenticado.

---

## Padrões de Tela

As telas do frontend seguem padrões reutilizáveis para:

* carregamento (`Loading`);
* erro (`ErrorMessage`);
* estado vazio (`EmptyState`);
* cartões (`Card`);
* tabelas (`Table`);
* badges de status;
* formulários com validação básica;
* mensagens amigáveis para falhas de conexão, dados ausentes e acesso negado.

Sempre que possível, os módulos devem reutilizar componentes existentes em `src/components/ui/` e `src/components/layout/`.

---

## Tratamento de Erros

O frontend trata erros em camadas:

* **Erro de autenticação (`401`)**: tratado globalmente pela instância do Axios.
* **Erro de permissão (`403`)**: exibido como acesso negado ou mensagem específica da página.
* **Erro de recurso inexistente (`404`)**: exibido como mensagem amigável, preservando o layout.
* **Erro de validação (`400`)**: exibido próximo ao formulário ou ao campo relacionado, quando possível.
* **Erro de conexão**: exibido sem desmontar telas já carregadas, sempre que o estado da página permitir.

Em formulários, erros de submissão devem preservar os dados já preenchidos para permitir correção e nova tentativa.

---

## Execução e Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` a partir do modelo base na pasta `frontend/`:

```bash
cp .env.example .env
```

Variável principal:

```text
VITE_API_URL=http://localhost:5000
```

Nunca versionar `.env` com dados sensíveis ou configurações locais reais.

---

## Execução Local

A partir da pasta `frontend/`:

```bash
npm install
npm run dev
```

A aplicação ficará disponível em:

```text
http://localhost:5173
```

---

## Execução com Docker

A partir da raiz do monorepo:

```bash
docker compose up --build -d
```

O frontend ficará disponível em:

```text
http://localhost:5173
```

Para acompanhar logs:

```bash
docker compose logs -f web
```

Para encerrar o ambiente:

```bash
docker compose down
```

---

## Build de Produção

A partir da pasta `frontend/`:

```bash
npm run build
```

Os arquivos otimizados serão gerados em:

```text
dist/
```

---

## Build de Produção com Docker

Caso o projeto possua `Dockerfile.prod` e `nginx.conf`, a imagem de produção pode ser testada localmente com:

```bash
docker build -f Dockerfile.prod -t gth-agents-web:prod .
docker run --rm -p 8080:80 gth-agents-web:prod
```

A aplicação ficará disponível em:

```text
http://localhost:8080
```

---

## Suporte SPA no Nginx

Como o frontend é uma Single Page Application, o roteamento interno é resolvido pelo React Router no navegador.

Em builds servidos por Nginx, rotas profundas como:

```text
/colaboradores/1/evolucao
```

precisam retornar `index.html` para que o React Router resolva a tela correta.

Exemplo de configuração:

```nginx
location / {
    try_files $uri $uri/ /index.html;
}
```

Essa configuração deve existir em `nginx.conf` quando a imagem de produção usar Nginx.

---

## Validações Técnicas

Comandos principais:

```bash
npm run lint
npm run build
```

Quando a aplicação estiver integrada via Docker:

```bash
docker compose config
docker compose up --build -d
```

---

## Convenções Técnicas

* Reutilizar a instância global do Axios em `src/services/api.js`.
* Não criar clientes HTTP paralelos sem necessidade.
* Reutilizar componentes comuns de `src/components/ui/`.
* Manter regras de negócio de cada módulo dentro de `features/`.
* Evitar duplicação de services.
* Não consumir endpoints não confirmados no backend.
* Preservar dados de formulário em falhas de submissão.
* Tratar `403` como falta de permissão, não como sessão expirada.
* Tratar `401` pelo fluxo global de autenticação.
* Evitar dados simulados quando a API real estiver disponível.
* Documentar limitações conhecidas nos walkthroughs das issues.

---

## Status Atual

O frontend do GTH Agents encontra-se em fase de consolidação do MVP, com módulos principais de autenticação, dashboard, colaboradores, avaliações, metas, PDI, feedbacks, reconhecimentos, evolução e cadastros auxiliares implementados ou em revisão final.

Próximas evoluções previstas:

* consolidação final da release frontend MVP;
* melhorias de responsividade;
* refinamento de UX;
* módulo de Saúde Organizacional;
* dashboards analíticos;
* People Analytics.
