# Scratchpad de Validação Manual - Responsividade e Usabilidade (Issue #038)

Este documento define os cenários de teste específicos para verificar se as melhorias de responsividade e usabilidade atendem aos requisitos da Issue #038.

---

## Cenário 1: Drawer Mobile e Topbar (< 1024px)
*   **Objetivo:** Validar a funcionalidade de gaveta (drawer) e adaptação do Topbar em telas de celular e tablet.
*   **Passos:**
    1. Reduzir a largura da janela para menos de 1024px (por exemplo, 375px ou 768px).
    2. Verificar se a Sidebar estática desapareceu e se o botão hambúrguer é exibido na Topbar.
    3. Clicar no botão hambúrguer para abrir a Sidebar (Drawer).
    4. Verificar se a Sidebar surge com transição suave e se um backdrop escuro com desfoque cobre o resto da tela.
    5. Clicar no botão "X" dentro da Sidebar e verificar se ela fecha.
    6. Abrir o Drawer novamente e clicar no backdrop (área escura fora da sidebar). Verificar se ela fecha.
    7. Abrir o Drawer, clicar em qualquer link de navegação (ex: "Metas"). Verificar se a rota muda e o Drawer se fecha automaticamente.
    8. Verificar na Topbar se o texto "Bem-vindo ao painel de controle" fica oculto e se o nome do usuário e o botão "Sair" não quebram nem causam estouro horizontal.

---

## Cenário 2: Overflow de Tabelas e Rolagem Lateral
*   **Objetivo:** Garantir que tabelas não quebrem o layout ou espremam dados em resoluções menores.
*   **Passos:**
    1. Acessar a tela de "Colaboradores" em modo mobile (375px).
    2. Verificar se a tabela de colaboradores possui rolagem horizontal independente (`overflow-x-auto`) e não empurra o layout para o lado.
    3. Fazer o mesmo nas listagens de "Metas", "PDI", e nas páginas de configurações ("Usuários", "Competências", "Setores" e "Funções").
    4. Verificar se a largura mínima de visualização impede que o texto das colunas fique ilegível ou excessivamente quebrado.

---

## Cenário 3: Grades e Cartões Responsivos
*   **Objetivo:** Verificar se grids se transformam em layouts de coluna única no mobile e se os cartões se ajustam de forma compacta.
*   **Passos:**
    1. Acessar o Dashboard em telas desktop (>= 1280px), tablet (768px) e celular (375px).
    2. Confirmar se o grid de estatísticas passa de 4 colunas (desktop) para 2 colunas (tablet) e 1 coluna (celular).
    3. Verificar se os grids secundários do Dashboard (Distribuição de Perfis e Alertas) empilham de forma limpa.
    4. Verificar se os cartões da página de Evolução do Colaborador (Pontos Fortes, Pontos de Melhoria, Recomendações) se adaptam de 3 colunas (desktop) para 1 coluna no mobile.
    5. Confirmar se os paddings dos componentes `Card` mudaram de `p-6` para `p-4` em telas pequenas para maximizar a área de leitura.

---

## Cenário 4: Altura de Botões e Área de Toque
*   **Objetivo:** Garantir usabilidade no toque móvel com altura mínima de 40px em botões e elementos interativos.
*   **Passos:**
    1. Verificar o tamanho dos botões primários e secundários (como "Novo Usuário", "Editar", etc.) no celular.
    2. Medir visualmente ou inspecionar se a altura total dos botões atinge ou supera 40px (`py-2.5` garante isso).
    3. Testar a facilidade de clique no botão hambúrguer da Topbar e no botão "X" da Sidebar.

---

## Resultados das Validações
*   [x] Cenário 1: Drawer Mobile e Topbar
*   [x] Cenário 2: Overflow de Tabelas e Rolagem Lateral
*   [x] Cenário 3: Grades e Cartões Responsivos
*   [x] Cenário 4: Altura de Botões e Área de Toque
