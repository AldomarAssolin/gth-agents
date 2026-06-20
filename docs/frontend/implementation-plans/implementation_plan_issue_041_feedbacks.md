# Plano de Implementação - Módulo de Feedbacks (Issue #041) - Ajustado Final

Este plano descreve a implementação do módulo frontend de **Feedbacks**, permitindo registrar e listar feedbacks estruturados vinculados a colaboradores.

## Contratos de API Confirmados

### 1. `POST /feedbacks` (Registrar Feedback)
- **Método & URL**: `POST /feedbacks`
- **Permissão (Blueprints/Filtros)**: `@roles_required("ADMIN", "RH", "LIDER")`
- **Payload**:
  ```json
  {
    "colaborador_id": 1,
    "autor_id": 2,
    "ponto_positivo": "Texto descritivo do ponto positivo",
    "acao_recomendada": "Texto descritivo da ação recomendada",
    "contexto": "Texto opcional de contexto",
    "ponto_melhoria": "Texto opcional de ponto de melhoria"
  }
  ```
- **Campos Obrigatórios**: `colaborador_id` (int), `autor_id` (int), `ponto_positivo` (str), `acao_recomendada` (str).
- **Campos Opcionais**: `contexto` (str/null), `ponto_melhoria` (str/null).
- **Origem do Autor**:
  - O backend não deduz o autor a partir do token JWT no use case `RegistrarFeedbackUC`. A API exige o parâmetro `autor_id` no payload.
  - O frontend enviará o valor correspondente à propriedade `user.id` do contexto de autenticação do `AuthContext`. Confirmou-se na inicialização e login do `AuthContext` que o `user.id` é numérico.
- **Melhoria Futura Recomendada**: Recomenda-se ajustar o backend futuramente para obter o ID do autor diretamente do token JWT decodificado no middleware/roteamento, evitando confiar no `autor_id` enviado no payload pelo cliente frontend, o que representa um risco de segurança (personificação).
- **Status HTTP de Sucesso**: `201 Created`
- **Formato da Resposta**: Objeto serializado contendo o feedback criado (`id`, `colaborador_id`, `autor_id`, `contexto`, `ponto_positivo`, `ponto_melhoria`, `acao_recomendada`, `origem`, `data_feedback`, `criado_em`).

### 2. `GET /colaboradores/{id}/evolucao` (Adaptado para Listagem)
- **Método & URL**: `GET /colaboradores/{id}/evolucao`
- **Ordenação**: O backend ordena os feedbacks de forma decrescente (do mais recente para o mais antigo) usando o campo `data_feedback` ou `criado_em` (`reverse=True`).
- **Limitação**: O backend limita o retorno a no máximo 5 registros (`[:5]`). Esta limitação será informada visualmente no frontend (exemplo: "Mostrando os 5 feedbacks mais recentes").

---

## Comportamento de Telas e Fluxos

### 1. Página `/feedbacks` (Listagem Centralizada)
- Não existe listagem global de feedbacks no backend. Portanto, a tela `/feedbacks` funcionará da seguinte maneira:
  1. Carregará a lista de colaboradores acessíveis ao usuário autenticado (`listarColaboradores`).
  2. Exibirá um estado inicial orientando o usuário a selecionar um colaborador para ver seus feedbacks.
  3. Realizará a busca de feedbacks (`GET /colaboradores/{id}/evolucao`) somente após a seleção do colaborador.
  4. Permitirá limpar ou trocar o colaborador a qualquer momento.
  5. Conterá um aviso textual/visual informando que não há uma lista global no backend, sendo necessária a seleção individual.

### 2. Cadastro e Redirecionamento
- A rota `/feedbacks/novo` permitirá cadastrar feedbacks.
- Após o cadastro bem-sucedido, o sistema exibirá uma mensagem de sucesso na tela e redirecionará automaticamente após o sucesso (ou após a visualização da mensagem) para `/colaboradores/{id}/feedbacks`.
- A listagem de feedbacks desse colaborador será devidamente recarregada chamando novamente a evolução.

### 3. Separação de Erros
- **`loadError`**: Erros de carregamento de colaboradores, falha ao obter evolução, colaborador inválido ou fora do escopo acessível (403/404/Erro de conexão). Bloqueará a renderização da página com um componente de erro.
- **`submitError`**: Falhas ao salvar o feedback (`POST /feedbacks`). Exibirá um alerta na parte superior do formulário sem desmontá-lo nem limpar os campos já preenchidos.

### 4. Fora de Escopo
- O endpoint `POST /feedbacks/estruturar` não será consumido, nem haverá botões ou lógica em UI/Service para essa funcionalidade.

---

## Proposed Changes

### Frontend Component

#### [NEW] [feedbacksService.js](../../../frontend/src/features/feedbacks/feedbacksService.js)
Serviço utilizando a instância `api` global:
- `criarFeedback(payload, options)`: Faz POST para `/feedbacks`.
- `listarFeedbacksPorColaborador(colaboradorId, options)`: Faz GET para `/colaboradores/${colaboradorId}/evolucao` e normaliza retornando `.feedbacks`.

#### [NEW] [feedbacksErrors.js](../../../frontend/src/features/feedbacks/feedbacksErrors.js)
Retorna mensagens amigáveis em português para falhas (400, 403, 404, 500, etc.).

#### [NEW] [feedbacksFormatters.js](../../../frontend/src/features/feedbacks/feedbacksFormatters.js)
Formata datas em padrão PT-BR.

#### [NEW] [FeedbackCard.jsx](../../../frontend/src/features/feedbacks/FeedbackCard.jsx)
Card visual padronizado conforme os componentes existentes do projeto, contendo os campos estruturados de feedback e informação visual da limitação/origem.

#### [NEW] [FeedbacksList.jsx](../../../frontend/src/features/feedbacks/FeedbacksList.jsx)
Lista os cards ou exibe estado vazio.

#### [NEW] [FeedbackForm.jsx](../../../frontend/src/features/feedbacks/FeedbackForm.jsx)
Formulário controlado de cadastro, prevenindo duplo envio e preservando os campos digitados.

#### [NEW] [FeedbacksColaboradorPage.jsx](../../../frontend/src/pages/FeedbacksColaboradorPage.jsx)
Página que exibe a lista de feedbacks vinculados a um colaborador específico.

#### [NEW] [NovoFeedbackPage.jsx](../../../frontend/src/pages/NovoFeedbackPage.jsx)
Página para criação de feedback com proteção de rota visual e suporte a query param `?colaborador_id=`.

#### [MODIFY] [FeedbacksPage.jsx](../../../frontend/src/pages/FeedbacksPage.jsx)
Atualizar a página `/feedbacks` para incluir o seletor de colaborador e carregamento sob demanda.

#### [MODIFY] [ColaboradorDetalhe.jsx](../../../frontend/src/features/colaboradores/ColaboradorDetalhe.jsx)
Substituir os botões desativados para direcionar para `/feedbacks/novo?colaborador_id={id}` e `/colaboradores/{id}/feedbacks`.

#### [MODIFY] [AppRoutes.jsx](../../../frontend/src/routes/AppRoutes.jsx)
Registrar as novas rotas.

---

## Verification Plan

### Automated Tests
```bash
cd frontend
npm run lint
npm run build
```

Na raiz:
```bash
docker compose config
git diff --check
```

### Manual Verification
Os cenários manuais estão detalhados em `docs/scratchpads/issue-041-feedbacks-manual-validation.md`.
