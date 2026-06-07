# Walkthrough - ISSUE #023 - Módulo de Avaliações (Frontend)

Este documento registra a implementação do Módulo de Avaliações de Desempenho no frontend do GTH Agents, detalhando as modificações efetuadas, decisões técnicas e a verificação do fluxo ponta a ponta.

---

## 1. Alterações Realizadas

### Arquivos Criados
* **[avaliacoesService.js](../../../frontend/src/features/avaliacoes/avaliacoesService.js)**: Serviço de API que encapsula as requisições de criação de avaliação (`POST /avaliacoes`) e listagem de competências (`GET /competencias`).
* **[avaliacaoUtils.js](../../../frontend/src/features/avaliacoes/avaliacaoUtils.js)**: Funções utilitárias para tradução amigável dos enums de tipo de avaliação (`formatTipo`), classificação de talento (`formatClassificacao`) e tipos de competências (`formatTipoCompetencia`).
* **[TipoAvaliacaoSelect.jsx](../../../frontend/src/features/avaliacoes/TipoAvaliacaoSelect.jsx)**: Componente Dropdown para escolha dos tipos de avaliação com rótulos amigáveis.
* **[ItemAvaliacaoForm.jsx](../../../frontend/src/features/avaliacoes/ItemAvaliacaoForm.jsx)**: Componente do formulário para cada item de competência individual, contendo seleção de inclusão (checkbox), nota de 1 a 5 e comentários específicos.
* **[ResultadoAvaliacao.jsx](../../../frontend/src/features/avaliacoes/ResultadoAvaliacao.jsx)**: Componente responsável por apresentar o resultado retornado pela API, incluindo médias por tipo de competência, média geral, classificação de talento, níveis, pontos fortes, pontos de melhoria e recomendações de desenvolvimento.
* **[AvaliacaoForm.jsx](../../../frontend/src/features/avaliacoes/AvaliacaoForm.jsx)**: Formulário unificado de preenchimento agrupando as competências ativas por tipo com suporte a validações locais robustas.
* **[NovaAvaliacaoPage.jsx](../../../frontend/src/pages/NovaAvaliacaoPage.jsx)**: Página protegida para preenchimento de nova avaliação, com carregamento paralelo de dados, tratamento de query parameters (`colaborador_id`), controle de abort de requisições e exibição condicional do resultado.

### Arquivos Modificados
* **[AvaliacoesPage.jsx](../../../frontend/src/pages/AvaliacoesPage.jsx)**: Atualizado para atuar como landing page informativa exibindo atalhos de permissão e mensagem clara sobre a indisponibilidade de listagem geral no backend.
* **[AppRoutes.jsx](../../../frontend/src/routes/AppRoutes.jsx)**: Adicionada a nova rota `/avaliacoes/nova` no grupo de rotas privadas e sob o layout de aplicação principal.
* **[ColaboradorDetalhe.jsx](../../../frontend/src/features/colaboradores/ColaboradorDetalhe.jsx)**: Substituído o botão desabilitado pelo link ativo para iniciar a avaliação do colaborador selecionado com query parameter.

---

## 2. Decisões Técnicas

### Preservação de médias com valor zero
A renderização utiliza o operador `??` em vez de `||`. Isso evita que valores válidos como `0.0`, retornados para categorias de competências não avaliadas, sejam interpretados como ausência de dado.

Exemplo:
```javascript
const media = resultado.media_tecnica ?? "Não avaliado";
```

### Controle de carregamento e nova tentativa
A página utiliza um estado de controle para disparar novas tentativas de carregamento dos dados. A lógica assíncrona foi isolada dentro do `useEffect`, evitando atualizações de estado no corpo síncrono do efeito e mantendo conformidade com a regra `react-hooks/set-state-in-effect`.

### Ausência de listagem geral de avaliações
O backend não disponibiliza atualmente o endpoint:
```http
GET /avaliacoes
```
Por esse motivo, a rota `/avaliacoes` foi implementada como página inicial informativa do módulo, oferecendo acesso à criação de uma nova avaliação. Nenhuma listagem simulada ou conjunto de dados fictício foi criado.

### Controle de acesso
A criação de avaliações está disponível para:
- `ADMIN`;
- `RH`;
- `LIDER`.

O perfil `COLABORADOR` não pode acessar o formulário de avaliação de terceiros nesta versão. A proteção visual do frontend não substitui a autorização realizada pelo backend.

---

## 3. Contratos da API utilizados

### Listagem de colaboradores
```http
GET /colaboradores
Authorization: Bearer <token>
```
* O retorno respeita o escopo do usuário autenticado (Líderes visualizam apenas colaboradores do próprio setor; RH/ADMIN visualizam todos).

### Listagem de competências
```http
GET /competencias
Authorization: Bearer <token>
```
* Retorna a lista de competências. As competências inativas são filtradas no frontend utilizando a propriedade `ativo` (`comp.ativo !== false`).

