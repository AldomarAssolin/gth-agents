# Implementar ISSUE #042 - Módulo Frontend de PDI (Plano de Desenvolvimento Individual)

Este plano descreve a implementação do módulo de PDI no frontend do GTH Agents, utilizando os contratos reais fornecidos pelo backend para criar, listar, atualizar e gerenciar os planos de desenvolvimento individual e suas respectivas ações.

---

## Contratos Reais do Backend Identificados

Após a inspeção do backend (rotas em `pdis_routes.py`, use cases em `pdi_uc.py`, enums em `pdi_enums.py` e mapeamento de exceções em `error_handler.py`), os seguintes contratos foram validados:

### 1. Enums de Domínio
*   **`StatusPDI`**: `RASCUNHO`, `ATIVO`, `CONCLUIDO`, `CANCELADO`
*   **`OrigemPDI`**: `AVALIACAO`, `FEEDBACK`, `META`, `INDICACAO_LIDER`, `AGENTE_IA`, `MANUAL`
*   **`TipoAcaoPDI`**: `TREINAMENTO`, `MENTORIA`, `LEITURA`, `PRATICA_SUPERVISIONADA`, `PARTICIPACAO_PROJETO`, `ACOMPANHAMENTO_LIDER`, `OUTRO`
*   **`StatusAcaoPDI`**: `PENDENTE`, `EM_ANDAMENTO`, `CONCLUIDA`, `CANCELADA`

### 2. Tabela de Endpoints Confirmados

| Operação | Método e URL | Permissão | Request (Body / Params) | Response (JSON) | Status de Sucesso | Erros Mapeados |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Criar PDI** | `POST /pdis` | `ADMIN`, `RH`, `LIDER` | `{ "colaborador_id": int, "titulo": str, "descricao": str, "origem": "MANUAL", "data_inicio": "YYYY-MM-DD", "data_fim": "YYYY-MM-DD", "acoes": [ { "tipo": str, "descricao": str, "prazo": "YYYY-MM-DD" } ] }` | PDI criado, com `id`, `status` (`ATIVO`), `acoes` (com `id`, status `PENDENTE`) e timestamps. | `201` | **400**: Dados ausentes ou data inválida.<br>**403**: Lider de outro setor.<br>**404**: Colaborador não encontrado. |
| **Listar todos os PDIs** | `GET /pdis` | Qualquer usuário | *Nenhum* | Lista completa de PDIs acessíveis pelo escopo do usuário. Retorna apenas `colaborador_id` (não inclui o nome do colaborador). | `200` | Filtra no backend por setor se `LIDER`, ou retorna apenas os do próprio `COLABORADOR` (via `colaborador_id` do token). |
| **Buscar PDI** | `GET /pdis/<id>` | Qualquer usuário | `id` na URL | Objeto PDI contendo dados principais e o array de `acoes` preenchido. | `200` | **403**: Fora do escopo de acesso.<br>**404**: PDI não encontrado. |
| **Atualizar PDI** | `PATCH /pdis/<id>` | `ADMIN`, `RH`, `LIDER` | `{ "titulo": str, "descricao": str, "data_inicio": "YYYY-MM-DD", "data_fim": "YYYY-MM-DD" }` | PDI atualizado. | `200` | **400**: Se o PDI estiver concluído/cancelado.<br>**403**: Fora do escopo.<br>**404**: PDI não encontrado. |
| **Concluir PDI** | `PATCH /pdis/<id>/concluir` | `ADMIN`, `RH`, `LIDER` | *Nenhum* | PDI com status `CONCLUIDO`. | `200` | **400**: Se houver ações pendentes ou estiver cancelado. |
| **Cancelar PDI** | `PATCH /pdis/<id>/cancelar` | `ADMIN`, `RH`, `LIDER` | *Nenhum* | PDI com status `CANCELADO`. | `200` | **400**: Se PDI já estiver concluído. |
| **Listar por Colaborador** | `GET /colaboradores/<id>/pdis` | Qualquer usuário | `colaborador_id` na URL | Lista de PDIs vinculados àquele colaborador específico. | `200` | **403**: Sem acesso ao colaborador. |
| **Criar Ação PDI** | `POST /pdis/<id>/acoes` | `ADMIN`, `RH`, `LIDER` | `{ "tipo": str, "descricao": str, "prazo": "YYYY-MM-DD" }` | Ação criada (status `PENDENTE`). | `201` | **400**: Prazo inválido ou dados vazios. |
| **Atualizar Ação** | `PATCH /pdis/<pdi_id>/acoes/<id>` | `ADMIN`, `RH`, `LIDER` | `{ "tipo": str, "descricao": str, "prazo": "YYYY-MM-DD" }` | Ação atualizada. | `200` | **400**: Validação de tipo/prazo.<br>**404**: Ação não encontrada no PDI. |
| **Concluir Ação** | `PATCH /pdis/<pdi_id>/acoes/<id>/concluir` | `ADMIN`, `RH`, `LIDER` | *Nenhum* | Ação com status `CONCLUIDA`. | `200` | **400**: Se ação já estiver com status `CANCELADA`. |
| **Cancelar Ação** | `PATCH /pdis/<pdi_id>/acoes/<id>/cancelar` | `ADMIN`, `RH`, `LIDER` | *Nenhum* | Ação com status `CANCELADA`. | `200` | Mapeia fluxo de cancelamento. |

