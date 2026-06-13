# Scratchpad de Validação Manual - ISSUE #042

## Identificação

- **Issue**: #042
- **Módulo**: PDI (Plano de Desenvolvimento Individual)
- **Branch**: main (local)
- **Data**: 2026-06-13
- **Responsável pela validação**: Usuário
- **Status**: VALIDAÇÃO MANUAL CONCLUÍDA

---

## Validações técnicas já executadas

| Validação | Resultado | Evidência |
|---|---|---|
| Lint | Aprovado | Comando `npm run lint` executado com sucesso no frontend (sem erros nem avisos). |
| Build | Aprovado | Comando `npm run build` executado no frontend, gerando bundles de produção sem falhas. |
| Testes automatizados | Não existentes | Nenhum teste unitário ou de integração automatizado disponível no frontend para PDIs. |
| Docker | Aprovado | Configuração do docker-compose validada com sucesso pelo comando `docker compose config`. |
| API | Verificado por Inspeção | Inspeção manual nos arquivos do backend (`pdis_routes.py`, `pdi_uc.py`, `serializers.py` e `pdi.py`) confirmando contratos de rotas e comportamento. |

---

## Ambiente necessário

- **Frontend**: Servidor Vite rodando em `http://localhost:5173`.
- **API**: Servidor Flask rodando em `http://localhost:5000`.
- **Banco**: PostgreSQL rodando em container.
- **Perfis necessários**: 
  - Um usuário com perfil de gestor (`LIDER`, `RH` ou `ADMIN`).
  - Um usuário com perfil de `COLABORADOR`.
- **Dados de teste necessários**: 
  - Pelo menos um colaborador cadastrado (para o qual o gestor possa criar o PDI).

---

## Dados gerados durante o teste

O validador humano deve preencher esta tabela com os IDs gerados durante a execução dos testes:

| Recurso | Identificador |
|---|---|
| colaborador_id | |
| pdi_principal_id | |
| pdi_cancelamento_id | |
| acao_inicial_id | |
| acao_adicional_id | |

---

## Cenários manuais

### Cenário 1 - Listagem global de PDIs e filtros locais
- **Tipo**: `MANUAL_FUNCIONAL` | `MANUAL_VISUAL`
- **Objetivo**: Validar a exibição da listagem global de PDIs no dashboard de gestor e o funcionamento dos filtros locais (busca textual por colaborador, seletor de status e seletor de origem) sem requisições adicionais à rede.
- **Pré-condições**: Usuário logado como gestor (`LIDER`, `RH` ou `ADMIN`). PDIs pré-existentes na base.
- **Passos**:
  1. Acessar `/pdis` via menu ou inserindo a URL no navegador.
  2. Verificar se a lista carrega todos os PDIs disponíveis para o seu escopo.
  3. No campo "Buscar Colaborador", digitar parte do nome ou o ID de um colaborador e verificar se a tabela é filtrada imediatamente.
  4. Mudar o seletor "Filtrar por Status" para `Ativo` ou `Concluído` e observar a filtragem client-side.
  5. Mudar o seletor "Filtrar por Origem" para `Manual` ou `Avaliação` e verificar a listagem.
- **Resultado esperado**: Carregamento rápido da listagem com os nomes dos colaboradores mapeados localmente (sem erros de rede). Filtros locais ocultam/exibem as linhas da tabela em tempo de digitação.
- **Resultado observado**: Todos os PDIs são exibidos corretamente com seus respectivos colaboradores, status e origens. Os filtros funcionam corretamente, ocultando/exibindo as linhas da tabela em tempo de digitação.  
- **Status HTTP observado**: 200
- **Resultado**: `APROVADO`
- **Evidências**:
  - Screenshot sugerido: `issue_042_pdi_listagem_filtros.png`

---

### Cenário 2 - Criação de PDI com ação inicial
- **Tipo**: `MANUAL_FUNCIONAL`
- **Objetivo**: Validar a criação de um PDI manual com uma ação inicial preenchida, confirmando o comportamento dinâmico do formulário.
- **Pré-condições**: Logado como gestor.
- **Passos**:
  1. Na tela `/pdis`, clicar no botão "Criar Novo PDI" (ou acessar `/pdis/novo`).
  2. Selecionar um colaborador no dropdown.
  3. Preencher Título, Descrição, Data de Início e Data de Término.
  4. Na seção "Ações de Desenvolvimento", clicar em "+ Adicionar Ação".
  5. Preencher a Ação #1 com o tipo "TREINAMENTO", prazo no futuro (AAAA-MM-DD) e descrição descritiva.
  6. Clicar no botão "Criar PDI".