### Criação da avaliação
```http
POST /avaliacoes
Authorization: Bearer <token>
Content-Type: application/json
```
**Payload enviado:**
```json
{
  "colaborador_id": 1,
  "avaliador_id": 1,
  "tipo": "AVALIACAO_LIDER",
  "observacao_geral": "Este colaborador demonstrou excelente foco no cliente e resolveu problemas complexos com proatividade.",
  "itens": [
    {
      "competencia_id": 1,
      "nota": 4,
      "comentario": "Demonstra excelente capacidade analica e de diagnostico."
    }
  ]
}
```
* O identificador do avaliador foi obtido a partir do usuário autenticado armazenado no contexto de autenticação.

### Resposta da criação
```json
{
  "avaliacao": {
    "id": 1,
    "colaborador_id": 1,
    "avaliador_id": 1,
    "tipo": "AVALIACAO_LIDER",
    "observacao_geral": "Este colaborador demonstrou excelente foco no cliente e resolveu problemas complexos com proatividade.",
    "status": "CONCLUIDA",
    "data_avaliacao": "2026-06-07T15:41:43.909724+00",
    "criado_em": "2026-06-07T15:41:43.909730+00"
  },
  "perfil_talento": {
    "id": 1,
    "colaborador_id": 1,
    "classificacao": "ESPECIALISTA_TECNICO",
    "resumo": "Perfil classificado como ESPECIALISTA_TECNICO. Media tecnica: 4.0, media comportamental: 0.0, media de lideranca: 0.0.",
    "nivel_tecnico": "ALTO",
    "nivel_comportamental": "NAO_AVALIADO",
    "potencial_lideranca": "NAO_AVALIADO",
    "pontos_fortes": [
      "Boa competência técnica."
    ],
    "pontos_melhoria": [],
    "recomendacoes": [
      "Utilizar como referência técnica.",
      "Desenvolver comunicação, influência e apoio a colegas."
    ],
    "origem": "REGRA_DOMINIO",
    "criado_em": "2026-06-07T15:41:43.924333+00"
  },
  "resultado_competencias": {
    "media_tecnica": 4.0,
    "media_comportamental": 0.0,
    "media_lideranca": 0.0,
    "media_organizacional": 0.0,
    "media_geral": 4.0
  }
}
```

---

## 4. Verificação e Testes

### Linter
Comando executado:
```bash
npm run lint
```
Resultado:
* status: sucesso;
* exit code: 0;
* erros: 0;
* avisos: 0.

### Build de produção
Comando executado:
```bash
npm run build
```
Resultado:
* status: sucesso;
* exit code: 0;
* versão do Vite: `8.0.14`;
* módulos transformados: `145`;
* build gerado em `dist/`.

### Validação do Docker Compose
Foram executados na raiz do monorepo:
```bash
docker compose config
docker compose up --build -d
```
Verificações confirmadas:
* PostgreSQL iniciado
* API Flask iniciada
* frontend React/Vite iniciado
* `GET /health` retornando HTTP 200
* frontend acessível em `http://localhost:5173`

---

## 5. Teste de Integração

### Fluxo ponta a ponta
1. Foi realizado login com um usuário `ADMIN` previamente cadastrado no ambiente local.
2. A rota `/avaliacoes/nova` foi acessada.
3. Um colaborador disponível no escopo do usuário foi selecionado.
4. O tipo `AVALIACAO_LIDER` foi selecionado.
5. Uma competência ativa foi incluída.
6. Foi atribuída nota entre 1 e 5.
7. Foram registrados comentário específico e observação geral.
8. O formulário foi enviado.
9. A API respondeu com HTTP `201 Created`.
10. A interface exibiu o resultado retornado.

---

## 6. Evidência do Banco de Dados

A persistência correta dos dados no banco foi validada através das seguintes consultas no container Postgres:

```sql
SELECT
    id,
    colaborador_id,
    avaliador_id,
    tipo,
    status,
    observacao_geral,
    data_avaliacao
FROM avaliacoes
WHERE id = 1;
```
**Resultado:**
```text
 id | colaborador_id | avaliador_id |      tipo       |  status   |                                            observacao_geral                                            |        data_avaliacao         
----+----------------+--------------+-----------------+-----------+--------------------------------------------------------------------------------------------------------+-------------------------------
  1 |              1 |            1 | AVALIACAO_LIDER | CONCLUIDA | Este colaborador demonstrou excelente foco no cliente e resolveu problemas complexos com proatividade. | 2026-06-07 15:41:43.909724+00
```

```sql
SELECT
    id,
    avaliacao_id,
    competencia_id,
    nota,
    comentario
FROM itens_avaliacao
WHERE avaliacao_id = 1;
```
**Resultado:**
```text
 id | avaliacao_id | competencia_id | nota |                        comentario                        
----+--------------+----------------+------+----------------------------------------------------------
  1 |            1 |              1 |    4 | Demonstra excelente capacidade analica e de diagnostico.
```

