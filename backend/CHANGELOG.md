# Changelog

## v1.0.0-mvp-backend

### Adicionado

- Autenticação JWT e geração de tokens seguros.
- Controle de acesso baseado em perfis (RBAC: ADMIN, RH, LIDER e COLABORADOR).
- Controle de acesso refinado por escopo (líderes limitados a colaboradores do setor, colaboradores limitados aos próprios dados).
- Módulos completos do MVP:
  - Cadastro de usuários, setores, funções, colaboradores e competências.
  - Avaliação de competências (Agente Avaliador com médias por tipo de competência: técnica, comportamental e liderança).
  - Classificação de perfil de talento (Agente Perfilador baseado nos pesos e médias).
  - Metas individuais e geração automática/estruturação de feedbacks (Agente Estruturador de Feedbacks).
  - Plano de Desenvolvimento Individual (PDI) com múltiplos tipos de ações práticas e controle de status de conclusão/cancelamento.
  - Reconhecimento com evidências rastreáveis e fluxo de cancelamento seguro.
  - Evolução consolidada de histórico do colaborador.
  - Dashboard gerencial do MVP com contadores e alertas de status.
- Documentação técnica completa da API no diretório `docs/`.
- Collection e Environment do Postman configurados na pasta `postman/`.

### Segurança

- Decorações de rotas com `@auth_required` e `@roles_required` em todos os endpoints sensíveis.
- Lógica de escopo centralizada (`AccessScopeService`) validando transações do Unit of Work.
- Remoção global automática de campos confidenciais como `senha` e `senha_hash` nas respostas serializadas da API.
- Bloqueio de autenticação para usuários inativos.

### Testes

- Suite de 126 testes de integração e unitários cobrindo 100% dos fluxos críticos de negócio e segurança.
- Cobertura geral de testes mantida em 90% do projeto com integração do plugin `pytest-cov`.
- Migrations automáticas do banco de dados validadas do zero (clean database).

### Release

- Primeira versão oficial estável do MVP Backend do GTH Agents.