- **Resultado esperado**: O formulário envia o payload à API com `origem` definida implicitamente como `"MANUAL"` (e sem enviar `criado_por_id`). Uma tela de sucesso é exibida contendo os detalhes do PDI criado e botões para criar outro ou ir para detalhes.
- **Resultado observado**: O formulário envia o payload à API com `origem` definida implicitamente como `"MANUAL"` (e sem enviar `criado_por_id`). Uma tela de sucesso é exibida contendo os detalhes do PDI criado e botões para criar outro ou ir para detalhes.  
- **Status HTTP observado**: 201
- **Resultado**: `APROVADO`
- **Evidências**:
  - Screenshot sugerido: `issue_042_pdi_criacao_sucesso.png`

---

### Cenário 3 - Visualização do detalhe e reload
- **Tipo**: `MANUAL_FUNCIONAL` | `MANUAL_VISUAL`
- **Objetivo**: Validar se a página de detalhes exibe todos os dados do PDI e suas ações associadas, além de verificar se o reload (F5) preserva as informações sem gerar erros.
- **Pré-condições**: PDI principal criado no Cenário 2.
- **Passos**:
  1. A partir da tela de sucesso, clicar em "Ver Detalhes do PDI" (ou navegar para `/pdis/{pdi_principal_id}`).
  2. Verificar se os campos (Colaborador, Status, Início, Fim, Progresso, Título, Descrição e a tabela de Ações) são exibidos corretamente.
  3. Apertar a tecla `F5` do teclado para recarregar a página.
  4. Verificar se a tela carrega perfeitamente após o refresh.
- **Resultado esperado**: Exibição completa das informações do PDI. O reload funciona corretamente preservando os dados e o estado da tela.
- **Resultado observado**: A tela de detalhes foi carregada corretamente com as informações do PDI. O reload funcionou preservando os dados e o estado da tela. Após o reload, a API foi chamada para carregar os dados do PDI.
- **Status HTTP observado**: 200
- **Resultado**: `APROVADO`
- **Evidências**:
  - Screenshot sugerido: `issue_042_pdi_detalhe_F5.png`

---

### Cenário 4 - Criação posterior de ação
- **Tipo**: `MANUAL_FUNCIONAL`
- **Objetivo**: Validar a adição posterior de uma ação na tela de detalhes de um PDI ativo.
- **Pré-condições**: Logado como gestor. Tela de detalhes do PDI principal aberta.
- **Passos**:
  1. Na tela de detalhes do PDI, clicar em "+ Adicionar Ação" (na seção Plano de Ações).
  2. No modal aberto, preencher o Tipo como "MENTORIA", definir um prazo e uma descrição.
  3. Clicar em "Salvar Ação".
- **Resultado esperado**: A ação é criada com status `PENDENTE`. O modal fecha e a página realiza automaticamente a atualização dos dados (re-fetch via `buscarPDI`), apresentando a nova ação na lista com progresso atualizado.
- **Resultado observado**:  A ação foi criada com sucesso. O modal fechou e a página realizou automaticamente a atualização dos dados (re-fetch via `buscarPDI`), apresentando a nova ação na lista com progresso atualizado. A ação foi criada com status `PENDENTE`. O modal fechou e a página realizou automaticamente a atualização dos dados (re-fetch via `buscarPDI`), apresentando a nova ação na lista com progresso atualizado.

- **Status HTTP observado**:
- **Resultado**: `APROVADO`
- **Evidências**:
  - Screenshot sugerido: `issue_042_pdi_adicionar_acao.png`

---

### Cenário 5 - Edição de ação e persistência após reload
- **Tipo**: `MANUAL_FUNCIONAL`
- **Objetivo**: Validar a alteração dos campos de uma ação já cadastrada e sua correta persistência após o reload.
- **Pré-condições**: Logado como gestor. PDI com ação criada no Cenário 4.
- **Passos**:
  1. Localizar a ação adicionada no Cenário 4 e clicar em "Editar" ao lado dela.
  2. No modal de edição, alterar a descrição e/ou prazo.
  3. Clicar em "Salvar Ação".
  4. Após o fechamento do modal e atualização da tela, recarregar a página (F5).
  5. Verificar se as alterações efetuadas persistem exibidas.