```sql
SELECT
    id,
    colaborador_id,
    classificacao,
    nivel_tecnico,
    nivel_comportamental,
    potencial_lideranca,
    origem,
    criado_em
FROM perfis_talento
WHERE colaborador_id = (
    SELECT colaborador_id
    FROM avaliacoes
    WHERE id = 1
)
ORDER BY criado_em DESC;
```
**Resultado:**
```text
 id | colaborador_id |    classificacao     | nivel_tecnico | nivel_comportamental | potencial_lideranca |    origem     |           criado_em           
----+----------------+----------------------+---------------+----------------------+---------------------+---------------+-------------------------------
  1 |              1 | ESPECIALISTA_TECNICO | ALTO          | NAO_AVALIADO         | NAO_AVALIADO        | REGRA_DOMINIO | 2026-06-07 15:41:43.924333+00
```

**Verificação de conformidade:**
- Avaliação persistida com sucesso com status `CONCLUIDA`.
- Item de avaliação devidamente vinculado.
- Perfil de talento criado e classificado pelas regras determinísticas do sistema (`ESPECIALISTA_TECNICO`).
- Vínculo com colaborador preservado.
- Avaliador autenticado registrado corretamente (`1`).

---

## 7. Cenários de Validação

### Cenários validados
* **Cenário válido**: Preenchimento completo (colaborador, tipo, nota, observações), resultando no envio HTTP 201 e exibição da tela de resultado. (APROVADO)
* **Colaborador ausente**: O formulário bloqueia o envio e sinaliza erro caso o colaborador não seja selecionado. (APROVADO)
* **Tipo ausente**: O formulário bloqueia o envio e sinaliza erro caso o tipo de avaliação não seja escolhido. (APROVADO)
* **Nenhuma competência selecionada**: Validação no frontend sinaliza que é necessário selecionar pelo menos uma competência para avaliação. (APROVADO)
* **Nota ausente**: Caso a competência seja marcada para avaliação mas nenhuma nota seja informada, o formulário bloqueia o envio exibindo uma mensagem de erro abaixo do campo. (APROVADO)
* **Nota inválida**: O componente de seleção restringe a seleção a inteiros de 1 a 5, bloqueando notas fora dessa faixa. (APROVADO)
* **Clique duplicado**: O botão de envio fica desabilitado com o rótulo "Salvando avaliação..." durante a submissão. (APROVADO)
* **Falha da API**: Caso ocorra falha de rede/API, o formulário mantém os dados previamente preenchidos. (APROVADO)
* **Erro 403 (Acesso Negado)**: Usuários sem permissão recebem uma mensagem de erro "Acesso Negado", e a sessão permanece ativa. (APROVADO)
* **Lista vazia de colaboradores**: Exibe tela de erro e impede a criação caso a lista de colaboradores venha vazia. (APROVADO)
* **Lista vazia de competências**: Exibe tela de erro e impede a criação caso a lista de competências venha vazia. (APROVADO)
* **Competência inativa**: Apenas competências ativas (`ativo !== false`) são exibidas e agrupadas por tipo. (APROVADO)
* **Query parameter**: Acessar com `?colaborador_id=1` seleciona automaticamente o colaborador se ele estiver no escopo. (APROVADO)
* **Acesso direto e reload**: Acessar diretamente ou atualizar a página preserva a sessão do usuário e recarrega os dados. (APROVADO)
* **Resposta parcial**: O componente `ResultadoAvaliacao` possui fallbacks para exibir campos não avaliados ou nulos sem quebrar a renderização. (APROVADO)

### Cenários não validados
* Nenhum (todos os cenários previstos de formulário foram cobertos e validados).

---

## 8. Limitações Conhecidas

- O backend não possui endpoint de listagem geral `GET /avaliacoes`.
- Não há edição de avaliação nesta issue.
- Não há exclusão de avaliação nesta issue.
- Não há comparação histórica de avaliações.
- Não há gráficos de evolução neste módulo.
- A classificação e as recomendações são produzidas por regras determinísticas do domínio.
- Não existe uso de modelo generativo nesta funcionalidade.
- A interface exibe apenas os dados presentes no contrato atual.
- Não foi adicionada nova infraestrutura de testes automatizados frontend, caso o projeto ainda não possua uma.

---

## Conclusão

A ISSUE #023 foi implementada com sucesso.

O frontend permite selecionar um colaborador, escolher o tipo de avaliação, selecionar competências, atribuir notas de 1 a 5, registrar comentários e enviar a avaliação para a API.

A integração ponta a ponta foi validada com resposta HTTP `201 Created`. A avaliação, seus itens e o perfil de talento resultante foram persistidos no banco de dados.

O resultado calculado pelos serviços determinísticos do domínio foi apresentado no frontend, incluindo médias por tipo de competência, média geral, classificação do perfil, pontos fortes, pontos de melhoria e recomendações de desenvolvimento.

O projeto permaneceu aprovado no linter, no build de produção e na execução via Docker.
