# Implementar ISSUE #024 - Módulo Frontend de Metas

Este plano descreve a implementação do módulo de metas no frontend do GTH Agents, utilizando os contratos reais fornecidos pelo backend para criar, listar por colaborador, filtrar e validar as metas dos colaboradores.

---

## Contratos Reais do Backend Identificados

Após a inspeção do backend, foram mapeados os seguintes endpoints e regras de negócio:

1. **Endpoint de Criação de Meta**:
   - **Endpoint**: `POST /metas`
   - **Permissões**: Restrito às roles `ADMIN`, `RH` e `LIDER` (através do middleware `@roles_required("ADMIN", "RH", "LIDER")`).
   - **Payload Esperado (JSON)**:
     ```json
     {
       "colaborador_id": 1,
       "criado_por_id": 2,
       "titulo": "Melhorar comunicação preventiva",
       "descricao": "Registrar antecipadamente riscos ou dificuldades.",
       "indicador": "2 registros preventivos por semana",
       "prazo": "2026-07-30",
       "prioridade": "ALTA"
     }
     ```
   - **Campos Obrigatórios**: `colaborador_id`, `criado_por_id`, `titulo`, `descricao`, `prazo`.
   - **Valores Permitidos para Prioridade** (Enum `PrioridadeMeta`):
     - `BAIXA`
     - `MEDIA`
     - `ALTA`
     - `CRITICA`
   - **Resposta de Sucesso (HTTP 201 Created)**: Retorna a entidade `Meta` criada, contendo os campos preenchidos, além de `id`, `status` (inicializado como `PENDENTE`), `origem` (definido como `"MANUAL"`), `criado_em` e `atualizado_em`.

2. **Endpoint de Listagem de Metas por Colaborador**:
   - **Endpoint**: `GET /colaboradores/<int:id>/metas`
   - **Permissões**: Exige que o usuário tenha acesso de leitura ao colaborador (Admin/RH possuem acesso global; Líderes possuem acesso aos colaboradores de seu setor; Colaboradores possuem acesso apenas às suas próprias metas).
   - **Resposta de Sucesso (HTTP 200 OK)**:
     ```json
     [
       {
         "id": 1,
         "colaborador_id": 1,
         "criado_por_id": 2,
         "titulo": "Melhorar comunicação preventiva",
         "descricao": "Registrar antecipadamente riscos ou dificuldades.",
         "indicador": "2 registros preventivos por semana",
         "prazo": "2026-07-30",
         "prioridade": "ALTA",
         "status": "PENDENTE",
         "origem": "MANUAL",
         "criado_em": "2026-06-07T14:56:32",
         "atualizado_em": "2026-06-07T14:56:32"
       }
     ]
     ```

3. **Existência ou Ausência de `GET /metas`**:
   - **Ausente**: Não existe um endpoint de listagem global `GET /metas` no backend.
   - **Comportamento**: A rota geral `/metas` do frontend funcionará como página inicial informativa do módulo, fornecendo um seletor de colaboradores para os perfis com permissão (Admin, RH, Líder) para que possam consultar metas individuais e um atalho para criar uma nova meta. Para perfis do tipo `COLABORADOR`, a página carregará diretamente suas próprias metas e omitirá a seleção de terceiros.

4. **Regras de Autenticação/Autorização e Riscos Conhecidos**:
   - O criador da meta (`criado_por_id`) será mapeado a partir da propriedade `id` do usuário autenticado obtido no `AuthContext` (`user.id`).
   - A listagem de metas do perfil `COLABORADOR` utilizará a propriedade `user.colaborador_id` para carregar as metas próprias.
   - **Não confundir**: `user.id` (ID do usuário) não se confunde com `user.colaborador_id` (ID do colaborador vinculado ao usuário).
   - > [!WARNING]
     > **Risco Conhecido**: O backend recebe `criado_por_id` pelo payload sem validar explicitamente no interceptor/caso de uso sua correspondência de identidade com o usuário autenticado da requisição. Para mitigar isso, o frontend preencherá esse campo internamente de forma automática e imutável através de `user.id`, sem exibir inputs de edição manual.
   - Para usuários com o perfil `COLABORADOR`, caso `user.colaborador_id` esteja ausente ou seja inválido (ex: nulo ou indefinido), a API não será chamada e o frontend exibirá uma tela de aviso informando que o vínculo de colaborador não está configurado para o usuário atual.
   - A rota de criação `/metas/nova` será protegida visualmente no frontend para impedir o acesso de usuários com perfil `COLABORADOR`. Caso um colaborador tente acessar diretamente via URL, uma tela de erro amigável de permissão (403) será exibida.