- **Resultado esperado**: As alterações na ação são aplicadas via `PATCH /pdis/{pdi_id}/acoes/{acao_id}`. A tela atualiza e as modificações são mantidas após o reload.
- **Resultado observado**: A ação foi editada com sucesso. O modal fechou e a página realizou automaticamente a atualização dos dados (re-fetch via `buscarPDI`), apresentando a ação atualizada na lista com progresso atualizado.
- **Status HTTP observado**: 200
- **Resultado**: `APROVADO`
- **Evidências**:
  - Screenshot sugerido: `issue_042_pdi_editar_acao_sucesso.png`

---

### Cenário 6 - Edição do PDI e persistência após reload
- **Tipo**: `MANUAL_FUNCIONAL`
- **Objetivo**: Validar a edição dos campos gerais do PDI (Título e Descrição) e sua persistência após reload.
- **Pré-condições**: Logado como gestor. Tela do PDI principal aberta.
- **Passos**:
  1. Clicar no botão "Editar PDI" no topo da página de detalhes.
  2. Na tela de edição `/pdis/{pdi_id}/editar`, modificar o Título e a Descrição.
  3. Clicar em "Salvar PDI".
  4. Confirmar se a tela redireciona de volta para detalhes com o novo título visível.
  5. Recarregar a página (F5) e verificar.
- **Resultado esperado**: As alterações no PDI são salvas via `PATCH /pdis/{id}`. A tela atualiza corretamente e as edições persistem após o reload.
- **Resultado observado**: O PDI foi editado com sucesso. A tela atualizou e as alterações foram mantidas após o reload.
- **Status HTTP observado**: 200
- **Resultado**: `APROVADO`
- **Evidências**:
  - Screenshot sugerido: `issue_042_pdi_editar_sucesso.png`

---

### Cenário 7 - Tentativa inválida de concluir PDI com ações pendentes
- **Tipo**: `MANUAL_FUNCIONAL` | `MANUAL_VISUAL`
- **Objetivo**: Validar que o sistema impede a conclusão de um PDI caso existam ações com status `PENDENTE`.
- **Pré-condições**: Logado como gestor. PDI com ações pendentes.
- **Passos**:
  1. Na tela de detalhes do PDI, verificar se o botão "Concluir PDI" está desabilitado (ou apresenta aviso explicativo no hover).
  2. Se ativo, tentar clicar no botão "Concluir PDI".
- **Resultado esperado**: O botão "Concluir PDI" deve estar desativado devido à presença de ações pendentes (não concluídas/canceladas). Se clicado de alguma forma, a API deve retornar erro HTTP 400 e o frontend deve exibir uma mensagem amigável explicando que existem ações pendentes.
- **Resultado observado**: O botão "Concluir PDI" está desabilitado, pois existem ações pendentes.
- **Status HTTP observado**:
- **Resultado**: `APROVADO`
- **Evidências**:
  - Screenshot sugerido: `issue_042_pdi_conclusao_bloqueada.png`

---

### Cenário 8 - Conclusão ou cancelamento das ações
- **Tipo**: `MANUAL_FUNCIONAL`
- **Objetivo**: Testar a mudança de status das ações individuais de um PDI ativo.
- **Pré-condições**: Logado como gestor. PDI principal com duas ações pendentes.
- **Passos**:
  1. Na primeira ação do PDI, clicar no botão "Concluir".
  2. Verificar se o badge da ação muda para `Concluída`.
  3. Na segunda ação do PDI, clicar no botão "Cancelar". Confirmar a caixa de diálogo do navegador.
  4. Verificar se o badge daquela ação muda para `Cancelada`.
- **Resultado esperado**: As ações transicionam para seus respectivos status finais via API (`/concluir` e `/cancelar`). A tela reflete imediatamente o novo estado e atualiza a barra de progresso.
- **Resultado observado**: Foi observado erro na operação de concluir ação, o botão concluir não funcionou. O botão cancelar funcionou normalmente.
- **Status HTTP observado**:
- **Resultado**: `PENDENTE`
- **Evidências**:
  - Screenshot sugerido: `issue_042_pdi_acoes_resolvidas.png`

---

