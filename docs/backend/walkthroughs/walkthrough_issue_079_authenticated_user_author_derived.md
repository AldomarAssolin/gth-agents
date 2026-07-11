# Walkthrough — Issue #079 — Derivar Autoria do Usuário Autenticado

Este documento registra a implementação e a validação do mecanismo de segurança que deriva os campos de autoria abrangidos pela Issue #079 a partir do usuário autenticado no JWT, disponível em `g.usuario["id"]`.

A alteração reduz o risco de falsificação de autoria nos fluxos de avaliações, metas, feedbacks, PDI e reconhecimentos, impedindo que identificadores enviados pelo cliente determinem quem será registrado como responsável pela operação.

## Resumo da implementação

O backend foi ajustado para não utilizar os campos de autoria recebidos no payload como fonte da identidade do autor.

Foi adotada uma estratégia transitória de compatibilidade:

* os campos de autoria continuam permitidos no JSON para não quebrar imediatamente os clientes existentes;
* os valores enviados pelo cliente não são utilizados na construção dos DTOs;
* o identificador usado pelo backend é recebido como argumento separado do payload;
* esse identificador é obtido exclusivamente de `g.usuario["id"]`.

Fluxo aplicado:

```text
JWT válido
↓
auth_middleware preenche g.usuario
↓
rota obtém g.usuario["id"]
↓
schema recebe o ID autenticado como argumento separado
↓
DTO é criado com a autoria autenticada
↓
use case valida e persiste o registro
```

## Arquivos criados e alterados

### Novo arquivo de testes

* [test_issue_079_spoofing.py](../../../backend/tests/test_issue_079_spoofing.py): testes de segurança, falsificação de autoria e regressão dos módulos abrangidos.

### Arquivos de documentação

* [implementation_plan_issue_079_authenticated_user_author_derived.md](../../../docs/backend/implementation-plans/implementation_plan_issue_079_authenticated_user_author_derived.md): plano de implementação da issue.
* [walkthrough_issue_079_authenticated_user_author_derived.md](../../../docs/backend/walkthroughs/walkthrough_issue_079_authenticated_user_author_derived.md): relatório da implementação e das validações executadas.

### Arquivos modificados

* [avaliacoes_routes.py](../../../backend/interface/routes/avaliacoes_routes.py): fornece `g.usuario["id"]` ao parser da avaliação.
* [avaliacao_schema.py](../../../backend/interface/schemas/avaliacao_schema.py): passa a receber `avaliador_id` como argumento separado do payload.
* [metas_routes.py](../../../backend/interface/routes/metas_routes.py): fornece `g.usuario["id"]` ao parser da meta.
* [meta_schema.py](../../../backend/interface/schemas/meta_schema.py): passa a receber `criado_por_id` como argumento separado do payload.
* [feedbacks_routes.py](../../../backend/interface/routes/feedbacks_routes.py): fornece `g.usuario["id"]` ao parser do feedback.
* [feedback_schema.py](../../../backend/interface/schemas/feedback_schema.py): passa a receber `autor_id` como argumento separado do payload.

## Decisões técnicas

### Origem obrigatória da autoria

As rotas utilizam:

```python
g.usuario["id"]
```

O acesso direto evita fallback silencioso para `None` caso a chave não esteja presente.

A validade da estrutura de `g.usuario` continua dependendo do middleware de autenticação e da decodificação do JWT.

### Autoria separada do payload

Os parsers passaram a receber o identificador autenticado como parâmetro nomeado separado:

```python
parse_registrar_avaliacao(
    data,
    avaliador_id=authenticated_user_id,
)

parse_criar_meta(
    data,
    criado_por_id=authenticated_user_id,
)

parse_registrar_feedback(
    data,
    autor_id=authenticated_user_id,
)
```

Mesmo que o JSON contenha `avaliador_id`, `criado_por_id` ou `autor_id`, esses valores não são usados na construção do DTO.

### Compatibilidade transitória

