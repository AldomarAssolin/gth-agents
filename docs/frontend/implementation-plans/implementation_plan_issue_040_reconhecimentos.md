# Plano de Implementação - Módulo Frontend de Reconhecimentos (Issue #040)

Este documento apresenta o plano de design e implementação revisado para o módulo frontend de reconhecimentos do monorepo GTH Agents. O objetivo é permitir que colaboradores visualizem seus reconhecimentos e que líderes, RH e administradores gerenciem, criem e cancelem reconhecimentos de forma segura e contextual.

## Contratos Reais Encontrados

Após inspeção estática no backend, confirmamos os seguintes contratos e endpoints disponíveis:

| Operação | Método e URL | Perfis Autorizados | Regra de Escopo | Payload / Parâmetros | Status HTTP Sucesso | Fonte no Código |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Criar Reconhecimento** | `POST /reconhecimentos` | `ADMIN`, `RH`, `LIDER` | Admin/RH criam para todos; Líder apenas para liderados no seu setor. | `colaborador_id` (int, obrigatório), `tipo` (string, obrigatório), `descricao` (string, obrigatório), `evidencia` (string, obrigatório) | `201 Created` | [reconhecimentos_routes.py](../../../backend/interface/routes/reconhecimentos_routes.py) |
| **Listar Reconhecimentos** | `GET /reconhecimentos` | Todos (`@auth_required`) | Admin/RH: todos; Líder: apenas do setor; Colaborador: apenas os próprios. | Nenhum | `200 OK` | [reconhecimentos_routes.py](../../../backend/interface/routes/reconhecimentos_routes.py) |
| **Buscar Reconhecimento** | `GET /reconhecimentos/<int:id>` | Todos (`@auth_required`) | Visualiza apenas se tiver acesso ao colaborador. | `id` no path (Nota: Não consumido nesta versão) | `200 OK` | [reconhecimentos_routes.py](../../../backend/interface/routes/reconhecimentos_routes.py) |
| **Cancelar Reconhecimento** | `PATCH /reconhecimentos/<int:id>/cancelar` | `ADMIN`, `RH`, `LIDER` | Admin/RH cancelam todos; Líder apenas do seu setor. | `motivo_cancelamento` (string, obrigatório) | `200 OK` | [reconhecimentos_routes.py](../../../backend/interface/routes/reconhecimentos_routes.py) |
| **Listar por Colaborador** | `GET /colaboradores/<int:id>/reconhecimentos` | Todos (`@auth_required`) | Apenas se tiver acesso ao colaborador. | `id` no path | `200 OK` | [reconhecimentos_routes.py](../../../backend/interface/routes/reconhecimentos_routes.py) |
| **Listar Colaboradores** | `GET /colaboradores` | Todos (`@auth_required`) | Líder: somente do setor; Colaborador: somente a si mesmo; Admin/RH: todos. | Nenhum | `200 OK` | [colaboradores_routes.py](../../../backend/interface/routes/colaboradores_routes.py) |

## Valores Reais do Domínio

### Tipos de Reconhecimento (`TipoReconhecimento`)
Confirmamos no arquivo [tipo_reconhecimento.py](../../../backend/domain/enums/tipo_reconhecimento.py) que os valores aceitos no backend para o campo `tipo` são:
- `DESTAQUE`
- `META_ATINGIDA`
- `EVOLUCAO_TECNICA`
- `COMPORTAMENTO_POSITIVO`
- `CONCLUSAO_TREINAMENTO`
- `CONCLUSAO_PDI`
- `REDUCAO_RETRABALHO`
- `APOIO_EQUIPE`
- `POTENCIAL_LIDERANCA`
- `OUTRO`

### Representação do Status
Conforme inspecionado no [reconhecimento_model.py](../../../backend/infrastructure/database/models/reconhecimento_model.py), o status ativo/cancelado é persistido pelo booleano `ativo` (`true`/`false`). A API também retorna metadados de cancelamento quando o reconhecimento é cancelado:
- `cancelado_em` (datetime)
- `cancelado_por_id` (int)
- `motivo_cancelamento` (text)