---

## Limitações do Backend & Decisões de Frontend

### 1. Limitações Identificadas no Backend
*   **Origem e Criação do Criador (`criado_por_id`)**: Foi confirmado que o campo `criado_por_id` **não** faz parte do payload aceito no JSON do body de `POST /pdis`. O backend extrai este valor automaticamente no controller (`pdis_routes.py`) através de `g.usuario.get("id")`, que por sua vez é obtido do token JWT.
    *   *Decisão de Frontend*: O frontend não incluirá `criado_por_id` no payload enviado para o backend. Para fins de auditoria visual interna ou exibição, o ID do usuário autenticado no frontend é mapeado pela propriedade `user.id` disponibilizada pelo `AuthContext`.
*   **Dados do Colaborador em `GET /pdis`**: O endpoint `GET /pdis` retorna apenas `colaborador_id` e não anexa o nome correspondente do colaborador.
    *   *Decisão de Frontend*: Para evitar requisições N+1 ao carregar a lista de PDIs na página geral `/pdis`, o frontend carregará previamente a listagem de colaboradores acessíveis (usando a função `listarColaboradores` do serviço de colaboradores) e construirá um dicionário local `Map<id, nome>` para resolver e renderizar o nome do colaborador na tabela instantaneamente.
*   **Transição de Status de Ação para `EM_ANDAMENTO`**: A entidade de domínio `AcaoPDI` possui um método interno `iniciar()`. No entanto, **não existe endpoint ou caso de uso** no backend Flask (`pdis_routes.py`, `pdi_uc.py`) exposto para disparar esse método ou atualizar a ação para `EM_ANDAMENTO`. O caso de uso `AtualizarAcaoPDIUC` apenas altera `tipo`, `descricao` e `prazo`.
    *   *Decisão de Frontend*: O status `EM_ANDAMENTO` ficará restrito ao escopo do backend e banco. O frontend não oferecerá botões de transição para este status, limitando-se ao fluxo de ciclo de vida mapeado em endpoints reais: `PENDENTE` -> `CONCLUIDA` ou `CANCELADA`.
*   **Ausência de HTTP 422**: O backend não utiliza HTTP 422 para erros de validação de negócios e formulários. Erros de validação no usecase (`ValidationError`) retornam globalmente **HTTP 400**.
    *   *Decisão de Frontend*: Mapearemos tratamentos amigáveis estritamente sob os códigos 400 (dados inválidos), 401 (não autorizado), 403 (acesso negado) e 404 (recurso não encontrado). O mapeamento de HTTP 422 foi formalmente removido.

### 2. Decisões de Arquitetura do Frontend
*   **Origem do PDI**: Os PDIs criados manualmente pela interface do frontend serão definidos estritamente com `"origem": "MANUAL"` no payload enviado à API. Não serão apresentadas opções de origem alternativas (como `AGENTE_IA` ou `AVALIACAO`) no formulário de criação, pois essas são reservadas para integrações e rotinas de sistema.
*   **Consolidação de Requisições de Ações**: Uma vez que o endpoint `GET /pdis/<id>` retorna o objeto PDI completo contendo a lista aninhada de suas ações (`acoes: [...]`), **não** utilizaremos o endpoint secundário `GET /pdis/<id>/acoes` no frontend. A função de listagem de ações (`listarAcoesPDI`) foi eliminada do serviço e das dependências de AbortController para reduzir chamadas desnecessárias de rede.
*   **Página Principal `/pdis`**: Renderizará a listagem global obtida de `GET /pdis` diretamente (sem a obrigatoriedade de selecionar um colaborador primeiro). Gestores visualizarão múltiplos PDIs de diferentes colaboradores de acordo com o escopo de liderança ou RH. Colaboradores comuns visualizarão apenas seus próprios PDIs.
*   **Visão Contextual `/colaboradores/:id/pdis`**: Permanecerá como uma tela específica para exibir o histórico e evolução de PDIs de um único colaborador, consumindo `GET /colaboradores/${colaboradorId}/pdis`.
*   **Filtros Locais (Client-Side)**: A listagem em `/pdis` incluirá filtros rápidos que não demandam requisições adicionais ao backend:
    *   *Colaborador* (filtro de texto dinâmico pesquisando pelo nome do colaborador);
    *   *Status do PDI* (Todos, RASCUNHO, ATIVO, CONCLUIDO, CANCELADO);
    *   *Origem do PDI* (Todos, MANUAL, AVALIACAO, FEEDBACK, etc.).
