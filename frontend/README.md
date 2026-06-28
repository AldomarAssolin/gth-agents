# GTH Agents - Frontend MVP

Interface web interativa de controle e acompanhamento de talentos (Gestão de Talentos Humanos) desenvolvida para o monorepo **GTH Agents**.

---

## Stack Utilizada

* **Core**: React 18 / Vite 8
* **Styling**: TailwindCSS 3 (Vanilla CSS + PostCSS para componentes personalizados)
* **Roteamento**: React Router v6
* **Comunicação**: Axios para chamadas REST API
* **Segurança**: Autenticação JWT (armazenamento persistido em LocalStorage com gerenciamento de estado via contexto React)
* **Build/Bundler**: Vite + Rolldown

---

## Pré-requisitos

* **Node.js**: v24+ (e gerenciador de pacotes npm)
* **Docker** e **Docker Compose** (opcional, para execução isolada e em container)

---

## Como Rodar Localmente

### 1. Instalar as dependências
Navegue até a pasta `frontend` e instale os pacotes necessários:
```bash
npm install
```

### 2. Configurar variáveis de ambiente
Crie um arquivo `.env` baseado no modelo de exemplo:
```bash
cp .env.example .env
```

### 3. Executar em modo desenvolvimento
Inicie o servidor de desenvolvimento Vite local:
```bash
npm run dev
```
O frontend estará acessível em: [http://localhost:5173](http://localhost:5173)

---

## Como Rodar com Docker (Desenvolvimento Integrado)

O desenvolvimento integrado do monorepo utiliza o `docker-compose.yml` localizado na raiz do projeto. Para subir o frontend integrado com a API Flask e o banco de dados PostgreSQL:

```bash
docker compose up --build
```
Após o processo de inicialização, os serviços estarão disponíveis em:
* **Frontend Dev**: http://localhost:5173
* **Backend API**: http://localhost:5000

---

## Geração do Build de Produção

Para testar o empacotador e validar a integridade estática dos bundles de produção localmente:

```bash
npm run build
```
O build estático compilado e otimizado será gerado na pasta `dist/`.

---

## Testar Imagem Docker de Produção (Standalone)

O frontend MVP possui suporte de produção via imagem Nginx standalone configurada para servir os arquivos estáticos e tratar fallbacks de roteamento SPA.

### 1. Construir a imagem Docker de produção
No diretório `frontend`, execute:
```bash
docker build -f Dockerfile.prod -t gth-agents-web:prod .
```

### 2. Rodar o container standalone
Execute o container mapeando a porta local 8080:
```bash
docker run --rm -p 8080:80 gth-agents-web:prod
```

### 3. Acessar a aplicação em produção
Abra no navegador: [http://localhost:8080](http://localhost:8080)

---

## Variáveis de Ambiente

As configurações dinâmicas do frontend são expostas ao Vite através das variáveis de ambiente prefixadas com `VITE_`.

O arquivo `frontend/.env.example` documenta as variáveis necessárias:
```env
VITE_API_URL=http://localhost:5000
```
* **VITE_API_URL**: URL base da API Flask para as requisições HTTP do Axios.

---

## Integração com o Backend

A interface consome os seguintes endpoints do backend Flask (todas as requisições privadas exigem o cabeçalho `Authorization: Bearer <token_jwt>`):

* `POST /login` - Autenticação de usuários.
* `GET /dashboard/mvp` - Métricas consolidadas de talentos, metas e alertas.
* `GET /colaboradores` - Listagem completa de colaboradores.
* `GET /colaboradores/<id>` - Detalhes específicos de um colaborador.
* `GET /colaboradores/<id>/evolucao` - Histórico integrado de feedbacks, reconhecimentos, metas e PDIs.
* `POST /avaliacoes` - Registro de nova avaliação de colaborador.
* `POST /metas` - Criação de novas metas.
* `POST /pdis` - Criação de novos Planos de Desenvolvimento Individual.
* `POST /pdis/<pdi_id>/acoes` - Adicionar ação de desenvolvimento ao PDI.
* `POST /feedbacks` - Envio de novos feedbacks.
* `POST /reconhecimentos` - Envio de novos reconhecimentos.

---

## Estrutura de Pastas

```text
frontend/
├── src/
│   ├── assets/       # Imagens e estilos estáticos globais
│   ├── components/   # Componentes reutilizáveis compartilhados (ex: Ui/Loading, Button, Input)
│   ├── features/     # Módulos encapsulados de lógica por domínio (ex: auth, colaboradores, pdis)
│   │   ├── auth/
│   │   ├── colaboradores/
│   │   └── pdis/
│   ├── layouts/      # Layouts estruturais de página (ex: Sidebar, Topbar, MainLayout)
│   ├── pages/        # Componentes de visualização principal associados às rotas
│   ├── routes/       # Definição e proteção de rotas da aplicação
│   ├── services/     # Clientes de comunicação Axios com a API backend
│   └── utils/        # Funções utilitárias auxiliares de conversão e formatação
├── Dockerfile.dev    # Dockerfile otimizado para o fluxo de desenvolvimento
├── Dockerfile.prod   # Dockerfile multi-stage com Nginx para build de produção
├── nginx.conf        # Configuração do Nginx com fallback de rotas React Router
└── vite.config.js    # Configuração do compilador/empacotador Vite
```

---

## Observações sobre Autenticação JWT

1. **Persistência**: O token recebido no login é salvo no `localStorage` sob a chave `token`.
2. **Contexto**: O hook personalizado `useAuth` fornece o estado global de autenticação (`user`, `login`, `logout`).
3. **Interceptador**: O cliente Axios (`services/api.js`) intercepta automaticamente cada requisição de saída para adicionar o token JWT ao cabeçalho `Authorization`.
4. **Tratamento de 401**: Respostas HTTP de erro 401 limpam automaticamente os cookies/localStorage e forçam o redirecionamento ao login.

---

## Observações sobre React Router e Nginx

Em uma aplicação do tipo SPA (Single Page Application), o roteamento é feito no lado do cliente. Se um usuário atualiza a página em uma rota profunda (como `/colaboradores/1/evolucao`), o servidor da web comum tentará encontrar o arquivo físico e retornará erro `404 Not Found`.

Para resolver isso em produção, a configuração `frontend/nginx.conf` inclui a diretiva `try_files`:
```nginx
location / {
    root /usr/share/nginx/html;
    index index.html index.htm;
    try_files $uri $uri/ /index.html;
}
```
Isso redireciona todas as requisições que não correspondem a um arquivo estático físico de volta para o `index.html`, delegando a resolução da rota ao `React Router` do lado do cliente.