O frontend representará isso de forma amigável em badges:
- `ativo = true` &rarr; **ATIVO**
- `ativo = false` &rarr; **CANCELADO**

---

## User Review Required

> [!IMPORTANT]
> **Resolução de Autoria:** O backend retorna apenas o `registrado_por_id` e `cancelado_por_id` (IDs do modelo de Usuário). Como `usuario.id` **NÃO** possui correspondência direta ou garantida com `colaborador.id` (são entidades independentes), não tentaremos carregar dados de colaboradores para resolver esses nomes de autoria.
>
> Para diferenciar claramente os agentes no card de reconhecimento, o frontend aplicará a seguinte regra:
> * Se `user.id === registrado_por_id` &rarr; **“Registrado por você”**
> * Se `user.id !== registrado_por_id` &rarr; **“Registrado pelo usuário #ID”**
> * Se `user.id === cancelado_por_id` &rarr; **“Cancelado por você”**
> * Se `user.id !== cancelado_por_id` &rarr; **“Cancelado pelo usuário #ID”**
>
> **Simplificação de Serviços:** O endpoint `GET /reconhecimentos/<id>` existe no backend, mas não será consumido no frontend nesta versão. Os endpoints de listagem (`GET /reconhecimentos` e `GET /colaboradores/<id>/reconhecimentos`) já fornecem todos os campos necessários (incluindo evidência, motivo e datas de auditoria), eliminando a necessidade de chamadas extras de detalhe.

---

## Proposed Changes

Propomos a criação do módulo `reconhecimentos` estruturado por feature no frontend, a vinculação das novas páginas nas rotas globais e a inserção de atalhos na tela de detalhes do colaborador.

### Módulo Frontend - Reconhecimentos

#### [NEW] [reconhecimentosService.js](../../../frontend/src/features/reconhecimentos/reconhecimentosService.js)
Serviço Axios responsável pela comunicação com a API.
- Reutilizar a instância global `api` importada de `../../services/api`.
- Métodos expostos (com suporte a `AbortSignal` nas leituras):
  - `listarReconhecimentos(options = {})`
  - `criarReconhecimento(payload, options = {})`
  - `cancelarReconhecimento(id, motivo, options = {})`
  - `listarReconhecimentosPorColaborador(colaboradorId, options = {})`

#### [NEW] [reconhecimentosErrors.js](../../../frontend/src/features/reconhecimentos/reconhecimentosErrors.js)
Função de tradução de erros de API baseada na resposta da requisição.
- Retorna mensagens específicas de validação de negócios (ex: *"A descrição é obrigatória"*, *"Motivo de cancelamento inválido"*).

#### [NEW] [reconhecimentosFormatters.js](../../../frontend/src/features/reconhecimentos/reconhecimentosFormatters.js)
Formatadores auxiliares para exibição de dados:
- `formatarData(isoString)`: Retorna data formatada no padrão brasileiro (`DD/MM/AAAA`).
- `traduzirTipoReconhecimento(tipo)`: Mapeia enums em strings legíveis (ex: `APOIO_EQUIPE` &rarr; `"Apoio da Equipe"`).

#### [NEW] [TipoReconhecimentoBadge.jsx](../../../frontend/src/features/reconhecimentos/TipoReconhecimentoBadge.jsx)
Componente que renderiza a badge de tipo de reconhecimento usando variantes de cores consistentes do componente global `Badge`:
- Variantes: `info` (DESTAQUE, EVOLUCAO_TECNICA), `success` (APOIO_EQUIPE, META_ATINGIDA), `warning` (POTENCIAL_LIDERANCA), `secondary` (OUTRO).

#### [NEW] [StatusReconhecimentoBadge.jsx](../../../frontend/src/features/reconhecimentos/StatusReconhecimentoBadge.jsx)
Componente de badge para o status ativo/cancelado:
- `ativo === true` &rarr; `success` (Ativo)
- `ativo === false` &rarr; `danger` (Cancelado)

