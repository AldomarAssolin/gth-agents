# Correção dos Estados de Erro nos Formulários (Issue #068)

Este plano de implementação propõe a correção dos estados de erro e carregamento nos formulários do frontend do GTH Agents. Durante a auditoria das páginas e formulários, identificamos uma mistura de responsabilidades entre estados de carregamento e submissão nas páginas de criação e edição. O objetivo deste plano é isolar e corrigir esses comportamentos, garantindo que erros de submissão à API não façam o formulário desaparecer e mantenham os dados inseridos intactos.

---

## Auditoria de Ocorrências Reais no Frontend

Realizamos uma auditoria das páginas do frontend (`frontend/src/pages`) e componentes de formulário (`frontend/src/features`). Abaixo estão listadas as páginas inspecionadas e o respectivo diagnóstico:

| Página / Formulário | Caminho do Arquivo | Diagnóstico de Erro e Comportamento | Classificação | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Login** | [LoginForm.jsx](../../../frontend/src/features/auth/LoginForm.jsx) | Mantém o estado dos inputs e renderiza o erro de autenticação (`401`, `403` ou rede) de forma amigável no topo do formulário via `<ErrorMessage />`. | N/A | **Correto** |
| **Novo Colaborador** | [NovoColaboradorPage.jsx](../../../frontend/src/pages/NovoColaboradorPage.jsx) / [ColaboradorForm.jsx](../../../frontend/src/features/colaboradores/ColaboradorForm.jsx) | Trata erros de carregamento dos catálogos (setores/funções) com botão de retry e trata erros de submissão isoladamente, exibindo a mensagem no topo sem resetar o formulário. | N/A | **Correto** |
| **Registrar Avaliação** | [NovaAvaliacaoPage.jsx](../../../frontend/src/pages/NovaAvaliacaoPage.jsx) / [AvaliacaoForm.jsx](../../../frontend/src/features/avaliacoes/AvaliacaoForm.jsx) | Possui estados separados para erro de carregamento (`fetchError`) e erro de salvamento (`submitError`). No entanto, o `AvaliacaoForm.jsx` possui um bloco de erro morto (`errors.submitError`) que nunca é populado. | Limpeza | **Requer Ajuste** (Limpeza de código morto) |
| **Nova Meta** | [NovaMetaPage.jsx](../../../frontend/src/pages/NovaMetaPage.jsx) | **Bug P2**: Utiliza o mesmo estado `error` para falhas de carregamento e falhas de submissão do formulário. Se a API retornar um erro ao tentar salvar (como `400` por dados inconsistentes ou erro de banco), a página inteira desmonta e renderiza o bloco `<ErrorMessage />` de tela cheia, obrigando o usuário a perder todos os dados digitados. | Bug P2 | **Requer Ajuste** |
| **Novo PDI** | [NovoPDIPage.jsx](../../../frontend/src/pages/NovoPDIPage.jsx) | **Bug P2**: Mesma ocorrência de mistura de estados de erro. O erro de submissão do formulário sobrescreve o estado `error` global da página, fazendo a tela ser substituída pela mensagem de erro geral e eliminando os dados preenchidos no formulário. | Bug P2 | **Requer Ajuste** |
| **Editar PDI** | [EditarPDIPage.jsx](../../../frontend/src/pages/EditarPDIPage.jsx) | **Bug P2**: Mesma ocorrência. Se o salvamento falhar (ex: data de término anterior à de início validada no backend), o formulário é desmontado em favor da tela de erro de conexão/carregamento. | Bug P2 | **Requer Ajuste** |
| **Modal de Ação do PDI** | [PDIDetalhePage.jsx](../../../frontend/src/pages/PDIDetalhePage.jsx) | Exibe erro local do modal sem desmontá-lo ou fechar a caixa de diálogo. | N/A | **Correto** |
| **Feedbacks** | [FeedbacksPage.jsx](../../../frontend/src/pages/FeedbacksPage.jsx) | Página exibe apenas um estado vazio (`EmptyState`), não contendo formulários de entrada de dados ou processos de submissão de erros. | N/A | **Inspecionado (N/A)** |
| **Reconhecimentos** | [ReconhecimentosPage.jsx](../../../frontend/src/pages/ReconhecimentosPage.jsx) | Exibe apenas um estado vazio estático (`EmptyState`), sem formulários ou fluxo de dados ativo. | N/A | **Inspecionado (N/A)** |
| **Cadastros Auxiliares** | N/A | Setores, funções e competências são consumidos como catálogos/lookups de leitura, não possuindo telas ou formulários de cadastro direto no frontend. | N/A | **Inspecionado (N/A)** |
| **Configurações (Mock)** | [ConfiguracoesPage.jsx](../../../frontend/src/pages/ConfiguracoesPage.jsx) | Página estática/mock sem endpoints ou chamadas de API ativas. | N/A | **Mock (N/A)** |

---

## Estrutura e Separação dos Estados de Erro

Para sanar a mistura de responsabilidades, implementaremos as seguintes regras de estado nas páginas afetadas:

1. **`loadError`**:
   - Representa **apenas** falhas de leitura ou inconsistências iniciais que impedem a montagem segura da página (ex: indisponibilidade da API ao obter colaboradores/detalhes iniciais de PDI, parâmetros inválidos na URL, ou falta de autorização de carregamento).
   - Quando `loadError` for verdadeiro, a renderização do formulário é interrompida em favor de uma tela amigável de erro de carregamento com botão de voltar/retry.

2. **`submitError`**:
   - Representa falhas na tentativa de envio dos dados do formulário para o backend (ex: erro de validação da API com HTTP 400 ou falha de conexão na submissão).
   - **Comportamento exigido**:
     - Mantém o formulário montado e visível na tela.
     - Preserva integralmente os dados já digitados pelo usuário nos campos.
     - É limpo/resetado imediatamente antes de qualquer nova tentativa de envio.
     - Não mantém o botão de envio bloqueado (disabled) após a ocorrência da falha, permitindo nova tentativa.

---

## User Review Required

> `[IMPORTANT ]`
> **Remoção de Código Morto em `AvaliacaoForm.jsx`**:
> Confirmamos via análise estática (grep) que a variável `errors.submitError` é apenas consumida nas linhas 215 e 217 de `AvaliacaoForm.jsx`. Não existe qualquer escrita, atribuição ou produtor associado a este campo no formulário de avaliações. Sua remoção é segura e limpa a interface do formulário, mantendo o controle de erro de gravação centralizado em `NovaAvaliacaoPage.jsx`.

> `[WARNING]`
> **Mapeamento de Erros da API**:
> O HTTP 422 **não** é considerado um contrato confirmado do projeto para respostas de erro de validação do backend (o backend utiliza HTTP 400). As validações e mapeamentos serão ajustados em conformidade, sem assumir suporte a HTTP 422 na API.

---

## Proposed Changes

### Páginas de Metas e PDIs (Frontend)

---

#### [MODIFY] [NovaMetaPage.jsx](../../../frontend/src/pages/NovaMetaPage.jsx)
- Separar o estado `error` em `loadError` e `submitError`.
- `loadError` será utilizado para falhas no `useEffect` de busca de colaboradores.
- `submitError` será utilizado no `handleSubmit` para falhas do `criarMeta`.
- No `handleSubmit`:
  - Limpar `submitError` no início.
  - Se falhar, atualizar `submitError` e garantir que o estado `isSubmitting` retorne a `false` no bloco `finally`, liberando o botão.
- Na renderização:
  - O bloco condicional de interrupção (`if (error)`) passa a avaliar apenas `loadError`.
  - Exibir `submitError` (via `<ErrorMessage />`) acima do card do formulário sem ocultar o formulário.

#### [MODIFY] [NovoPDIPage.jsx](../../../frontend/src/pages/NovoPDIPage.jsx)
- Separar `error` em `loadError` (falhas no carregamento de colaboradores) e `submitError` (falhas no envio de `criarPDI`).
- Garantir a limpeza de `submitError` no envio e liberação do botão no `finally`.
- Renderizar `submitError` no topo do card e condicionar a interrupção da página apenas a `loadError`.

#### [MODIFY] [EditarPDIPage.jsx](../../../frontend/src/pages/EditarPDIPage.jsx)
- Separar `error` em `loadError` (falhas no carregamento inicial de PDI) e `submitError` (falhas no `atualizarPDI`).
- Garantir a limpeza de `submitError` no envio e liberação do botão no `finally`.
- Renderizar `submitError` acima do formulário sem desmontá-lo.

#### [MODIFY] [AvaliacaoForm.jsx](../../../frontend/src/features/avaliacoes/AvaliacaoForm.jsx)
- Remover o bloco de renderização de erro morto `errors.submitError` (linhas 215-219), limpando o layout.

---

## Verification Plan

### Validações Técnicas (Antigravity)
O agente Antigravity executará estritamente as seguintes etapas automatizadas para verificação estática e estrutural do código:
1. **Linting**:
   ```bash
   cd frontend && npm run lint
   ```
2. **Build**:
   ```bash
   cd frontend && npm run build
   ```
3. **Testes Automatizados**:
   Execução de testes unitários ou de integração aplicáveis que estejam presentes no repositório.
4. **Verificação de Formatação Git**:
   ```bash
   git diff --check
   ```

### Validações Funcionais e de Navegador (Usuário)
Toda a validação funcional no navegador será realizada pelo usuário no ambiente local de desenvolvimento, cobrindo:
1. Carregamento correto das páginas com o backend ativo.
2. Comportamento sob erro de conexão (interrupção do backend) na submissão de Metas e PDIs (exibição de erro preservando inputs e reativando botões).
3. Envio com datas inconsistentes e dados inválidos (HTTP 400) e persistência do formulário aberto para correção.

---

## Handoff para Validação Humana

Após as validações técnicas automatizadas, utilizaremos a Skill `gth-manual-validation-handoff` para gerar o arquivo de scratchpad específico para guiar os testes do usuário:
* **Caminho**: [docs/scratchpads/issue-068-manual-validation.md](../../../docs/scratchpads/issue-068-manual-validation.md)
* O scratchpad conterá a lista detalhada de casos de teste, inputs para simulação e tabelas para registro de evidências da validação de navegador.
