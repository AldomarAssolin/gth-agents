---
name: gth-frontend-module
description: Implementa e revisa módulos frontend do GTH Agents em React, Vite e JavaScript. Use para páginas, rotas, formulários, services, componentes, autenticação visual, estados de loading/erro/vazio, integração com API e validação do frontend.
---

# GTH Frontend Module

## Objetivo

Construir módulos frontend coerentes com a arquitetura e os padrões já existentes no monorepo.

## Antes de alterar

1. Inspecione `frontend/src/routes`, `frontend/src/pages`, `frontend/src/features`, `frontend/src/components` e `frontend/src/services`.
2. Localize implementações semelhantes, priorizando módulos já concluídos.
3. Confirme como funcionam autenticação, perfil, autorização visual, Axios, tratamento de 401/403 e armazenamento de sessão.
4. Confirme os contratos reais usando a Skill `gth-api-contract-analysis`.

## Padrões

- React + Vite + JavaScript.
- Organização por feature.
- Página como orquestradora, evitando componentes monolíticos.
- Service responsável apenas por comunicação e normalização mínima da API.
- Estado React fora do service.
- Reutilizar a instância Axios global e seus interceptors.
- Reutilizar componentes de UI e layout existentes.
- Reutilizar services compartilhados de colaboradores, competências, setores e funções quando existirem.
- Não criar uma segunda solução de autenticação ou autorização.

## Estados obrigatórios

Quando aplicável, tratar explicitamente:

- carregamento;
- erro de rede;
- erro de validação;
- 401 conforme fluxo global;
- 403 sem encerrar sessão;
- 404;
- lista vazia;
- resposta parcial;
- envio em andamento;
- prevenção de envio duplicado.

## Leitura e concorrência

- Permitir `AbortSignal` nas chamadas de leitura quando a página puder desmontar ou trocar parâmetros.
- Cancelar requisições obsoletas em efeitos.
- Não tratar cancelamento voluntário como erro de usuário.

## Rotas e perfis

- Modificar placeholders existentes em vez de duplicar rotas.
- Proteger visualmente as rotas com o mecanismo já adotado pelo projeto.
- Ocultar ou desabilitar ações não permitidas, mantendo o backend como autoridade final.
- Validar parâmetros de rota e query string antes de usá-los.

## Dados

- Não inventar campos ausentes.
- Não converter indiscriminadamente payload inválido em array vazio.
- Preservar zero, `false` e strings válidas durante normalização.
- Evitar N+1. Quando precisar resolver nomes por IDs, carregue catálogos uma vez ou use dados já disponíveis.

## Validação mínima

Executar, conforme aplicável:

```bash
cd frontend
npm run lint
npm run build
```

Também validar acesso direto, reload, navegação, integração real, permissões e estados vazios quando o ambiente permitir.

## Restrições

- Não criar mocks para esconder endpoint ausente.
- Não alterar backend apenas para facilitar a tela, salvo escopo explícito.
- Não adicionar biblioteca nova quando os componentes atuais forem suficientes.
- Não afirmar responsividade ou integração sem verificação correspondente.