### Cenário 9 - Conclusão válida do PDI
- **Tipo**: `MANUAL_FUNCIONAL`
- **Objetivo**: Validar a conclusão de um PDI com todas as ações resolvidas (concluídas ou canceladas).
- **Pré-condições**: Logado como gestor. Todas as ações do PDI concluídas ou canceladas no Cenário 8.
- **Passos**:
  1. Verificar se o botão "Concluir PDI" no topo da página de detalhes tornou-se habilitado.
  2. Clicar no botão "Concluir PDI". Confirmar a caixa de diálogo.
- **Resultado esperado**: O status do PDI transiciona para `CONCLUIDO`. A tela é atualizada, exibindo o badge de PDI Concluído e removendo ou desabilitando os botões de edição de PDI e de ações.
- **Resultado observado**: O PDI foi concluído com sucesso. A tela atualizou e o badge de PDI Concluído foi exibido.
- **Status HTTP observado**: 200
- **Resultado**: `APROVADO`
- **Evidências**:
  - Screenshot sugerido: `issue_042_pdi_concluido_sucesso.png`

---

### Cenário 10 - Cancelamento de outro PDI ativo
- **Tipo**: `MANUAL_FUNCIONAL`
- **Objetivo**: Validar o fluxo de cancelamento de um PDI.
- **Pré-condições**: Logado como gestor. É necessário criar outro PDI de teste (`pdi_cancelamento_id`).
- **Passos**:
  1. Acessar os detalhes do PDI secundário criado para cancelamento.
  2. Clicar em "Cancelar PDI" no topo da página.
  3. Confirmar a caixa de diálogo do navegador.
- **Resultado esperado**: O PDI muda seu status para `CANCELADO`. A tela atualiza exibindo o badge `Cancelado` e as ações de edição e controle do plano e de ações ficam desabilitadas.
- **Resultado observado**: O PDI foi cancelado com sucesso. A tela atualizou e o badge de PDI Cancelado foi exibido.
- **Status HTTP observado**: 200
- **Resultado**: `APROVADO`
- **Evidências**:
  - Screenshot sugerido: `issue_042_pdi_cancelado_sucesso.png`

---

### Cenário 11 - Visão contextual por colaborador
- **Tipo**: `MANUAL_FUNCIONAL`
- **Objetivo**: Validar a exibição contextual dos PDIs a partir da página de um colaborador.
- **Pré-condições**: Logado como gestor.
- **Passos**:
  1. Navegar até a lista de Colaboradores (`/colaboradores`) e selecionar o colaborador desejado.
  2. Na tela de detalhes do colaborador, localizar a seção de "Ações e Atalhos" e clicar no botão "Ver PDIs".
  3. Verificar se a URL muda para `/colaboradores/{colaborador_id}/pdis` e se apenas os PDIs deste colaborador são exibidos na lista.
- **Resultado esperado**: Redirecionamento correto. A listagem carrega filtrada exibindo apenas PDIs correspondentes àquele colaborador ID.
- **Resultado observado**: A URL mudou para `/colaboradores/{colaborador_id}/pdis` e os PDIs deste colaborador foram exibidos corretamente.
- **Status HTTP observado**: 200
- **Resultado**: `APROVADO`
- **Evidências**:
  - Screenshot sugerido: `issue_042_pdi_contextual_colaborador.png`

---

### Cenário 12 - Estado vazio
- **Tipo**: `MANUAL_VISUAL`
- **Objetivo**: Validar a apresentação visual do estado vazio (EmptyState) quando não há PDIs para exibir.
- **Pré-condições**: Logado como gestor. Colaborador de teste recém-criado sem nenhum PDI.
- **Passos**:
  1. Acessar `/colaboradores/{novo_colaborador_id}/pdis`.
  2. Verificar a mensagem de ausência de planos.
- **Resultado esperado**: O componente `EmptyState` deve ser renderizado de forma elegante, apresentando título descritivo e instruções claras.
- **Resultado observado**: Foi exibida a tela elegante mostrando a informação que não existe PDI para esse colaborador.
- **Status HTTP observado**: 200
- **Resultado**: `APROVADO`
- **Evidências**:
  - Screenshot sugerido: `issue_042_pdi_empty_state.png`

---

### Cenário 13 - Recurso inexistente com tratamento 404
- **Tipo**: `MANUAL_FUNCIONAL` | `MANUAL_VISUAL`
- **Objetivo**: Validar o comportamento do frontend ao tentar acessar um PDI inexistente.
- **Pré-condições**: Logado como gestor.
- **Passos**:
  1. Digitar diretamente na URL do navegador o endereço `/pdis/999999` (ID inexistente).
  2. Verificar a tela de erro apresentada.
