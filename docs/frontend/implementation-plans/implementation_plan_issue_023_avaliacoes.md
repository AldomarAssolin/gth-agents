# Implementar ISSUE #023 - Módulo de Avaliações (Frontend)

Este plano descreve a implementação do módulo de avaliações de competências no frontend do GTH Agents, permitindo registrar avaliações para colaboradores e exibir o resultado calculado pelo backend.

---

## Contratos Reais do Backend Identificados

Após a inspeção do backend, foram identificados os seguintes detalhes contratuais:

1. **Endpoint de Criação de Avaliação**:
   - **Endpoint**: `POST /avaliacoes`
   - **Permissões**: Restrito às roles `ADMIN`, `RH` e `LIDER` (através do middleware `@roles_required("ADMIN", "RH", "LIDER")`).
   - **Payload Esperado (JSON)**:
     ```json
     {
       "colaborador_id": 1,
       "avaliador_id": 2,
       "tipo": "AVALIACAO_LIDER",
       "observacao_geral": "Colaborador apresenta boa evolução.",
       "itens": [
         {
           "competencia_id": 1,
           "nota": 5,
           "comentario": "Demonstra domínio técnico."
         }
       ]
     }
     ```
   - **Campos Obrigatórios**: `colaborador_id`, `avaliador_id`, `tipo`, `itens` (mínimo 1 item). Cada item em `itens` deve conter `competencia_id` e `nota` (inteiro de 1 a 5).
   - **Nomes Reais dos Tipos de Avaliação** (Enum `TipoAvaliacao`):
     - `AUTOAVALIACAO`
     - `AVALIACAO_LIDER`
     - `AVALIACAO_TECNICA`
     - `AVALIACAO_360`
   - **Estrutura da Resposta de Sucesso (HTTP 201 Created)**:
     ```json
     {
       "avaliacao": {
         "id": 1,
         "colaborador_id": 1,
         "avaliador_id": 2,
         "tipo": "AVALIACAO_LIDER",
         "observacao_geral": "Colaborador apresenta boa evolução.",
         "itens": [
           {
             "id": 1,
             "competencia_id": 1,
             "nota": 5,
             "comentario": "Demonstra domínio técnico."
           }
         ],
         "criado_em": "2026-06-06T19:49:27"
       },
       "perfil_talento": {
         "id": 1,
         "colaborador_id": 1,
         "classificacao": "ALTA_PERFORMANCE",
         "resumo": "...",
         "nivel_tecnico": "...",
         "nivel_comportamental": "...",
         "potencial_lideranca": "...",
         "pontos_fortes": ["..."],
         "pontos_melhoria": ["..."],
         "recomendacoes": ["..."],
         "origem": "AGENTE_IA",
         "criado_em": "..."
       },
       "resultado_competencias": {
         "media_tecnica": 5.0,
         "media_comportamental": 0.0,
         "media_lideranca": 0.0,
         "media_organizacional": 0.0,
         "media_geral": 5.0
       }
     }
     ```

2. **Existência ou Ausência de `GET /avaliacoes`**:
   - **Ausente**: O backend **não** possui um endpoint `GET /avaliacoes` para listagem de avaliações.
   - **Comportamento**: A rota frontend `/avaliacoes` funcionará como página inicial do módulo exibindo uma explicação breve, um aviso claro de que a listagem geral ainda não está disponível no backend (sem dados simulados) e o botão "Nova avaliação" direcionando para `/avaliacoes/nova`.

3. **Listagem de Colaboradores**:
   - **Endpoint**: `GET /colaboradores` (já implementado no frontend como `listarColaboradores` em `colaboradoresService.js`).
   - **Comportamento**: Retorna os colaboradores associados ao escopo do usuário autenticado (Líderes visualizam apenas colaboradores do próprio setor; RH/ADMIN visualizam todos).

