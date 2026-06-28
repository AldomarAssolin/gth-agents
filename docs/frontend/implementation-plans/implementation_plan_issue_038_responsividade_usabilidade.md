# Plano de Implementação - Melhorar Responsividade e Usabilidade (Issue #038)

Este plano detalha as melhorias de responsividade (mobile-first), usabilidade e consistência visual para o frontend do GTH Agents, garantindo uma experiência adequada em dispositivos desktop, tablet e celular.

## User Review Required

> [!IMPORTANT]
> **Alterações no Layout Global (`AppLayout`):**
> O layout global passará a gerenciar o estado da Sidebar (aberta/fechada) no mobile. No desktop (telas grandes >= 1024px), a sidebar continuará fixa e visível. No mobile/tablet (< 1024px), ela passará a ser um Drawer absoluto com um backdrop escuro, acionado por um botão de menu (hambúrguer) na Topbar.

> [!WARNING]
> **Preservação Funcional:**
> Não haverá alterações nas regras de negócio, rotas ou contratos de API. O foco é exclusivamente na usabilidade (tamanho de botões, largura dos campos, quebra de tabelas e grids, empilhamento no mobile e padronização visual de estados e feedbacks).

## Open Questions

Não há dúvidas técnicas abertas. Seguiremos a estratégia mobile-first recomendada com as classes utilitárias do Tailwind CSS.

---

## Proposed Changes

### 1. Layout Global & Navegação

#### [MODIFY] [AppLayout.jsx](../../../frontend/src/layouts/AppLayout.jsx)
- Introduzir estado react `isSidebarOpen` (padrão `false`).
- Passar propriedades de controle de visibilidade para a Sidebar e Topbar.
- Adicionar backdrop escuro no mobile quando a Sidebar estiver aberta.
- Reduzir padding da área principal de `p-8` para `p-4 md:p-8` para melhor aproveitamento em telas pequenas.

#### [MODIFY] [Sidebar.jsx](../../../frontend/src/components/layout/Sidebar.jsx)
- Modificar o container principal do componente para usar posicionamento fixo e animação de slide no mobile: `fixed inset-y-0 left-0 z-50 transform -translate-x-full lg:translate-x-0 lg:static lg:transform-none transition-transform duration-300 ease-in-out`.
- Controlar a visibilidade baseando-se no estado `isOpen` (se ativo, usar `translate-x-0`, senão `-translate-x-full` no mobile).
- Adicionar botão de fechar (X) no topo da Sidebar apenas visível no mobile.
- Chamar callback `onClose` ao clicar em qualquer item de menu (para fechar automaticamente após navegação no celular).

#### [MODIFY] [Topbar.jsx](../../../frontend/src/components/layout/Topbar.jsx)
- Adicionar botão de menu (hambúrguer) no canto esquerdo da Topbar, visível apenas em telas menores (`lg:hidden`).
- Ao clicar no botão, chamar `onToggleSidebar` para abrir a Sidebar.
- Ajustar os espaçamentos e a quebra de texto para evitar que as informações do usuário/botão de sair quebrem layout em telas de 375px.

### 2. Componentes de UI Comuns

#### [MODIFY] [Table.jsx](../../../frontend/src/components/ui/Table.jsx)
- Garantir que a tabela esteja envolvida por uma `div` com `w-full overflow-x-auto` para evitar estouro horizontal.
- Se necessário, ajustar paddings de colunas (`px-4 py-3` no mobile).

#### [MODIFY] [Card.jsx](../../../frontend/src/components/ui/Card.jsx)
- Ajustar paddings internos de `p-6` para `p-4 sm:p-6` para melhor legibilidade no mobile.

#### [MODIFY] [Button.jsx](../../../frontend/src/components/ui/Button.jsx)
- Garantir tamanhos mínimos de toque adequados (altura de pelo menos 40px no mobile).
- Permitir passagem de classe de largura completa (`w-full`) para ações em formulários mobile.

#### [MODIFY] [Input.jsx](../../../frontend/src/components/ui/Input.jsx) / [Select.jsx](../../../frontend/src/components/ui/Select.jsx)
- Ajustar os tamanhos de fonte e paddings para maior conforto de digitação e consistência visual.

### 3. Páginas e Fluxos Principais

#### [MODIFY] Páginas do Sistema (`frontend/src/pages/*.jsx`)
- **DashboardPage.jsx**: Ajustar o grid de cards de estatísticas (`grid-cols-1 sm:grid-cols-2 lg:grid-cols-4`) e a listagem de registros recentes para quebrar adequadamente no celular.
- **ColaboradoresPage.jsx** / **ColaboradorDetalhePage.jsx**: Ajustar ações e tabelas/telas de detalhes para empilhar no mobile.
- **EvolucaoColaboradorPage.jsx**: Ajustar o layout em abas/seções para empilhamento vertical suave.
- **MetasPage.jsx** / **PDIsPage.jsx** / **FeedbacksPage.jsx** / **ReconhecimentosPage.jsx**: Revisar grids de filtros, listagens de cards e tabelas, garantindo que botões de ação principal não fiquem espremidos.
- **LoginPage.jsx**: Ajustar card de login para centralizar perfeitamente no celular com margens confortáveis.
- **Cadastros Auxiliares** (Setores, Funções, Usuários, Competências): Revisar grids de formulários e tabelas.

---

## Estratégia de Responsividade

- **Mobile First / breakpoints do Tailwind**:
  - `sm` (640px)
  - `md` (768px)
  - `lg` (1024px)
  - `xl` (1280px)
- **Tabelas**: Todas receberão contêiner com rolagem horizontal e quebra de palavras configurada.
- **Grids**: Trocar grids estáticos por dinâmicos (`grid-cols-1 md:grid-cols-2 lg:grid-cols-3`).

---

## Riscos

- **Quebras de Layout Específicas**: Alguns modais ou formulários aninhados em cards podem ter larguras fixas rígidas (`w-[500px]`). Vamos inspecionar e trocar para larguras máximas com flexibilidade (`w-full max-w-lg`).
- **Navegação Mobile**: Certificar que o menu drawer fecha corretamente ao clicar no backdrop ou em itens, evitando sensação de travamento.

---

## Fora do Escopo

- Modificar chamadas de API ou comportamento do backend.
- Adicionar novos campos ou regras de negócio.
- Mudar esquemas de cores globais ou criar tema escuro alternativo.
- Adicionar bibliotecas externas de gráficos ou UI.

---

## Verification Plan

### Automated Tests
- Executar lint do frontend:
  ```bash
  cd frontend && npm run lint
  ```
- Executar build de produção do frontend:
  ```bash
  cd frontend && npm run build
  ```
- Validar configuração do Docker Compose:
  ```bash
  docker compose config
  ```

### Manual Verification
1. Criar Scratchpad em `docs/scratchpads/issue-038-manual-validation.md` contendo cenários de validação detalhados por página.
2. Levantar o ambiente (`docker compose up` ou `npm run dev` localmente).
3. Testar a interface em 3 resoluções simuladas (Desktop 1366px, Tablet 768px, Mobile 375px/390px).
4. Validar o comportamento do Drawer, fechamento ao navegar, overflow de tabelas e grids de formulários.