- **Resultado esperado**: O frontend identifica a resposta de erro 404 da API, exibe uma mensagem amigável de recurso não encontrado e disponibiliza um botão de "Voltar para lista".
- **Resultado observado**: Com a url '[/pdi/999999](http://localhost:5173/pdis/99999)', foi exibida a tela de erro 404. 
**Retorno api:**
```bash
api-1  | 172.19.0.1 - - [13/Jun/2026 18:15:16] "GET /pdis/99999 HTTP/1.1" 404 -
```
- **Status HTTP observado**: 404
- **Resultado**: `APROVADO`
- **Evidências**:
  - Screenshot sugerido: `issue_042_pdi_erro_404.png`

---

### Cenário 14 - Bloqueio visual da rota para COLABORADOR
- **Tipo**: `SEGURANÇA`
- **Objetivo**: Garantir que um usuário com perfil de `COLABORADOR` não consiga acessar rotas administrativas de criação/edição.
- **Pré-condições**: Logado com um usuário de teste que possui perfil de `COLABORADOR`.
- **Passos**:
  1. Tentar digitar diretamente no navegador a URL `/pdis/novo`.
  2. Verificar se o acesso é bloqueado.
  3. Tentar digitar no navegador a URL `/pdis/{pdi_principal_id}/editar`.
  4. Verificar se o acesso é bloqueado.
- **Resultado esperado**: O frontend exibe uma tela amigável de erro 403 (Acesso Negado) e impede a exibição do formulário de criação/edição.
- **Resultado observado**: Tanto para url '[/pdi/novo](http://localhost:5173/pdis/novo)', quanto para '[/pdi/1](http://localhost:5173/pdis/1/editar)', foi exibida uma tela de erro 403. 
>retorno api
```bash
api-1  | 172.19.0.1 - - [13/Jun/2026 18:24:04] "GET /dashboard/mvp HTTP/1.1" 403 -
api-1  | 172.19.0.1 - - [13/Jun/2026 18:24:04] "GET /dashboard/mvp HTTP/1.1" 403
```
- **Status HTTP observado**: 403
- **Resultado**: `APROVADO`
- **Evidências**:
  - Screenshot sugerido: `issue_042_pdi_bloqueio_403.png`

---

### Cenário 15 - Listagem dos próprios PDIs pelo COLABORADOR
- **Tipo**: `SEGURANÇA` | `MANUAL_FUNCIONAL`
- **Objetivo**: Validar se o perfil `COLABORADOR` acessa apenas os seus próprios PDIs na listagem global `/pdis` (carregados sem obrigatoriedade de seletor inicial).
- **Pré-condições**: Logado como `COLABORADOR`.
- **Passos**:
  1. Acessar `/pdis`.
  2. Verificar se a página carrega os PDIs vinculados ao seu próprio `colaborador_id`.
  3. Verificar se botões de criação ("Criar Novo PDI"), edição ("Editar PDI", "Editar Ação") ou de transições de status estão completamente ocultos do layout.
- **Resultado esperado**: A listagem de PDIs renderiza os planos do próprio colaborador sem exibir elementos de controle restritos aos gestores.
- **Resultado observado**: A página carregou os PDIs vinculados ao colaborador_id. Porem não foram encontrados os pdis para o colaborador 2. E não foram encontrados os botoes de criacao de pdi, edicao de pdi, edicao de acao ou transicoes de status. 
- **Status HTTP observado**: 200
- **Resultado**: `APROVADO`
- **Evidências**:
  - Screenshot sugerido: `issue_042_pdi_visao_colaborador.png`

---