4. **Listagem de Competências**:
   - **Endpoint**: `GET /competencias` (através de `cadastros_interface_bp`).
   - **Estrutura de Competência**:
     - `id`: int
     - `nome`: str
     - `tipo`: `TECNICA`, `COMPORTAMENTAL`, `LIDERANCA`, `ORGANIZACIONAL`
     - `descricao`: str | None
     - `peso`: Decimal (ex: "1.00")
     - `ativo`: bool (devemos exibir apenas as com `ativo === true`).

5. **Regras de Autenticação/Autorização**:
   - O usuário autenticado (extraído do JWT no frontend via `useAuth()`) deve ser a fonte da identidade do avaliador. A propriedade `user.id` será enviada como `avaliador_id` no payload. O usuário não poderá selecionar o avaliador no formulário.
   - A rota de criação de avaliação exige roles `ADMIN`, `RH` ou `LIDER`. Se um `COLABORADOR` tentar acessar a criação, exibiremos uma tela de erro de permissão (403) sem deslogar o usuário.

---

## User Review Required

> [!IMPORTANT]
> O backend **não** fornece uma rota `GET /avaliacoes` para listagem geral de avaliações. Como instruído, a rota `/avaliacoes` funcionará apenas como landing page informativa com atalho para a criação, sem dados simulados.

> [!WARNING]
> O usuário `COLABORADOR` não tem permissão no backend para criar avaliações (HTTP 403 / `@roles_required`). Adotaremos o tratamento de permissão no frontend para desabilitar o acesso a `/avaliacoes/nova` para este perfil, tratando adequadamente qualquer erro 403 do backend sem invalidar a sessão.

---

## Open Questions

*Nenhuma questão em aberto encontrada. Todos os contratos do backend foram devidamente mapeados.*

---

## Proposed Changes

### Módulo de Avaliações (Frontend)

Nesta seção, agrupamos e detalhamos as alterações necessárias no frontend.

---

#### [NEW] [avaliacoesService.js](../../../frontend/src/features/avaliacoes/avaliacoesService.js)
Criar o serviço responsável por encapsular as requisições à API para o módulo de avaliações:
- `criarAvaliacao(payload, options)`: envia dados para `POST /avaliacoes`.
- `listarCompetencias(options)`: recupera a lista de competências através de `GET /competencias`.

#### [NEW] [TipoAvaliacaoSelect.jsx](../../../frontend/src/features/avaliacoes/TipoAvaliacaoSelect.jsx)
Componente de seleção para os tipos de avaliação disponíveis no enum `TipoAvaliacao`:
- Exibe rótulos amigáveis ("Autoavaliação", "Avaliação do líder", "Avaliação técnica", "Avaliação 360°").
- Mantém o valor original do enum em maiúsculo (`AUTOAVALIACAO`, `AVALIACAO_LIDER`, `AVALIACAO_TECNICA`, `AVALIACAO_360`).

#### [NEW] [ItemAvaliacaoForm.jsx](../../../frontend/src/features/avaliacoes/ItemAvaliacaoForm.jsx)
Componente para renderização de cada competência individual no formulário:
- Apresenta: nome, tipo da competência, descrição (se houver) e peso (se houver).
- Checkbox "Avaliar esta competência" para incluir/excluir o item da avaliação.
- Seleção de nota (1 a 5) com legendas amigáveis (ex: "3 - Adequado").
- Campo de comentário opcional (habilitado apenas se a competência estiver selecionada).

#### [NEW] [ResultadoAvaliacao.jsx](../../../frontend/src/features/avaliacoes/ResultadoAvaliacao.jsx)
Exibição premium do resultado calculado da avaliação de desempenho:
- Exibe a classificação do perfil de talento formatada de forma amigável (ex: "Alta Performance").
- Apresenta as médias por categoria (Técnica, Comportamental, Liderança, Organizacional) e a média geral.
- Exibe em listas estilizadas os pontos fortes, pontos de melhoria e recomendações.
- Trata campos ausentes utilizando fallbacks elegantes como "Não avaliado" ou "Nenhum item identificado".

