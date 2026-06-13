---

name: gth-manual-validation-handoff
description: >
Gera e acompanha um Scratchpad de validação manual para issues do GTH Agents.
Deve ser usada quando a validação exigir navegador, interação visual,
autenticação por múltiplos perfis, responsividade, screenshots, vídeos
ou outras atividades que devam ser executadas pelo usuário para reduzir
consumo de recursos do agente.
------------------------------

# GTH Manual Validation Handoff

## Objetivo

Transferir ao usuário os testes manuais e visuais que não devem ser executados automaticamente pelo agente.

Esta Skill deve gerar um Scratchpad específico para a issue em execução, baseado em:

* escopo da issue;
* plano de implementação;
* critérios de aceite;
* contratos reais da API;
* arquivos alterados;
* perfis de acesso;
* regras de negócio;
* limitações conhecidas;
* validações técnicas já executadas.

A Skill não contém cenários fixos de um módulo específico.

---

# Quando usar

Usar esta Skill quando houver necessidade de:

* abrir navegador;
* navegar entre páginas;
* preencher formulários;
* testar fluxos funcionais completos;
* testar diferentes perfis de acesso;
* validar loading, erro e estados vazios;
* validar responsividade;
* capturar screenshots;
* gravar vídeos;
* confirmar experiência do usuário;
* produzir evidências visuais;
* homologar comportamento que não pode ser comprovado apenas por lint, build ou testes automatizados.

---

# Quando não usar

Não usar esta Skill para substituir:

* lint;
* build;
* testes unitários;
* testes de integração;
* testes backend;
* validação de migrations;
* validação de Docker Compose;
* inspeção de contratos;
* análise estática;
* consultas técnicas que o agente pode executar com baixo consumo.

---

# Princípio obrigatório

A implementação pode ser tecnicamente concluída sem estar funcionalmente homologada.

Os estados devem ser separados:

```text
IMPLEMENTAÇÃO CONCLUÍDA
VALIDAÇÃO TÉCNICA CONCLUÍDA
VALIDAÇÃO MANUAL PENDENTE
VALIDAÇÃO MANUAL CONCLUÍDA
PRONTO PARA FECHAMENTO
```

Quando existirem testes manuais obrigatórios ainda não executados, usar:

```text
Status: AGUARDANDO VALIDAÇÃO HUMANA
```

Não declarar a issue pronta, concluída ou totalmente validada antes do retorno do usuário.

---

# Fluxo da Skill

```text
1. Ler a issue.
2. Ler o plano de implementação.
3. Inspecionar as alterações realizadas.
4. Ler os critérios de aceite.
5. Identificar validações já executadas.
6. Identificar cenários manuais ainda necessários.
7. Classificar cada cenário.
8. Gerar Scratchpad específico da issue.
9. Interromper o fechamento.
10. Aguardar o usuário preencher os resultados.
11. Revisar o Scratchpad preenchido.
12. Consolidar resultados no walkthrough.
13. Informar se a issue está pronta para fechamento.
```

---

# Fontes obrigatórias para gerar os cenários

Antes de criar o Scratchpad, analisar:

```text
- descrição da issue;
- plano de implementação;
- walkthrough parcial, se existir;
- contratos reais da API;
- rotas frontend;
- perfis autorizados;
- regras de escopo;
- estados e transições de domínio;
- componentes e páginas alterados;
- tratamento de loading;
- tratamento de erro;
- tratamento de dados vazios;
- critérios de aceite.
```

Não criar cenários baseados apenas no nome da issue.

---

# Classificação dos testes

Cada item deve ser classificado como:

## Automatizado

Executado por ferramenta ou comando.

Exemplos:

```text
npm run lint
npm run build
pytest
docker compose config
```

## Manual funcional

Exige interação do usuário.

Exemplos:

```text
preencher formulário
navegar entre páginas
testar fluxo de criação
testar atualização
testar transição de status
```

## Manual visual

Exige observação da interface.

Exemplos:

```text
responsividade
badge
mensagem de erro
estado vazio
loading
layout
```

## Segurança e perfil

Exige autenticação com diferentes perfis.

Exemplos:

```text
ADMIN
RH
LIDER
COLABORADOR
```

## Evidência

Exige captura ou registro.

Exemplos:

```text
screenshot
vídeo
resposta HTTP
consulta ao banco
```

---

# Geração dos cenários

Para cada funcionalidade implementada, verificar se existe cenário para:

```text
- caminho principal;
- validação de campos;
- erro esperado;
- estado vazio;
- acesso direto por URL;
- reload;
- persistência;
- autorização;
- escopo;
- transição de estado;
- comportamento após escrita;
```

Gerar apenas cenários aplicáveis à issue.

Não criar cenários genéricos sem relação com a implementação.

---

# Estrutura obrigatória do Scratchpad

Criar o arquivo:

```text
docs/scratchpads/issue-{numero}-manual-validation.md
```

O conteúdo deve seguir esta estrutura:

````md
# Scratchpad de Validação Manual - ISSUE #{numero}

## Identificação

- Issue:
- Módulo:
- Branch:
- Data:
- Responsável pela validação:
- Status: AGUARDANDO VALIDAÇÃO HUMANA

## Validações técnicas já executadas

| Validação | Resultado | Evidência |
|---|---|---|
| Lint | | |
| Build | | |
| Testes automatizados | | |
| Docker | | |
| API | | |

