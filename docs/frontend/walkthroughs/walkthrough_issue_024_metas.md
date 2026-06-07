# Walkthrough - Implementação do Módulo de Metas (Issue #024)

Este documento descreve a implementação, os testes e a homologação do módulo de acompanhamento e gestão de metas (Metas) no frontend do monorepo **GTH Agents**.

---

## 1. Objetivo

Implementar e integrar o módulo de metas no frontend do monorepo GTH Agents, permitindo a visualização de metas associadas a colaboradores de forma dinâmica, a filtragem de metas locais por status, a criação de novas metas por usuários gestores autorizados, e o tratamento robusto de restrições de acesso, ciclos de vida de chamadas com AbortController, carregamento e tratamento de erros.

---

## 2. Arquivos Criados e Alterados

### Criados
- [metasService.js](../../../frontend/src/features/metas/metasService.js): Serviço de comunicação com os endpoints `/metas` (criação) e `/colaboradores/<id>/metas` (listagem).
- [metasFormatters.js](../../../frontend/src/features/metas/metasFormatters.js): Utilitário para formatação segura de prazos no padrão brasileiro (`DD/MM/AAAA`) livre de problemas de timezone.
- [metasErrors.js](../../../frontend/src/features/metas/metasErrors.js): Tradução de mensagens de erro amigáveis baseadas em respostas JSON da API.
- [StatusMetaBadge.jsx](../../../frontend/src/features/metas/StatusMetaBadge.jsx): Badge de representação visual do status da meta (Pendente, Em andamento, Concluída, Atrasada, Cancelada) com fallback seguro.
- [PrioridadeMetaBadge.jsx](../../../frontend/src/features/metas/PrioridadeMetaBadge.jsx): Badge de representação visual da prioridade da meta (Baixa, Média, Alta, Crítica) com fallback seguro.
- [MetasTable.jsx](../../../frontend/src/features/metas/MetasTable.jsx): Tabela de apresentação responsiva de metas.
- [MetasColaboradorView.jsx](../../../frontend/src/features/metas/MetasColaboradorView.jsx): Componente unificado para listagem, filtragem de status local e estados vazios/erro de um colaborador específico.
- [MetaForm.jsx](../../../frontend/src/features/metas/MetaForm.jsx): Formulário de criação de metas com validação rigorosa de campos no frontend.
- [NovaMetaPage.jsx](../../../frontend/src/pages/NovaMetaPage.jsx): Página de controle para criação de novas metas.
- [MetasColaboradorPage.jsx](../../../frontend/src/pages/MetasColaboradorPage.jsx): Página dedicada à listagem das metas de um colaborador.

### Alterados
- [MetasPage.jsx](../../../frontend/src/pages/MetasPage.jsx): Atualizado para atuar como central do módulo com seletor de colaboradores para gestores e exibição automática das metas para o perfil `COLABORADOR`.
- [AppRoutes.jsx](../../../frontend/src/routes/AppRoutes.jsx): Registro das rotas `/metas/nova` e `/colaboradores/:id/metas`.
- [ColaboradorDetalhe.jsx](../../../frontend/src/features/colaboradores/ColaboradorDetalhe.jsx): Liberação dos atalhos para criação e visualização das metas do colaborador.

---

## 3. Contratos Reais Utilizados

O desenvolvimento baseia-se diretamente nos contratos fornecidos pelo backend:
1. `GET /colaboradores/<int:id>/metas`
   - Retorna array de metas de um colaborador específico.
   - Código HTTP de sucesso: `200 OK`.
2. `POST /metas`
   - Criação de meta associada a um colaborador.
   - Código HTTP de sucesso: `201 Created`.
   - Payload JSON suportado:
     ```json
     {
       "colaborador_id": 1,
       "criado_por_id": 1,
       "titulo": "Melhorar cobertura de testes unitarios",
       "descricao": "Escrever testes automatizados para os controllers",
       "indicador": null,
       "prazo": "2026-07-30",
       "prioridade": "ALTA"
     }
     ```

---

## 4. Decisões Técnicas

- **Reutilização da Camada de View**: O componente `MetasColaboradorView` centraliza toda a lógica de carregamento, filtragem local de status e exibição da tabela. Ele é reutilizado em `MetasPage`, `MetasColaboradorPage` e na visualização própria do perfil `COLABORADOR`, evitando duplicação de lógica.
- **Validação de Identificadores**: IDs obtidos da URL ou da query string são convertidos e validados como inteiros estritamente maiores que zero antes de disparar consultas na API.
- **Prevenção de Condições de Corrida**: As requisições assíncronas de carregamento de metas e colaboradores utilizam `AbortController` para cancelar chamadas obsoletas durante desmontagem ou troca de seleção.
- **Persistência de Seleção**: A seleção de colaborador em `MetasPage` é persistida no histórico de navegação e na query string (`/metas?colaborador_id=X`), permitindo o compartilhamento e recarregamento direto da tela mantendo o colaborador selecionado.

---

## 5. Limitação de GET /metas

