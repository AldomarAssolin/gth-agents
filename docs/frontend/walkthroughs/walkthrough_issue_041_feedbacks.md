# Walkthrough - Implementação do Módulo de Feedbacks (Issue #041)

Este documento registra a implementação técnica, arquitetura, decisões de design, tratamento de erros, e a validação do módulo frontend de **Feedbacks** no GTH Agents.

---

## 1. Contrato da API Consumido

### `POST /feedbacks` (Registrar Feedback)
- **Roteamento & Permissões**: `@roles_required("ADMIN", "RH", "LIDER")`
- **Payload Enviado**:
  ```json
  {
    "colaborador_id": 1,
    "autor_id": 2,
    "ponto_positivo": "Texto descritivo",
    "acao_recomendada": "Texto descritivo",
    "contexto": "Texto opcional ou null",
    "ponto_melhoria": "Texto opcional ou null"
  }
  ```
- **Nota de Segurança / Decisão de Design**: A API Flask exige `autor_id` diretamente no payload. O frontend recupera o ID a partir de `user.id` disponível no `AuthContext`, após validar que o valor existe e é numérico.
- **Melhoria Técnica Futura**: Registra-se para melhoria futura que o backend obtenha o autor do feedback diretamente a partir do JWT decodificado no middleware de autenticação, evitando o envio de `autor_id` pelo payload, mitigando o risco de personificação de usuários.

### `GET /colaboradores/{id}/evolucao` (Histórico de Feedbacks)
- **Ordenação**: Ordenado por data de forma decrescente no backend (`reverse=True`).
- **Limitação de histórico**: Limitado a no máximo 5 registros recentes. Uma mensagem explicativa sobre essa limitação de histórico foi adicionada na listagem de feedbacks no frontend.
- **Risco técnico conhecido**: enquanto o backend aceitar `autor_id` no payload, a integridade da autoria depende de validação server-side. O frontend envia o usuário autenticado atual, mas o backend deve ser ajustado futuramente para não confiar em identificadores enviados pelo cliente.

---

## 2. Decisões Técnicas de Frontend

### Separação de Fluxos de Erros
- **Erros de Carregamento (`loadError`)**: Controlam falhas ao inicializar dados (ex: colaboradores inexistentes ou fora de escopo de permissão). Interrompem a renderização do conteúdo principal da página e exibem um estado de erro com opção de nova tentativa, quando aplicável.
- **Erros de Envio (`submitError`)**: Ocorrem em falhas de submissão do formulário. São renderizados no topo da tela, permitindo que o usuário visualize o problema sem que o formulário seja desmontado ou limpo, preservando o progresso da digitação.

### Redirecionamento e Mensagem de Sucesso
- Após a criação bem-sucedida, o formulário exibe uma caixa verde de sucesso (`Sucesso: Feedback registrado com sucesso! Redirecionando...`).
- Após 1,5 segundos, o usuário é redirecionado automaticamente para `/colaboradores/{id}/feedbacks`.
- O estado de navegação é passado com o sucesso, exibindo um banner verde closeable também na tela de listagem de feedbacks para confirmar o sucesso da operação.
- A espera de 1,5 segundo foi usada para permitir que o usuário leia a confirmação antes do redirecionamento automático.

---

## 3. Arquivos Criados e Alterados

### [NEW] [feedbacksService.js](../../../frontend/src/features/feedbacks/feedbacksService.js)
Serviço para interagir com o backend: `criarFeedback` e `listarFeedbacksPorColaborador`.

### [NEW] [feedbacksErrors.js](../../../frontend/src/features/feedbacks/feedbacksErrors.js)
Traduz e trata os códigos de erro HTTP retornados pela API de feedbacks.

### [NEW] [feedbacksFormatters.js](../../../frontend/src/features/feedbacks/feedbacksFormatters.js)
Formata datas em formato PT-BR.

### [NEW] [FeedbackCard.jsx](../../../frontend/src/features/feedbacks/FeedbackCard.jsx)
Card visual padronizado conforme os componentes existentes do projeto, com suporte a exibição de nome de colaborador condicional, contexto e campos de feedback estruturado.

### [NEW] [FeedbacksList.jsx](../../../frontend/src/features/feedbacks/FeedbacksList.jsx)
Lista os cards de feedback e exibe um aviso claro sobre a limitação de 5 registros retornados pelo backend.

### [NEW] [FeedbackForm.jsx](../../../frontend/src/features/feedbacks/FeedbackForm.jsx)
Formulário controlado de feedbacks estruturados, garantindo validação local antes da submissão.

### [NEW] [NovoFeedbackPage.jsx](../../../frontend/src/pages/NovoFeedbackPage.jsx)
Página para registrar feedbacks com controle de permissão e preenchimento prévio por URL.

### [NEW] [FeedbacksColaboradorPage.jsx](../../../frontend/src/pages/FeedbacksColaboradorPage.jsx)
Página para listar o histórico de feedbacks do colaborador selecionado com suporte a reload em caso de falha.

### [MODIFY] [FeedbacksPage.jsx](../../../frontend/src/pages/FeedbacksPage.jsx)
Página central `/feedbacks` adaptada com um seletor para carregamento sob demanda de feedbacks por colaborador individual.

### [MODIFY] [ColaboradorDetalhe.jsx](../../../frontend/src/features/colaboradores/ColaboradorDetalhe.jsx)
Substituição dos botões desativados pelos links ativos de "Registrar Feedback" e "Ver Feedbacks".

### [MODIFY] [AppRoutes.jsx](../../../frontend/src/routes/AppRoutes.jsx)
Registro das novas rotas de cadastro e listagem.

---

## 4. Validações Executadas

A validação funcional em navegador foi preparada no scratchpad `docs/scratchpads/issue-041-feedbacks-manual-validation.md` e permanece sob responsabilidade do homologador humano.

### Lint
Executado `npm run lint` na pasta `frontend`:
```bash
> gth-agents-web@0.0.0 lint
> eslint .
```
*Status:* Concluído com zero erros e avisos.

### Build
Executado `npm run build` na pasta `frontend`:
```bash
vite v8.0.14 building client environment for production...
✓ 186 modules transformed.
dist/index.html                   0.46 kB │ gzip:   0.29 kB
dist/assets/index-DZyC1GsF.css   27.25 kB │ gzip:   5.79 kB
dist/assets/index-DfK6M7-q.js   478.21 kB │ gzip: 129.06 kB
✓ built in 1.05s
```
*Status:* Concluído com sucesso.

### Docker Compose Config
Executado `docker compose config` na raiz:
*Status:* Arquivo YAML validado e funcional.

### Git Diff Check
Executado `git diff --check` na raiz:
*Status:* Sem erros de formatação ou espaços em branco.

### Regras de Organização (files.md)
- `find frontend backend -maxdepth 1 -type f` -> Retorno vazio.
- `grep -R "/home/" docs` -> Retorno vazio (sem caminhos absolutos locais).
- `find docs/frontend docs/scratchpads -type f | sort` confirmou a presença dos documentos da Issue #041 nos diretórios esperados, sem duplicatas relacionadas ao módulo de feedbacks.