## Ambiente necessário

- Frontend:
- API:
- Banco:
- Perfis necessários:
- Dados de teste necessários:

Não registrar senhas, tokens ou segredos.

## Dados gerados durante o teste

| Recurso | Identificador |
|---|---|
| colaborador_id | |
| recurso_id | |
| outros IDs | |

## Cenários manuais

### Cenário {número} - {nome}

Tipo:

```text
MANUAL_FUNCIONAL | MANUAL_VISUAL | SEGURANÇA | PERSISTÊNCIA
````

Objetivo:

Pré-condições:

Passos:

1.
2.
3.

Resultado esperado:

Resultado observado:

Status HTTP observado:

```text
```

Resultado:

```text
PENDENTE | APROVADO | REPROVADO | BLOQUEADO | NÃO EXECUTADO
```

Evidências:

```text
Screenshot:
Vídeo:
Resposta HTTP:
Consulta ao banco:
```

Observações:

## Evidências geradas

| Cenário | Tipo | Arquivo ou referência | Resultado |
| ------- | ---- | --------------------- | --------- |
|         |      |                       |           |

## Problemas encontrados

| ID | Cenário | Descrição | Severidade | Situação |
| -- | ------- | --------- | ---------- | -------- |
|    |         |           |            |          |

## Resultado final

* [ ] Todos os cenários obrigatórios foram aprovados.
* [ ] Existem falhas.
* [ ] Existem bloqueios.
* [ ] Existem cenários não executados.
* [ ] O walkthrough pode ser finalizado.
* [ ] A issue pode seguir para fechamento.

## Autorização do usuário

```text
Validação manual concluída: SIM | NÃO
Walkthrough pode ser finalizado: SIM | NÃO
Issue pode ser marcada como pronta: SIM | NÃO
```

````

---

# Regras para nomear evidências

Gerar nomes previsíveis:

```text
issue_{numero}_{modulo}_{cenario}.{extensao}
````

Exemplos genéricos:

```text
issue_042_pdi_criacao_sucesso.png
issue_024_metas_listagem.png
issue_019_auth_login_invalido.png
```

A Skill deve sugerir o nome, mas não afirmar que o arquivo existe.

---

# Quantidade de evidências

Não exigir screenshot para todo passo.

Priorizar evidências para:

```text
- criação concluída;
- estado final relevante;
- erro importante;
- acesso negado;
- visão específica por perfil;
- responsividade;
- fluxo central da issue.
```

Evitar produção excessiva de imagens ou vídeos.

Vídeo deve ser solicitado apenas quando comprovar um fluxo contínuo que várias imagens não representariam adequadamente.

---

# Regras de segurança

Nunca incluir no Scratchpad:

```text
- senhas;
- tokens;
- cookies;
- secrets;
- conteúdo de .env;
- dados pessoais reais;
- caminhos privados desnecessários.
```

Referenciar usuários apenas por perfil ou e-mail de teste quando necessário.

Exemplo:

```text
Usuário de teste com perfil COLABORADOR
```

---

# Regras de execução

Sem autorização explícita, a Skill não deve:

```text
- abrir navegador;
- executar automação visual;
- capturar screenshot;
- gravar vídeo;
- editar imagem;
- executar testes manuais;
- preencher formulários;
- realizar login;
- fazer commit;
- fazer push;
- fazer merge;
- trocar branch;
- fechar issue.
```

---

# Retorno após geração

Depois de criar o Scratchpad, informar:

```text
Implementação e validações técnicas concluídas.

Os testes manuais foram preparados em:

docs/scratchpads/issue-{numero}-manual-validation.md

Status: AGUARDANDO VALIDAÇÃO HUMANA
```

Não declarar que a issue está pronta.

---

# Processamento do Scratchpad preenchido

Quando o usuário informar que concluiu os testes:

1. Ler o Scratchpad atualizado.
2. Verificar quais cenários foram aprovados.
3. Verificar falhas e bloqueios.
4. Verificar se as evidências informadas existem.
5. Não alterar resultados fornecidos pelo usuário.
6. Não transformar cenário não executado em aprovado.
7. Atualizar o walkthrough.
8. Separar claramente:

   * validado automaticamente;
   * validado manualmente;
   * verificado por inspeção;
   * não executado;
   * bloqueado.
9. Informar se a issue pode seguir para fechamento.

---

# Critério de prontidão

A issue só pode ser considerada pronta quando:

```text
- validações técnicas obrigatórias passaram;
- cenários manuais obrigatórios foram aprovados;
- falhas críticas foram corrigidas;
- bloqueios foram resolvidos ou formalmente aceitos;
- evidências obrigatórias foram fornecidas;
- usuário autorizou o fechamento.
```

Caso contrário:

```text
Status: NÃO PRONTA PARA FECHAMENTO
```

---

# Integração com outras Skills

## gth-issue-implementation

Deve acionar esta Skill quando identificar testes manuais ou visuais.

## gth-validation

Deve executar primeiro as validações técnicas e delegar a esta Skill apenas o que exigir intervenção humana.

## gth-documentation

Deve usar o Scratchpad preenchido como fonte para o walkthrough final.

## gth-git-workflow

Não deve permitir fechamento, commit final de documentação ou PR como concluído enquanto a validação humana obrigatória estiver pendente, salvo autorização expressa do usuário.