---

## User Review Required

> [!IMPORTANT]
> O backend não disponibiliza uma rota `GET /metas` global. Sendo assim, a página `/metas` atuará como landing page do módulo com busca/seleção de colaborador (para Admin, RH e Líder) e visualização direta das próprias metas para o perfil `COLABORADOR`.

> [!WARNING]
> Usuários com perfil `COLABORADOR` não possuem permissão no backend para criar metas (retornará HTTP 403). Bloquearemos o acesso a `/metas/nova` no frontend para este perfil e exibiremos um aviso apropriado caso tentem navegar até ele diretamente.

---

## Open Questions

*Nenhuma questão em aberto encontrada.*

---

## Proposed Changes

### Módulo de Metas (Frontend)

---

#### [NEW] [metasService.js](../../../frontend/src/features/metas/metasService.js)
Serviço para centralizar a comunicação com a API:
- `criarMeta(payload)`: envia dados para `POST /metas`.
- `listarMetasPorColaborador(colaboradorId, options)`: recupera as metas de um colaborador específico em `GET /colaboradores/${colaboradorId}/metas`.

#### [NEW] [metasFormatters.js](../../../frontend/src/features/metas/metasFormatters.js)
Utilitários de formatação do módulo:
- `formatarData(data)`: trata strings de datas simples (`YYYY-MM-DD`) e datetimes ISO sem sofrer deslocamentos indesejados devido ao fuso horário, retornando `DD/MM/AAAA`.

#### [NEW] [metasErrors.js](../../../frontend/src/features/metas/metasErrors.js)
Utilitário para tradução de erros retornados pela API:
- Trata códigos HTTP 400/422 (Dados inválidos), 403 (Permissão negada), 404 (Não encontrado) e falhas de rede. Preserva o interceptor global e não trata o erro 401 localmente.

#### [NEW] [StatusMetaBadge.jsx](../../../frontend/src/features/metas/StatusMetaBadge.jsx)
Componente reutilizável para exibição do status da meta:
- Mapeia os status do backend (`PENDENTE`, `EM_ANDAMENTO`, `CONCLUIDA`, `ATRASADA`, `CANCELADA`) para rótulos e cores do componente `Badge` do sistema. Possui fallback seguro ("Status não informado" ou valor genérico formatado) para status ausentes ou desconhecidos.

#### [NEW] [PrioridadeMetaBadge.jsx](../../../frontend/src/features/metas/PrioridadeMetaBadge.jsx)
Componente reutilizável para exibição da prioridade da meta:
- Mapeia as prioridades do backend (`BAIXA`, `MEDIA`, `ALTA`, `CRITICA`) para rótulos legíveis e variantes visuais do `Badge`. Possui fallback seguro ("Não informada" ou valor genérico formatado) para prioridades ausentes ou desconhecidas.

#### [NEW] [MetasTable.jsx](../../../frontend/src/features/metas/MetasTable.jsx)
Tabela responsiva que renderiza a lista de metas recebida por props, exibindo: título, descrição/indicador, prazo formatado, prioridade, status e origem.

#### [NEW] [MetasColaboradorView.jsx](../../../frontend/src/features/metas/MetasColaboradorView.jsx)
Visualização reutilizável para listagem e filtragem de metas por colaborador, evitando duplicação:
- Aceita `colaboradorId` via props.
- Antes de realizar a chamada à API, valida se o identificador `colaboradorId` é um inteiro maior que zero.
- Gerencia o carregamento de metas (`listarMetasPorColaborador`) passando `AbortController.signal`.
- Gerencia os estados de loading, erro e lista vazia.
- Apresenta o filtro simples por status (local) e renderiza a `MetasTable`.

#### [NEW] [MetaForm.jsx](../../../frontend/src/features/metas/MetaForm.jsx)
Formulário de preenchimento para a criação de uma nova meta:
- Inclui seletor de colaboradores (se não estiver pré-selecionado), inputs para título, descrição, indicador, prazo (data) e prioridade.
- Valida o `colaborador_id` selecionado contra a lista de colaboradores acessíveis (inteiro maior que zero e presente no array de opções carregadas).
- Realiza validações detalhadas no frontend (campos obrigatórios com `.trim()`).