O backend **não** disponibiliza o endpoint global:
```http
GET /metas
```
Por esse motivo:
- ADMIN, RH e LIDER selecionam um colaborador antes da consulta;
- COLABORADOR visualiza diretamente as metas do colaborador vinculado;
- A listagem utiliza obrigatoriamente:
  ```http
  GET /colaboradores/{id}/metas
  ```
- A página geral `/metas` funciona como entrada do módulo e não como listagem global consolidada.

---

## 6. Autorização Visual e Integridade do Formulário

### Integridade do formulário e limitação de segurança
O campo `criado_por_id` não é exibido no formulário e é preenchido automaticamente com o identificador do usuário autenticado obtido pelo `AuthContext` (`user.id`).

Essa medida garante consistência na interface, mas não representa uma proteção definitiva, pois o payload pode ser alterado fora do frontend. A validação efetiva deve ocorrer no backend, comparando `criado_por_id` com o usuário autenticado ou obtendo o identificador diretamente do JWT.

### Distinção entre Usuário e Colaborador
O sistema diferencia claramente os campos:
- `user.id`: Identificador da conta de usuário autenticada (utilizado para registrar `criado_por_id`).
- `user.colaborador_id`: Identificador do colaborador associado ao usuário.

Para o perfil `COLABORADOR`, a consulta das metas utiliza `user.colaborador_id`. O campo `user.id` é usado apenas como identificador do usuário criador de uma meta e não é utilizado como identificador do colaborador.

Quando `user.colaborador_id` não está disponível (nulo/indefinido), nenhuma requisição de metas é realizada e a interface exibe um aviso informando que o usuário ainda não está vinculado a um colaborador no sistema.

---

## 7. Lint

Comando executado:
```bash
cd frontend
npm run lint
```
Resultado:
- Exit code: `0`
- Quantidade de erros: `0`
- Quantidade de avisos: `0`

---

## 8. Build

Comando executado:
```bash
cd frontend
npm run build
```
Resultado:
- Vite: `v8.0.14`
- Módulos transformados: `155`
- Tempo de build: `833ms`
- Arquivos gerados em `dist/`:
  - `dist/index.html` (0.46 kB │ gzip: 0.29 kB)
  - `dist/assets/index-Db6ASqPO.css` (24.85 kB │ gzip: 5.41 kB)
  - `dist/assets/index-Dh7gc_Ks.js` (402.80 kB │ gzip: 117.20 kB)

---

## 9. Docker e Conectividade

### Docker Compose
Comandos executados:
```bash
docker compose config
docker compose up --build -d
docker compose ps
```
Resultado:
- Configuração válida.
- Banco PostgreSQL (`db-1`) iniciado com status `Up (healthy)`.
- API Flask (`api-1`) iniciada com status `Up`.
- Frontend Vite (`web-1`) iniciado com status `Up`.

### Conectividade
Comandos executados:
```bash
curl -i http://localhost:5000/health
curl -I http://localhost:5173
```
Resultado:
- Backend API: HTTP `200 OK`, retornando `{"status":"ok"}`.
- Frontend Web: HTTP `200 OK`.

### Execução do Seed
O arquivo `seed_db.py` foi executado manualmente no contêiner da API para preparar os dados de teste utilizados na validação funcional:
```bash
docker compose exec api python seed_db.py
```

---

## 10. Validação da Listagem para Gestor

Acesso do perfil gestor (`ADMIN`) carregando a lista de colaboradores, selecionando o "Colaborador A (Engenharia)" no seletor de colaboradores, persistindo seu ID na URL e apresentando a tabela de metas correspondente.

![Visualização de Metas do Gestor](../../../frontend/src/assets/imagens/issue_024_metas_lista_gestor.png)

---

## 11. Validação da Listagem para Colaborador

Acesso do perfil `COLABORADOR` (`colab@test.com`) no qual o seletor global de colaboradores é ocultado, carregando diretamente as metas vinculadas a seu `user.colaborador_id` (comportamento garantido pelo `AuthContext`).

![Visualização de Metas do Colaborador](../../../frontend/src/assets/imagens/issue_024_metas_lista_colaborador.png)

---

## 12. Validação do Filtro

O filtro por status funciona localmente sobre a coleção carregada, sem gerar novas requisições HTTP para a API.
Os filtros testados incluem:
- Todos os Status;
- Pendente;
- Em andamento;
- Concluída;
- Atrasada;
- Cancelada.

Quando o status selecionado não contém metas correspondentes, o componente de estado vazio (`EmptyState`) é exibido de forma limpa.

---

## 13. Validação da Criação

Fluxo completo de criação de meta executado com sucesso como administrador.

Endpoint:
```http
POST /metas
```
Payload enviado:
```json
{
  "colaborador_id": 1,
  "criado_por_id": 1,
  "titulo": "Nova Meta de Teste",
  "descricao": "Descricao de teste",
  "indicador": null,
  "prazo": "2026-08-30",
  "prioridade": "ALTA"
}
```
Resposta da API:
- HTTP `201 Created`
- status: `"PENDENTE"`
- origem: `"MANUAL"`

