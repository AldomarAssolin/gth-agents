# Plano de Implementação - ISSUE #022 (Tela de Evolução do Colaborador)

Este plano descreve a implementação da tela de evolução individual do colaborador no frontend React, consumindo o endpoint do backend `GET /colaboradores/{id}/evolucao`.

## Contrato do Endpoint Real (`GET /colaboradores/{id}/evolucao`)

A estrutura retornada pelo backend (conforme `ConsultarEvolucaoColaboradorUC` e serializador SQLAlquemy) é:

```json
{
  "colaborador": {
    "id": 1,
    "nome": "Colaborador A",
    "matricula": "M001",
    "email": "colabA@test.com",
    "data_admissao": "2026-01-01",
    "status": "ATIVO",
    "setor_id": 1,
    "funcao_id": 1
  },
  "perfil_atual": {
    "id": 2,
    "classificacao": "ESPECIALISTA_TECNICO",
    "resumo": "Resumo 2",
    "nivel_tecnico": "ALTO",
    "nivel_comportamental": "MEDIO",
    "potencial_lideranca": "MEDIO",
    "pontos_fortes": ["Forte 1", "Forte 2"],
    "pontos_melhoria": ["Melhoria 1"],
    "recomendacoes": ["Recomendação 1"],
    "origem": "AGENTE_IA",
    "criado_em": "2026-05-20T10:00:00Z"
  },
  "indicadores": {
    "total_avaliacoes": 1,
    "total_metas": 3,
    "metas_concluidas": 1,
    "metas_atrasadas": 1,
    "total_feedbacks": 1,
    "pdis_ativos": 1,
    "reconhecimentos": 1,
    "media_tecnica": 4.5,
    "media_comportamental": 4.0
  },
  "ultimas_avaliacoes": [
    {
      "id": 1,
      "tipo": "AVALIACAO_LIDER",
      "data_avaliacao": "2026-05-01T10:00:00Z",
      "observacao_geral": "Avaliacao 1"
    }
  ],
  "metas": [
    {
      "id": 1,
      "titulo": "Meta 1",
      "status": "CONCLUIDA",
      "prioridade": "MEDIA",
      "prazo": "2026-06-01"
    }
  ],
  "feedbacks": [
    {
      "id": 1,
      "contexto": "Feedback 1",
      "ponto_positivo": "Bom",
      "ponto_melhoria": "Melhorar",
      "acao_recomendada": "Focar",
      "data_feedback": "2026-05-01T10:00:00Z"
    }
  ],
  "pdis": [
    {
      "id": 1,
      "titulo": "PDI 1",
      "status": "ATIVO",
      "origem": "AVALIACAO",
      "data_inicio": "2026-05-01",
      "data_fim": "2026-06-01"
    }
  ],
  "reconhecimentos": [
    {
      "id": 1,
      "tipo": "DESTAQUE",
      "descricao": "Desc R1",
      "evidencia": "Evi R1",
      "data_reconhecimento": "2026-05-15T10:00:00Z",
      "ativo": true
    }
  ],
  "avaliacoes": [
    {
      "id": 1,
      "tipo": "AVALIACAO_LIDER",
      "observacao_geral": "Avaliacao 1",
      "itens": [
        {
          "id": 1,
          "nota": 4,
          "comentario": "Bom",
          "competencia": {
            "id": 1,
            "nome": "Trabalho em Equipe",
            "tipo": "COMPORTAMENTAL"
          }
        }
      ]
    }
  ]
}
```

> [!NOTE]
> O array de `avaliacoes` (detalhadas) no contrato atual não contém o campo `data_avaliacao` em nível de raiz do modelo (ela está presente apenas em `ultimas_avaliacoes` ou em submodelos).

---

## Diretrizes de Ajustes Técnicos

### 1. Validação de ID na Rota (`EvolucaoColaboradorPage.jsx`)
- O ID recebido do `useParams` será convertido para número.
- O componente verificará se é um inteiro estritamente positivo.
- Se o ID for inválido:
  - Não fará nenhuma chamada de API.
  - Exibirá imediatamente a mensagem de erro: `Identificador de colaborador inválido.`.

### 2. Formatações Centrais (`evolucaoFormatters.js`)
- Criação de um utilitário dedicado a isolar lógica de mapeamento:
  - **Formatação de datas**: Tratamento seguro de datas com fallbacks consistentes.
  - **Formatação de médias**: Exibir `0,0` caso a nota exista e seja `0`, ou exibir formatada com vírgula (padrão pt-BR). Exibir "Ainda não avaliado" apenas para nulo, indefinido, ausente ou se `indicadores.total_avaliacoes === 0`.
  - **Tradução de enums & Classificações**: Mapa de traduções para classificação (ex: `POTENCIAL_LIDER` -> "Potencial Líder", `ESPECIALISTA_TECNICO` -> "Especialista Técnico"), origens e prioridades.
  - Tratamento sistemático de valores `null` e `undefined` com strings de fallback descritivas.