O frontend existente ainda envia alguns campos de autoria.

Nesta issue, eles continuam sendo aceitos para preservar compatibilidade, mas são ignorados pelo backend.

A remoção definitiva desses campos dos payloads frontend deverá ser realizada em uma refatoração futura.

### Ações de PDI

A entidade `AcaoPDI` não possui campos próprios de autoria.

Por isso, nenhum campo adicional foi criado para ações de PDI nesta issue.

### Autenticação nos testes

Os testes utilizam o cabeçalho:

```text
X-Enforce-Auth: true
```

Esse cabeçalho é um recurso exclusivo do ambiente de testes, usado para forçar a execução dos mecanismos de autenticação durante a suíte automatizada.

Ele não faz parte do contrato público da API.

## Validação executada

### Testes específicos da Issue #079

Comando executado:

```bash
PYTHONPATH=. .venv/bin/pytest tests/test_issue_079_spoofing.py
```

Resultado:

```text
5 funções de teste aprovadas
```

Cada função contém múltiplas asserções e cenários relacionados a segurança, autenticação, escopo e persistência.

#### Avaliações

O teste `test_seguranca_avaliacao_derivada_jwt` validou:

* campo `avaliador_id` ausente;
* identificador falso enviado no payload;
* identificador inexistente enviado no payload;
* persistência do usuário autenticado;
* HTTP 401 sem autenticação;
* HTTP 403 para colaborador fora do escopo.

#### Metas

O teste `test_seguranca_meta_derivada_jwt` validou que `criado_por_id` é definido pelo usuário autenticado, independentemente do valor enviado pelo cliente.

#### Feedbacks

O teste `test_seguranca_feedback_derivado_jwt` validou que `autor_id` é definido pelo usuário autenticado, independentemente do payload.

#### PDI

O teste `test_regressao_pdi_derivada_jwt` confirmou que o fluxo de criação de PDI continua utilizando o usuário autenticado como criador.

#### Reconhecimentos

O teste `test_regressao_reconhecimento_derivada_jwt` confirmou que:

* `registrado_por_id` é definido pelo usuário autenticado na criação;
* `cancelado_por_id` é definido pelo usuário autenticado no cancelamento.

Os testes de Avaliações, Metas e Feedbacks comprovam a correção de segurança.

Os testes de PDI e Reconhecimentos atuam como regressão, pois esses módulos já derivavam autoria do contexto autenticado.

### Suíte completa

Comando executado:

```bash
PYTHONPATH=. .venv/bin/pytest
```

Resultado:

```text
131 testes aprovados
0 falhas
Duração: 65,28 segundos
```

O baseline anterior à implementação possuía 126 testes aprovados.

A suíte final acrescentou cinco funções de teste específicas da Issue #079, sem regressões nos testes existentes.

## Limitações e riscos conhecidos

O middleware JWT valida assinatura e expiração do token, mas não consulta o usuário no banco em todas as requisições.

Por isso, alterações realizadas após a emissão do token, como:

* desativação do usuário;
* mudança de perfil;
* alteração de setor;
* mudança de escopo;

podem não ser refletidas imediatamente em todos os fluxos.

O comportamento efetivo depende das validações adicionais realizadas por cada use case.

Esse risco não foi alterado nesta issue e deve ser analisado em uma correção específica de autenticação e revogação de acesso.

## Pendência futura

Remover dos payloads frontend os campos:

```text
avaliador_id
criado_por_id
autor_id
```

Após essa limpeza, os schemas públicos poderão deixar de aceitar definitivamente esses campos.

## Conclusão

A Issue #079 foi implementada e validada por testes automatizados específicos e pela suíte completa do backend.

Os fluxos abrangidos deixaram de utilizar identificadores de autoria fornecidos pelo cliente e passaram a derivar a autoria do usuário autenticado disponível em `g.usuario["id"]`.

O frontend atual permaneceu compatível com o contrato transitório adotado, e a suíte final foi concluída com 131 testes aprovados e nenhuma falha.