Tela de formulário de criação preenchido:

![Nova Meta Formulário](../../../frontend/src/assets/imagens/issue_024_metas_nova.png)

Tela de sucesso com detalhes exibidos após a criação bem-sucedida da meta:

![Meta criada com sucesso](../../../frontend/src/assets/imagens/issue_024_metas_criada.png)

---

## 14. Persistência no Banco

A gravação dos dados foi validada diretamente no banco de dados PostgreSQL executando a consulta:
```sql
SELECT id, colaborador_id, criado_por_id, titulo, descricao, indicador, prazo, prioridade, status, origem FROM metas ORDER BY id DESC LIMIT 1;
```
Resultado retornado:
```text
 id | colaborador_id | criado_por_id |       titulo       |     descricao      | indicador |   prazo    | prioridade |  status  | origem
----+----------------+---------------+--------------------+--------------------+-----------+------------+------------+----------+--------
  4 |              1 |             1 | Nova Meta de Teste | Descricao de teste |           | 2026-08-30 | ALTA       | PENDENTE | MANUAL
```
Os dados inseridos no banco são idênticos aos enviados pelo frontend e estão devidamente associados ao colaborador e ao criador.

---

## 15. Validação de Rotas

Cenários de rotas testados e validados no frontend:
- `/metas`: Carrega com seletor (Gestores) ou carrega metas próprias (Colaborador).
- `/metas?colaborador_id=1`: Carrega o seletor com o Colaborador A pré-selecionado.
- `/metas?colaborador_id=999` (ID inexistente): Remove o parâmetro indevido e limpa a seleção.
- `/metas/nova?colaborador_id=1`: Abre a tela de criação com o Colaborador A pré-selecionado e travado.
- `/metas/nova` (acesso como COLABORADOR): Exibe tela de "Acesso Negado" com link para voltar às metas.

Tela de bloqueio visual da rota de criação exibida para o perfil colaborador:

![Acesso Negado](../../../frontend/src/assets/imagens/issue_024_metas_acesso_negado.png)

---

## 16. Validações de Formulário

A validação de integridade do formulário de criação de metas foi testada:
- **Títulos e Descrições com Espaços**: Inputs são higienizados com `.trim()`. Títulos ou descrições vazias ou compostas apenas por espaços em branco disparam erro de campo obrigatório.
- **Prazos em Branco**: Impedidos pelo validador do formulário.
- **Prevenção de Duplo Envio**: O botão de submissão é desabilitado e seu texto é alterado para "Salvando..." enquanto a promise de envio estiver pendente.
- **Prioridade inválida**: Valores fora de `BAIXA`, `MEDIA`, `ALTA` e `CRITICA` são rejeitados antes do envio.

---

## 17. Cenários Validados por Execução

- **Login e Autenticação**: Login realizado com sucesso como gestor (`admin@test.com`) e colaborador (`colab@test.com`).
- **Seletor de Colaboradores**: Funcionamento, preenchimento e persistência na URL.
- **Filtragem Local por Status**: Execução do filtro de status com atualização imediata da tabela e exibição de estados vazios.
- **Criação de Meta (201 Created)**: Fluxo completo de preenchimento, submissão, verificação de payloads e renderização do card de sucesso.
- **Persistência de Dados**: Confirmação de integridade dos campos no PostgreSQL.
- **Proteção visual da rota**: Validação do bloqueio ao acessar `/metas/nova` com perfil `COLABORADOR`, exibindo a tela de acesso negado sem executar a criação.

---

## 18. Comportamentos Verificados por Inspeção Estática

- **Fallbacks dos badges:** Verificados por inspeção estática dos mapeamentos e dos valores padrão usados para status e prioridades ausentes ou desconhecidos.
- **Tratamento de 401**: Verificado que o service de metas propaga o erro de autenticação diretamente para o interceptor global de API da aplicação.
- **Preservação de Dados**: Verificado estaticamente que falhas de rede no formulário preservam os inputs já digitados pelo usuário.
- **Formatação de datas**: O prazo é formatado a partir da parte `YYYY-MM-DD`, sem conversão por `Date`, evitando deslocamentos causados por fuso horário.
  - O prazo `2026-08-30` foi exibido como `30/08/2026`.

---

## 19. Limitações Conhecidas

- **Ausência de Listagem Geral consolidada**: Conforme descrito na seção 5, devido à limitação de contrato da API do backend.
- **Segurança de Identidade**: O backend confia no `criado_por_id` fornecido no payload JSON em vez de obtê-lo do JWT. O frontend preenche este campo de forma automatizada, mas o comportamento final de integridade de autoria reside sob responsabilidade da API.
- **Ausência de Testes Automatizados no Frontend**: O repositório atual ainda não possui infraestrutura de testes automatizados configurada (como Vitest ou React Testing Library) para validar as páginas e componentes do frontend.

---

## 20. Resultado Final

A ISSUE #024 foi implementada e validada conforme o escopo definido. A listagem por colaborador, o filtro por status, a criação de metas, o controle visual de acesso e a persistência no PostgreSQL foram comprovados.