*   **Sincronização de Tela (Refresh Strategy)**:
    *   Após qualquer operação de escrita (criar/editar PDI, criar/editar ação, concluir/cancelar PDI ou ação), o frontend re-executará a consulta correspondente (`buscarPDI` para página de detalhes, ou `listarPDIs` para página de listagem) atualizando o estado local.
*   **Gerenciamento de Requisições com `AbortController`**:
    *   Todas as chamadas assíncronas de leitura (`listarPDIs`, `buscarPDI`, `listarPDIsPorColaborador`) aceitarão um objeto `options` contendo um `signal` de `AbortController`. No `useEffect` correspondente, a função de cleanup invocará `controller.abort()`.

---

## User Review Required

> [!IMPORTANT]
> **Fluxo de Ações do PDI**: Para gerenciar as ações individualmente, haverá uma interface dedicada (modais ou formulários de edição rápida) dentro da visualização de detalhes do PDI (`/pdis/:id`). Gestores poderão editar o conteúdo e prazo das ações, ou transicioná-las diretamente para Concluída/Cancelada.

> [!WARNING]
> **Permissão do Colaborador**: Colaboradores logados não verão botões de edição, criação, conclusão ou cancelamento de PDIs e ações. Qualquer tentativa de acessar rotas de criação resultará na tela 403 amigável.

---

## Proposed Changes

### Módulo de PDI (Frontend)

---

#### [NEW] [pdisService.js](../../../frontend/src/features/pdis/pdisService.js)
Serviço de integração Axios aceitando `options` com `signal` em métodos de leitura:
- `listarPDIs(options)`: `GET /pdis`.
- `buscarPDI(pdiId, options)`: `GET /pdis/${pdiId}`.
- `criarPDI(payload)`: `POST /pdis` (sem enviar `criado_por_id`).
- `atualizarPDI(pdiId, payload)`: `PATCH /pdis/${pdiId}`.
- `concluirPDI(pdiId)`: `PATCH /pdis/${pdiId}/concluir`.
- `cancelarPDI(pdiId)`: `PATCH /pdis/${pdiId}/cancelar`.
- `listarPDIsPorColaborador(colaboradorId, options)`: `GET /colaboradores/${colaboradorId}/pdis`.
- `criarAcaoPDI(pdiId, payload)`: `POST /pdis/${pdiId}/acoes`.
- `atualizarAcaoPDI(pdiId, acaoId, payload)`: `PATCH /pdis/${pdiId}/acoes/${acaoId}`.
- `concluirAcaoPDI(pdiId, acaoId)`: `PATCH /pdis/${pdiId}/acoes/${acaoId}/concluir`.
- `cancelarAcaoPDI(pdiId, acaoId)`: `PATCH /pdis/${pdiId}/acoes/${acaoId}/cancelar`.

#### [NEW] [pdisFormatters.js](../../../frontend/src/features/pdis/pdisFormatters.js)
Formatadores e utilitários:
- `traduzirStatusPDI(status)`: Mapeamento de enums.
- `traduzirOrigemPDI(origem)`: Mapeamento de enums.
- `traduzirTipoAcaoPDI(tipo)`: Mapeamento de enums.
- `traduzirStatusAcaoPDI(status)`: Mapeamento de enums.
- `formatarData(data)`: Formatação simples `YYYY-MM-DD` -> `DD/MM/AAAA`.

#### [NEW] [pdisErrors.js](../../../frontend/src/features/pdis/pdisErrors.js)
Mapeador de erros HTTP:
- Converte erros HTTP 400 (VALIDATION_ERROR), 403 (FORBIDDEN) e 404 (NOT_FOUND) para mensagens legíveis.

#### [NEW] [StatusPDIBadge.jsx](../../../frontend/src/features/pdis/StatusPDIBadge.jsx)
Badges do PDI: Mapeia status para variantes de cor (`info` para ATIVO, `success` para CONCLUIDO, etc.).