#### [NEW] [AvaliacaoForm.jsx](../../../frontend/src/features/avaliacoes/AvaliacaoForm.jsx)
O formulário de preenchimento da avaliação:
- Campos: Colaborador (select), Tipo de Avaliação, Observação Geral e a listagem de competências agrupadas por tipo.
- Realiza validações locais antes do envio (colaborador obrigatório, tipo obrigatório, ao menos 1 competência, notas válidas nos itens selecionados).
- Evita envio duplo desabilitando o botão de submissão e exibindo indicador de progresso.
- Trata e exibe mensagens de erro próximo ao campo correspondente.

#### [NEW] [avaliacaoUtils.js](../../../frontend/src/features/avaliacoes/avaliacaoUtils.js)
Utilitários de formatação e mapeamento de dados do módulo de avaliações.
- `formatClassificacao(classificacao)`: mapeia enums de classificação de talento para strings legíveis.
- `formatTipo(tipo)`: mapeia enums de tipo de avaliação para strings amigáveis.

#### [NEW] [NovaAvaliacaoPage.jsx](../../../frontend/src/pages/NovaAvaliacaoPage.jsx)
Página para registrar uma nova avaliação:
- Carrega a lista de colaboradores e competências em paralelo.
- Inicializa o colaborador selecionado se houver parâmetro `colaborador_id` na URL query.
- Renderiza o formulário `AvaliacaoForm` ou o `ResultadoAvaliacao` após a criação bem-sucedida.

#### [MODIFY] [AvaliacoesPage.jsx](../../../frontend/src/pages/AvaliacoesPage.jsx)
Atualizar a página `/avaliacoes` para cumprir as regras do módulo:
- Apresentar título, descrição e botão "Nova avaliação".
- Exibir estado informativo explicando que a listagem de avaliações não está disponível no backend atualmente, sem utilizar dados simulados.

#### [MODIFY] [AppRoutes.jsx](../../../frontend/src/routes/AppRoutes.jsx)
Adicionar a rota `/avaliacoes/nova` direcionando para `NovaAvaliacaoPage.jsx`.

#### [MODIFY] [ColaboradorDetalhe.jsx](../../../frontend/src/features/colaboradores/ColaboradorDetalhe.jsx)
Modificar o botão de atalho "Registrar Avaliação (Em breve)" para um link ativo que aponta para `/avaliacoes/nova?colaborador_id={id}`.

---

## Verification Plan

### Automated Tests
- Execução do Linter no frontend para garantir conformidade com as regras de estilo do projeto:
  ```bash
  npm run lint
  ```
- Execução do Build de produção no frontend para atestar ausência de erros de build:
  ```bash
  npm run build
  ```
- Execução do Docker Compose no monorepo para verificar os containers:
  ```bash
  docker compose config
  ```

### Manual Verification
1. **Cenário 1 - Fluxo Completo de Sucesso**:
   - Login como Administrador (`admin@gth.com.br`).
   - Acesso à rota `/avaliacoes` -> Clicar em "Nova avaliação".
   - Selecionar colaborador, tipo de avaliação, marcar competências técnicas/comportamentais, aplicar notas e comentários.
   - Preencher a observação geral e clicar em "Salvar avaliação".
   - Confirmar requisição POST 201 e exibição imediata do `ResultadoAvaliacao` com as médias e recomendações geradas.
2. **Cenário 2 - Atalho pelo Colaborador**:
   - Acessar os detalhes de um colaborador específico.
   - Clicar no atalho "Registrar Avaliação".
   - Confirmar redirecionamento para `/avaliacoes/nova?colaborador_id={id}` com o colaborador previamente selecionado no formulário.
3. **Cenário 3 - Validação no Frontend**:
   - Tentar enviar a avaliação sem selecionar nenhuma competência.
   - Confirmar que o frontend bloqueia a requisição e exibe um erro descritivo.
4. **Cenário 4 - Permissão / Erro 403**:
   - Entrar com usuário perfil `COLABORADOR`.
   - Tentar acessar `/avaliacoes/nova`.
   - Confirmar bloqueio visual ou mensagem "Você não possui permissão para registrar esta avaliação" sem deslogar o usuário.