#### [NEW] [ReconhecimentoForm.jsx](../../../frontend/src/features/reconhecimentos/ReconhecimentoForm.jsx)
Formulário controlado de criação de reconhecimentos:
- Inputs: Colaborador (Select), Tipo de Reconhecimento (Select), Descrição (Textarea) e Evidência (Textarea).
- Bloqueio e pré-seleção do colaborador via prop `lockColaborador` se o ID vier validado da página.
- Validação local básica e desabilitação de botões durante envio.
- Preservação do estado preenchido após falhas de submissão do backend.

#### [NEW] [ReconhecimentoCard.jsx](../../../frontend/src/features/reconhecimentos/ReconhecimentoCard.jsx)
Componente para renderizar um card de reconhecimento no mural:
- Apresenta: Autor, Colaborador, Tipo, Data, Descrição, Evidência e Status.
- Exibe bloco de auditoria se estiver cancelado (motivo, data, autor diferenciado).
- Exibe botão "Cancelar Reconhecimento" para gestores autorizados se o card estiver ativo.

#### [NEW] [CancelarReconhecimentoDialog.jsx](../../../frontend/src/features/reconhecimentos/CancelarReconhecimentoDialog.jsx)
Modal de confirmação de cancelamento que exige o motivo:
- Campo de `<textarea>` para preenchimento obrigatório do motivo.
- Bloqueia as ações de fechar e confirmar durante a submissão.

#### [NEW] [ReconhecimentosList.jsx](../../../frontend/src/features/reconhecimentos/ReconhecimentosList.jsx)
Componente predominantemente apresentacional que:
- Renderiza a listagem de cards.
- Oferece filtros locais por colaborador, tipo e status.
- Dispara o callback `onCancelar(reconhecimento)` quando o usuário clica para iniciar o fluxo de cancelamento.

---

### Páginas do Sistema

#### [MODIFY] [ReconhecimentosPage.jsx](../../../frontend/src/pages/ReconhecimentosPage.jsx)
Mural dinâmico completo:
- Gerencia o estado de carregamento de reconhecimentos e colaboradores.
- Gerencia estados separados de erro: `loadError` e `cancelError`.
- Gerencia estado de submissão de cancelamento: `isCancelling`.
- Realiza a chamada HTTP para buscar reconhecimentos e disparar o cancelamento.
- **Resiliência a Falhas:** Caso o cancelamento falhe (dispare um erro), define `cancelError` para exibir um aviso amigável, mas **não desmonta nem limpa a listagem de reconhecimentos**.

#### [NEW] [NovoReconhecimentoPage.jsx](../../../frontend/src/pages/NovoReconhecimentoPage.jsx)
Página para registro de um novo reconhecimento:
- Proteção visual baseada no perfil (somente `ADMIN`, `RH`, `LIDER`).
- Carrega a lista de colaboradores acessíveis com `AbortController`.
- **Tratamento de Query String:** O parâmetro `colaborador_id` extraído das query strings é validado **somente após** carregar a lista de colaboradores acessíveis.
  * Se o ID não constar na lista (inválido ou fora do escopo do líder), o campo de seleção permanecerá destravado e com valor padrão vazio ("Selecione...").
  * Exibirá um aviso contextual em tela alertando o usuário: *"O colaborador solicitado via parâmetro não foi encontrado ou está fora do seu escopo de acesso."*
- Gerencia estados separados: `loadError`, `submitError`, `isSubmitting`.
- Preserva dados do formulário caso a API retorne erro.

#### [NEW] [ReconhecimentosColaboradorPage.jsx](../../../frontend/src/pages/ReconhecimentosColaboradorPage.jsx)
Página contextual de reconhecimentos de um colaborador específico:
- Acessível em `/colaboradores/:id/reconhecimentos`.
- Carrega as informações do colaborador e seus reconhecimentos vinculados.
- Gerencia localmente os estados de erro (`loadError`, `cancelError`) e loadings (`isCancelling`).

---

### Atalhos no Perfil do Colaborador