#### [NEW] [StatusAcaoPDIBadge.jsx](../../../frontend/src/features/pdis/StatusAcaoPDIBadge.jsx)
Badges de Ação do PDI: Mapeia status da ação (`PENDENTE`, `CONCLUIDA`, `CANCELADA`) para variantes.

#### [NEW] [PDITable.jsx](../../../frontend/src/features/pdis/PDITable.jsx)
Tabela global de exibição de PDIs:
- Renderiza colunas: Colaborador, Título, Origem, Início, Fim, Status, Progresso (Ações Concluídas/Total).
- Link para detalhes do PDI (`/pdis/:id`).
- Recebe um mapa de colaboradores como prop para tradução de `colaborador_id` para nome.

#### [NEW] [PDIsColaboradorView.jsx](../../../frontend/src/features/pdis/PDIsColaboradorView.jsx)
Componente contextual de PDI para um colaborador específico:
- Recebe `colaboradorId`.
- Consome `listarPDIsPorColaborador(colaboradorId)` enviando `AbortSignal`.
- Renderiza tabela responsiva reutilizando `PDITable`.

#### [NEW] [PDIForm.jsx](../../../frontend/src/features/pdis/PDIForm.jsx)
Formulário dinâmico para criação ou edição de PDI:
- Campos: Título, Descrição, Data de Início, Data de Fim.
- Se for criação: permite adicionar array dinâmico de Ações iniciais.
- Define a origem como `"MANUAL"` fixo e oculto.
- Aceita prop `initialData` e `isEdit` para reaproveitamento em fluxos de edição (`PATCH /pdis/:id`).

#### [NEW] [NovoPDIPage.jsx](../../../frontend/src/pages/NovoPDIPage.jsx)
Página de criação de PDI:
- Restringe acesso a gestores.
- Carrega lista de colaboradores elegíveis com `AbortSignal`.
- Recebe `colaborador_id` opcional via query string.

#### [NEW] [EditarPDIPage.jsx](../../../frontend/src/pages/EditarPDIPage.jsx)
Página para edição de PDI (`PATCH /pdis/:id`):
- Restringe acesso a gestores.
- Carrega dados do PDI usando `buscarPDI` e os envia ao `PDIForm`.

#### [NEW] [PDIDetalhePage.jsx](../../../frontend/src/pages/PDIDetalhePage.jsx)
Página de detalhes e controle do PDI e suas Ações:
- Consome `buscarPDI(pdiId)`.
- Apresenta card geral e botões de controle (`Concluir`, `Cancelar`, `Editar PDI`).
- Exibe lista detalhada das ações do PDI.
- Permite gestores adicionarem uma nova ação de forma dinâmica (`POST /pdis/:id/acoes`).
- Permite gestores editarem ações específicas (`PATCH /pdis/:pdi_id/acoes/:id`) por meio de formulário/modal inline.
- Permite gestores concluírem ou cancelarem ações de forma individual.
- **Sincronização**: Re-executa `buscarPDI(pdiId)` após cada alteração com sucesso.

#### [NEW] [PDIsColaboradorPage.jsx](../../../frontend/src/pages/PDIsColaboradorPage.jsx)
Página de visualização contextual para colaboradores/gestores na rota `/colaboradores/:id/pdis`:
- Renderiza `PDIsColaboradorView` para o colaborador selecionado.

#### [MODIFY] [PDISPage.jsx](../../../frontend/src/pages/PDISPage.jsx)
Substituição da view estática:
- Consome `listarPDIs(options)` e `listarColaboradores(options)` com `AbortSignal` no carregamento inicial.
- Constrói o Map de `id -> nome` dos colaboradores.
- Exibe caixa de filtros locais no topo (busca textual por nome do colaborador, seletor de status e seletor de origem).
- Exibe o botão "Criar Novo PDI" para gestores.
- Renderiza a lista filtrada localmente na `PDITable`.

#### [MODIFY] [AppRoutes.jsx](../../../frontend/src/routes/AppRoutes.jsx)
Registrar rotas atualizadas do módulo:
- `/pdis` -> `PDISPage`
- `/pdis/novo` -> `NovoPDIPage`
- `/pdis/:id` -> `PDIDetalhePage`
- `/pdis/:id/editar` -> `EditarPDIPage`
- `/colaboradores/:id/pdis` -> `PDIsColaboradorPage`

#### [MODIFY] [ColaboradorDetalhe.jsx](../../../frontend/src/features/colaboradores/ColaboradorDetalhe.jsx)
- Alterar o botão desativado "Criar PDI" para apontar para `/pdis/novo?colaborador_id={colaborador.id}`.
- Alterar o botão desativado "Ver PDIs" para apontar para `/colaboradores/{colaborador.id}/pdis`.