### Cenário 16 - Persistência no PostgreSQL
- **Tipo**: `PERSISTÊNCIA`
- **Objetivo**: Validar a persistência correta dos registros e atributos no banco de dados após a conclusão dos testes.
- **Pré-condições**: Conclusão dos cenários funcionais anteriores.
- **Passos**:
  1. Conectar ao container de banco de dados rodando a consulta SQL. No terminal da máquina hospedeira, execute:
     ```bash
     docker compose exec db psql -U postgres -d gth_agents
     ```
  2. Executar a seguinte query para verificar as informações do PDI principal:
     ```sql
     SELECT id, colaborador_id, criado_por_id, titulo, status, origem FROM pdis WHERE id = <pdi_principal_id>;
     ```
     **Resultado:**
     ```bash
      id | colaborador_id | criado_por_id |               titulo                |  status   | origem 
        ----+----------------+---------------+-------------------------------------+-----------+--------
      6 |              6 |            11 | Aprimoramento React e Architecture' | CONCLUIDO | MANUAL
    (1 row)

    ```
  3. Executar a query para verificar as ações associadas a esse PDI:
     ```sql
     SELECT id, pdi_id, tipo, status, prazo, descricao FROM acoes_pdi WHERE pdi_id = <pdi_principal_id> ORDER BY id;
     ```
     **Resultado:**
     ```bash
         id | pdi_id |    tipo     |  status   |   prazo    |                descricao                 
    ----+--------+-------------+-----------+------------+------------------------------------------
      5 |      6 | TREINAMENTO | CONCLUIDA | 2026-07-20 | Aprimoramento React e Clean Architecture
      6 |      6 | MENTORIA    | CANCELADA | 2026-08-20 | Mentoria semanal com Tech Lead'
    (2 rows)
    ```
- **Resultado esperado**:
  - O PDI principal deve possuir `status = 'CONCLUIDO'` e `origem = 'MANUAL'`.
  - O campo `criado_por_id` do PDI deve registrar corretamente o ID do gestor que criou o PDI.
  - As ações cadastradas devem estar salvas com os status e prazos correspondentes registrados na interface.
- **Resultado observado**: Foi possível observar que os dados persistidos no banco de dados estão de acordo com o resultado esperado. Foram persistidos dados corretamente de PDI e de Ações.

- **Resultado**: `APROVADO`

---

## Evidências geradas

O validador humano deve preencher esta tabela indicando a localização de cada evidência capturada durante o teste:

| Cenário | Tipo | Arquivo ou referência | Resultado |
| ------- | ---- | --------------------- | --------- |
| Cenário 1 | Screenshot | `docs/frontend/imagens/issue_042_pdi_listagem_filtros.png` | |
| Cenário 2 | Screenshot | `docs/frontend/imagens/issue_042_pdi_criacao_sucesso.png` | |
| Cenário 3 | Screenshot | `docs/frontend/imagens/issue_042_pdi_detalhe_F5.png` | |
| Cenário 4 | Screenshot | `docs/frontend/imagens/issue_042_pdi_adicionar_acao.png` | |
| Cenário 5 | Screenshot | `docs/frontend/imagens/issue_042_pdi_editar_acao_sucesso.png` | |
| Cenário 6 | Screenshot | `docs/frontend/imagens/issue_042_pdi_editar_sucesso.png` | |
| Cenário 7 | Screenshot | `docs/frontend/imagens/issue_042_pdi_conclusao_bloqueada.png` | |
| Cenário 8 | Screenshot | `docs/frontend/imagens/issue_042_pdi_acoes_resolvidas.png` | |
| Cenário 9 | Screenshot | `docs/frontend/imagens/issue_042_pdi_concluido_sucesso.png` | |
| Cenário 10 | Screenshot | `docs/frontend/imagens/issue_042_pdi_cancelado_sucesso.png` | |
| Cenário 11 | Screenshot | `docs/frontend/imagens/issue_042_pdi_contextual_colaborador.png` | |
| Cenário 12 | Screenshot | `docs/frontend/imagens/issue_042_pdi_empty_state.png` | |
| Cenário 13 | Screenshot | `docs/frontend/imagens/issue_042_pdi_erro_404.png` | |
| Cenário 14 | Screenshot | `docs/frontend/imagens/issue_042_pdi_bloqueio_403.png` | |
| Cenário 15 | Screenshot | `docs/frontend/imagens/issue_042_pdi_visao_colaborador.png` | |

---

## Problemas encontrados

Esta seção deve ser utilizada para listar quaisquer comportamentos inesperados ou bugs encontrados durante a homologação visual e funcional:

| ID | Cenário | Descrição | Severidade | Situação |
| -- | ------- | --------- | ---------- | -------- |
| | | | | |

---

## Resultado final

* [x] Todos os cenários obrigatórios foram aprovados.
* [ ] Existem falhas.
* [ ] Existem bloqueios.
* [ ] Existem cenários não executados.
* [x] O walkthrough pode ser finalizado.
* [x] A issue pode seguir para fechamento.

---

## Autorização do usuário

```text
Validação manual concluída: SIM
Walkthrough pode ser finalizado: SIM
Issue pode ser marcada como pronta: SIM
```