#### [MODIFY] [ColaboradorDetalhe.jsx](../../../frontend/src/features/colaboradores/ColaboradorDetalhe.jsx)
Modificar o bloco de "Ações e Atalhos" para incluir integrações reais de reconhecimentos:
1. Substituir o atalho desabilitado *"Registrar Reconhecimento (Em breve)"* por um link para `/reconhecimentos/novo?colaborador_id=${colaborador.id}` (habilitado apenas para `ADMIN`, `RH`, `LIDER`; usuários comuns visualizam desabilitado ou com aviso).
2. Adicionar o atalho *"Ver Reconhecimentos"* (Link para `/colaboradores/${colaborador.id}/reconhecimentos`) disponível para todos os perfis autorizados.

---

### Rotas e Navegação

#### [MODIFY] [AppRoutes.jsx](../../../frontend/src/routes/AppRoutes.jsx)
Adicionar as novas rotas dentro do escopo protegido (`PrivateRoute` e `AppLayout`):
- `/reconhecimentos` &rarr; `ReconhecimentosPage`
- `/reconhecimentos/novo` &rarr; `NovoReconhecimentoPage`
- `/colaboradores/:id/reconhecimentos` &rarr; `ReconhecimentosColaboradorPage`

---

## Regras de Acesso e Controle Visual

1. **Página de Criação e Ação de Cancelamento**: Bloqueio local contra perfil `COLABORADOR` (exibição de `ErrorMessage` com aviso de acesso negado).
2. **Ocultação de Ações**: Ocultar botões de criação e cancelamento para usuários sem permissões gestoras.
3. **Escopo de Dados**: O backend aplica os filtros de escopo automaticamente com base na autenticação do usuário.

---

## Estratégia de Erros e Estados da Interface

A aplicação controlará os estados individualmente para manter a interface reativa e protegida contra reinicializações indesejadas:
- `loadError`: Define erros ao falhar em carregar listas de dados iniciais.
- `submitError`: Exibe falhas de cadastro na parte superior do formulário, preservando os campos preenchidos.
- `cancelError`: Exibe erros no cancelamento em banners temporários sem apagar a lista de reconhecimentos.
- `isSubmitting` / `isCancelling`: Controla desabilitação de botões e exibe loadings parciais.

---

## Plano de Validação

### Validação Técnica (Antigravity)
Após a codificação, executaremos exatamente a seguinte sequência de comandos para garantir a conformidade técnica:
```bash
# Lint e Build do frontend no escopo correto do monorepo
(
  cd frontend
  npm run lint
  npm run build
)

# Validação do Compose Docker
docker compose config

# Testes automatizados de integração e regressão no container do backend
docker compose exec api \
  pytest tests/test_reconhecimentos.py

# Verificação estática de diffs no repositório
git diff --check
```
*Nota: Caso os containers do Docker compose não estejam previamente iniciados na execução técnica, o comando de teste será adaptado para:*
`docker compose run --rm api pytest tests/test_reconhecimentos.py`

### Roteiro de Validação Manual
Após a validação técnica, usaremos o fluxo de handoff para criar o arquivo de evidências em `docs/scratchpads/issue-040-manual-validation.md` documentando detalhadamente cada teste utilizando o seguinte formato padrão para cada cenário:
```markdown
### Cenário XX: [Título do Cenário]
- **Perfil**: [Perfil de Usuário Utilizado (ADMIN/RH/LIDER/COLABORADOR)]
- **Pré-condições**: [Ambiente necessário, estados dos dados]
- **IDs utilizados**: [IDs de colaboradores, usuários ou reconhecimentos reais testados]
- **Passos**:
  1. Passo 1...
  2. Passo 2...
- **Resultado esperado**: [O que deve acontecer]
- **Resultado observado**: [O que de fato aconteceu]
- **Status**: [APROVADO / REJEITADO]
- **Evidências**: [Links de imagens/vídeos ou trechos de logs no terminal]
- **Observações**: [Notas complementares]
```

Documentaremos os seguintes 20 cenários específicos de teste:

1. **Listagem Global (Mural)**: Acessar `/reconhecimentos` como administrador e validar a listagem geral de reconhecimentos com seus respectivos badges.
2. **Listagem Contextual**: Acessar `/colaboradores/:id/reconhecimentos` e validar que apenas os reconhecimentos do colaborador correspondente aparecem.
3. **Criação**: Registrar com sucesso um novo reconhecimento a partir de `/reconhecimentos/novo`.
4. **Query String Válida**: Navegar para `/reconhecimentos/novo?colaborador_id=<ID_VALIDO>` e certificar que o colaborador correspondente é pré-selecionado e o campo permanece bloqueado.
5. **Query String Inválida**: Acessar `/reconhecimentos/novo?colaborador_id=9999` (id inválido ou fora do escopo de liderança do usuário) e garantir que o select não é pré-selecionado, permanece desbloqueado e exibe o aviso contextual: *"O colaborador solicitado via parâmetro não foi encontrado ou está fora do seu escopo de acesso."*
6. **Campos Obrigatórios**: Tentar submeter o formulário de criação com campos vazios (tipo, descrição, evidência) e garantir que a validação de formulário do navegador/local impede a submissão.
7. **Preservação do Formulário**: Simular indisponibilidade temporária do backend (desligando o container da API ou gerando falha de rede física) e submeter o formulário de criação. Verificar que a mensagem de `submitError` aparece, mas os dados preenchidos nos campos são integralmente preservados.
8. **Prevenção de Envio Duplicado**: Clicar repetidamente de forma rápida no salvar da criação e checar se o estado de `isSubmitting` desabilita o botão após a primeira requisição.
9. **Cancelamento com Motivo**: Cancelar um reconhecimento ativo preenchendo um motivo válido e checar se o card atualiza para o estado cancelado exibindo os dados de cancelamento (motivo, data, autor como "Cancelado por você").
10. **Motivo Vazio no Cancelamento**: Tentar confirmar o cancelamento no modal com o campo motivo em branco e verificar que a validação local bloqueia o envio.
11. **Erro de Cancelamento (Falha de Rede)**: Simular falha de rede física ou perda de conexão ao enviar o cancelamento e garantir que a interface exibe a mensagem amigável em `cancelError`, mas a listagem do mural continua visível e intacta.
12. **Erro de Cancelamento (Recurso Inexistente)**: Tentar enviar um PATCH de cancelamento diretamente via curl/cliente HTTP para um ID de reconhecimento inexistente, verificando que o backend retorna HTTP 404 e a interface trata a falha sem desmontar a página.
13. **Cancelamento Duplicado (Proteção Visual)**: Validar que no card de um reconhecimento já cancelado (`ativo = false`), o botão de ação "Cancelar Reconhecimento" é completamente ocultado do HTML.
14. **Cancelamento Duplicado (Regra Backend)**: Tentar enviar um PATCH de cancelamento via chamada direta de API para um ID de reconhecimento que já foi cancelado anteriormente, verificando que o backend rejeita com erro apropriado (HTTP 400 Bad Request) e que a interface não entra em crash.
15. **Estado Vazio (Sem registros)**: Acessar a listagem global ou contextual com um colaborador que reconhecidamente não possua registros no banco e certificar a correta renderização do componente `<EmptyState />`.
16. **Estado Vazio (Filtro Sem Correspondência)**: Aplicar filtros de busca no mural que não possuam registros correspondentes e validar que o componente exibe feedback claro de que não há resultados para a busca selecionada, distinguindo-se do vazio real do banco.
17. **Proteção Visual da Rota**: Logar como `COLABORADOR` e certificar que não são renderizados links de criação e que a rota `/reconhecimentos/novo` o redireciona ou exibe aviso visual de "Acesso Negado".
18. **Resposta HTTP 403 do Backend**: Forçar submissão direta do endpoint de criação utilizando credenciais de `COLABORADOR` e certificar que o backend rejeita com HTTP 403.
19. **Tratamento de Erro de Submissão na Interface**: Validar que ao receber um erro 403 ou 400 do backend na submissão, a página captura e exibe adequadamente no `submitError` sem crashar a aplicação.
20. **Responsividade**: Validar o comportamento do mural, botões, atalhos e modais de cancelamento em layout mobile e desktop.

Após o registro técnico de todos os resultados no Scratchpad, o documento será encerrado com a linha final:
`Status: AGUARDANDO VALIDAÇÃO HUMANA`