#### [NEW] [NovaMetaPage.jsx](../../../frontend/src/pages/NovaMetaPage.jsx)
Página que controla a criação de metas:
- Valida permissão do usuário de acordo com a validação direta baseada no perfil na própria página (`["ADMIN", "RH", "LIDER"].includes(user?.perfil)`).
- Carrega os colaboradores elegíveis usando `AbortController.signal`.
- Lida com a pré-seleção a partir da query string `?colaborador_id=X`, validando se `colaborador_id` é um inteiro maior que zero e se corresponde a um colaborador presente na lista acessível.
- Exibe feedback visual de sucesso diretamente na página contendo os detalhes da meta criada (utilizando um card inline) e opções de navegação.

#### [NEW] [MetasColaboradorPage.jsx](../../../frontend/src/pages/MetasColaboradorPage.jsx)
Página para visualização detalhada das metas de um colaborador específico:
- Valida se o ID extraído dos parâmetros de rota é um inteiro maior que zero.
- Reutiliza o componente `MetasColaboradorView` para renderizar as metas.

#### [MODIFY] [MetasPage.jsx](../../../frontend/src/pages/MetasPage.jsx)
Substituir o esqueleto existente pela tela informativa e interativa:
- Se o usuário for `COLABORADOR`, renderiza diretamente `MetasColaboradorView` com `colaboradorId={user.colaborador_id}` (bloqueando a chamada e exibindo tela de erro se `user.colaborador_id` estiver ausente).
- Caso contrário, exibe o seletor de colaboradores.
- Persiste a seleção do colaborador na query string `/metas?colaborador_id=X`.
- Valida o `colaborador_id` da query string contra a lista de colaboradores retornada pela API antes de renderizar a visualização.
- Quando um colaborador for selecionado, exibe as metas dele reutilizando `MetasColaboradorView`.

#### [MODIFY] [AppRoutes.jsx](../../../frontend/src/routes/AppRoutes.jsx)
Registrar as novas rotas do módulo:
- `/metas/nova` -> `NovaMetaPage`
- `/colaboradores/:id/metas` -> `MetasColaboradorPage`

#### [MODIFY] [ColaboradorDetalhe.jsx](../../../frontend/src/features/colaboradores/ColaboradorDetalhe.jsx)
- Ativar o botão "Criar Meta (Em breve)" transformando-o em um link funcional para `/metas/nova?colaborador_id={id}` com base no perfil do usuário autenticado.
- Adicionar botão "Ver Metas" apontando para `/colaboradores/{id}/metas`.

---

## Verification Plan

### Automated Tests
- Executar linting estático no frontend:
  ```bash
  cd frontend && npm run lint && cd ..
  ```
- Validar build de produção do frontend:
  ```bash
  cd frontend && npm run build && cd ..
  ```

### Manual/Container Verification
1. **Verificação de Containers e Conectividade**:
   - Iniciar os serviços usando a flag de build e verificar status:
     ```bash
     docker compose config
     docker compose up --build -d
     docker compose ps
     ```
   - Validar endpoints e conexões da API:
     ```bash
     curl -i http://localhost:5000/health
     curl -I http://localhost:5173
     ```
2. **Cenário 1 - Landing Page e Seleção (Líder/RH/Admin)**:
   - Fazer login como `admin@empresa.com`.
   - Navegar até `/metas`.
   - Selecionar um colaborador no seletor, verificar se a lista de metas é carregada.
   - Verificar se a query string `/metas?colaborador_id=X` foi atualizada e se o estado é mantido ao recarregar a página.
   - Testar o filtro simples por status (TODOS, PENDENTE, etc.).
3. **Cenário 2 - Landing Page para Colaborador**:
   - Fazer login como colaborador comum.
   - Navegar até `/metas`.
   - Verificar que o seletor de colaboradores fica oculto e a lista carrega diretamente as metas dele.
4. **Cenário 3 - Criação de Meta**:
   - Navegar até `/metas/nova?colaborador_id=X` (ou através de atalho no ColaboradorDetalhe).
   - Preencher campos válidos e submeter.
   - Verificar status HTTP 201 no console e exibição dos dados persistidos na tela de sucesso.
   - Confirmar persistência diretamente no banco de dados do container PostgreSQL:
     ```sql
     SELECT id, colaborador_id, criado_por_id, titulo, descricao, indicador, prazo, prioridade, status, origem FROM metas ORDER BY id DESC LIMIT 1;
     ```
5. **Cenário 4 - Validações e Erros**:
   - Submeter o formulário de metas vazio e checar se as validações de input aparecem.
   - Tentar acessar `/metas/nova` como perfil `COLABORADOR` e verificar exibição da mensagem de acesso negado.