---

## Verification Plan

### Fase 1 - Validações técnicas executadas pelo Antigravity

Executar somente validações técnicas e automatizadas de baixo consumo.

#### Frontend

```bash
cd frontend
npm run lint
npm run build
```

#### Docker

Na raiz do monorepo:

```bash
docker compose config
```

Quando necessário para validar integração técnica:

```bash
docker compose up --build -d
docker compose ps
```

Não abrir navegador automaticamente.

#### Testes automatizados

Executar apenas testes automatizados existentes e diretamente relacionados às alterações.

Registrar separadamente:

* validações aprovadas;
* validações reprovadas;
* verificações feitas apenas por inspeção;
* testes não existentes;
* testes não executados.

---

### Fase 2 - Handoff para validação humana

Após concluir as validações técnicas, utilizar a Skill:

```text
gth-manual-validation-handoff
```

A Skill deve gerar:

```text
docs/scratchpads/issue-042-manual-validation.md
```

O Scratchpad deve ser construído dinamicamente com base:

* na ISSUE #042;
* neste plano;
* nos contratos reais da API;
* nos arquivos efetivamente alterados;
* nos critérios de aceite;
* nas regras de perfil e escopo;
* nas limitações conhecidas;
* nas validações técnicas já realizadas.

O Antigravity não deve executar os cenários manuais.

---

### Cenários que devem constar no Scratchpad

A Skill deve preparar, quando aplicáveis, cenários para:

1. Listagem global de PDIs e filtros locais.
2. Criação de PDI com ação inicial.
3. Visualização do detalhe e reload.
4. Criação posterior de ação.
5. Edição de ação e persistência após reload.
6. Edição do PDI e persistência após reload.
7. Tentativa inválida de concluir PDI com ações pendentes.
8. Conclusão ou cancelamento das ações.
9. Conclusão válida do PDI.
10. Cancelamento de outro PDI ativo.
11. Visão contextual por colaborador.
12. Estado vazio.
13. Recurso inexistente com tratamento 404.
14. Bloqueio visual da rota para COLABORADOR.
15. Listagem dos próprios PDIs pelo COLABORADOR.
16. Persistência no PostgreSQL.
17. Capturas visuais essenciais.

Não usar IDs fixos como `/pdis/1`.

O Scratchpad deve possuir campos para registrar:

```text
colaborador_id
pdi_principal_id
pdi_cancelamento_id
acao_inicial_id
acao_adicional_id
```

---

### Evidências visuais

A Skill deve sugerir poucas evidências, priorizando:

* criação bem-sucedida;
* detalhe do PDI;
* estado concluído;
* visão contextual por colaborador;
* visão do perfil COLABORADOR;
* acesso negado.

Não exigir screenshot para todos os passos.

Vídeo deve ser opcional e solicitado apenas quando necessário para representar um fluxo contínuo.

O Antigravity não deve:

* abrir navegador;
* capturar screenshots;
* gravar vídeos;
* gerar imagens;
* declarar evidências inexistentes.

---

### Persistência

A Skill deve inspecionar a configuração real do Docker Compose antes de sugerir comandos do PostgreSQL.

Não presumir:

```text
gth_user
gth_db
```

Gerar o comando com o usuário e o banco realmente configurados.

A consulta deve permitir verificar:

```text
PDI criado
origem MANUAL
criado_por_id
título atualizado
status final
ações concluídas ou canceladas
```

A execução ficará sob responsabilidade do usuário.

---

### Estado após geração do Scratchpad

Depois de criar o arquivo, informar:

```text
Implementação concluída.
Validações técnicas concluídas.
Validação manual pendente.

Scratchpad:
docs/scratchpads/issue-042-manual-validation.md

Status: AGUARDANDO VALIDAÇÃO HUMANA
```

Não finalizar o walkthrough.

Não declarar a issue pronta.

Não executar commit, push, merge ou troca de branch.

---

### Processamento posterior

Depois que o usuário preencher o Scratchpad e fornecer as evidências:

1. Ler os resultados registrados.
2. Verificar os arquivos de evidência realmente existentes.
3. Consolidar o walkthrough.
4. Distinguir:

   * validado automaticamente;
   * validado manualmente pelo usuário;
   * verificado por inspeção;
   * não executado;
   * bloqueado.
5. Informar se a issue está pronta para fechamento.

Nenhum cenário pendente pode ser convertido automaticamente em aprovado.