### 3. Comportamento do AbortController
- A busca de dados da evolução utilizará o cancelamento nativo da requisição.
- Ao ocorrer erro de cancelamento (`ERR_CANCELED` ou `CanceledError` do Axios):
  - O erro será **silenciado**, sem exibir banners ou alertas visuais para o usuário.
  - O estado de carregamento (`loading`) não será modificado após o abort para evitar race conditions ou atualizações em componentes desmontados.
- **Troca rápida**: Os dados de evolução anteriores e o estado de erro serão limpos do estado local antes de iniciar qualquer nova busca.

### 4. Exibição de Feedbacks (`FeedbacksResumo.jsx`)
- O contrato atual do endpoint não retorna o campo `autor` na lista de feedbacks.
- O componente de feedbacks exibirá o autor de forma estritamente condicional: somente se o campo estiver presente na resposta do backend. Não inventar ou assumir a presença deste campo.

### 5. Reconhecimentos Legados e Ativos (`ReconhecimentosResumo.jsx`)
- Considerar como **ativo** qualquer reconhecimento cujo campo `ativo` não seja explicitamente `false` (i.e. `true` ou ausente/indefinido), a fim de manter ampla compatibilidade com respostas e dados legados do banco.

---

## Proposed Changes

### Módulo de Evolução (`src/features/evolucao`)

#### [NEW] [evolucaoService.js](../../../frontend/src/features/evolucao/evolucaoService.js)
Serviço de busca de dados recebendo e encaminhando o `signal` de cancelamento.

#### [NEW] [evolucaoFormatters.js](../../../frontend/src/features/evolucao/evolucaoFormatters.js)
Isola lógica de tradução de enums, formatação de médias/datas e strings de fallback.

#### [NEW] [DadosColaboradorCard.jsx](../../../frontend/src/features/evolucao/DadosColaboradorCard.jsx)
Card de dados básicos mostrando apenas os IDs de setor e função.

#### [NEW] [PerfilTalentoCard.jsx](../../../frontend/src/features/evolucao/PerfilTalentoCard.jsx)
Exibe classificação de talento, resumo, níveis, pontos fortes/fracos e recomendações (tratando listas vazias/nulas).

#### [NEW] [IndicadoresEvolucao.jsx](../../../frontend/src/features/evolucao/IndicadoresEvolucao.jsx)
Exibe todos os contadores quantitativos.

#### [NEW] [ResumoCompetenciasCard.jsx](../../../frontend/src/features/evolucao/ResumoCompetenciasCard.jsx)
Cards com as médias técnica e comportamental, formatadas de forma correta (com fallback seguro).

#### [NEW] [AvaliacoesTimeline.jsx](../../../frontend/src/features/evolucao/AvaliacoesTimeline.jsx)
Cronologia de `ultimas_avaliacoes` (visão resumida).

#### [NEW] [AvaliacoesDetalhes.jsx](../../../frontend/src/features/evolucao/AvaliacoesDetalhes.jsx)
Listagem completa e detalhada das avaliações e notas das competências a partir de `avaliacoes`.

#### [NEW] [MetasResumo.jsx](../../../frontend/src/features/evolucao/MetasResumo.jsx)
Listagem das metas com realce de prioridade e atraso.

#### [NEW] [PDISResumo.jsx](../../../frontend/src/features/evolucao/PDISResumo.jsx)
Resumos do PDI sem renderizar ações (não contempladas pelo contrato).

#### [NEW] [FeedbacksResumo.jsx](../../../frontend/src/features/evolucao/FeedbacksResumo.jsx)
Exibição dos feedbacks com renderização condicional do autor.

#### [NEW] [ReconhecimentosResumo.jsx](../../../frontend/src/features/evolucao/ReconhecimentosResumo.jsx)
Apresenta reconhecimentos cujos campos `ativo` não sejam explicitamente `false`.

---

### Páginas

#### [MODIFY] [EvolucaoColaboradorPage.jsx](../../../frontend/src/pages/EvolucaoColaboradorPage.jsx)
Página principal contendo validação estrita do ID de rota, limpeza de estados anteriores para novas buscas, silenciamento de erros de cancelamento e layout responsivo.

---

## Verification Plan

### Automated Tests
- Executar `npm run lint`.
- Executar `npm run build`.

### Manual Verification
O subagente do navegador testará:
1. **Identificador inválido**: Acessar `/colaboradores/abc/evolucao` e verificar mensagem de erro sem chamadas adicionais.
2. **Perfil atual nulo**: Acessar colaborador sem perfil registrado e verificar tratamento de fallback no card de perfil de talento.
3. **Avaliação sem itens**: Verificar integridade da renderização do componente de detalhes das avaliações.
4. **Feedback sem ponto_melhoria**: Confirmar que o feedback é exibido normalmente com fallbacks corretos.
5. **Indicadores parcialmente ausentes**: Garantir robustez perante a ausência parcial das chaves de indicadores.
6. **Acesso direto e recarga (reload)**: Garantir persistência de dados e funcionamento correto.
7. **Troca rápida de colaboradores**: Trocar de ID repetidamente de forma rápida para comprovar o cancelamento correto de chamadas HTTP ativas (race conditions).
8. **Erros 403 e 404**: Validar as telas de erro correspondentes.
9. **Responsividade**: Testar visualização em celular e tablet.
