# Walkthrough — Cobertura de Segurança de Autoria e Autorização (Issue #080)

Este documento registra a implementação e os resultados reais da Issue #080, focada na proteção do backend do GTH Agents contra falsificação de autoria, acesso por perfil inadequado e violações de escopo por colaborador ou setor.

> A cobertura combina RBAC por perfil com controle de acesso por escopo organizacional, validando tanto operações bloqueadas quanto acessos legítimos.

---

## 1. O que foi feito

Desenvolvemos uma nova suíte de testes dedicada à segurança (`backend/tests/test_issue_080_security_coverage.py`) que implementa cenários robustos e integrados para validar a integridade do sistema, sem alterar as regras de negócio existentes.

A suíte resultou em **49 casos de teste** coletados pelo pytest, incluindo
funções parametrizadas e cenários integrados de segurança, cobrindo os seguintes aspectos fundamentais:
- **HTTP 401 (Não Autenticado):** Validação parametrizada de 24 rotas operacionais garantindo que tentativas sem contexto autenticado ou sem o token exigido pelas rotas protegidas resultem em `401 Unauthorized`.
- **HTTP 403 (Perfil Insuficiente):** Validação de 14 rotas operacionais garantindo que usuários com perfil `COLABORADOR` não consigam executar ações restritas a líderes, RH ou administradores.
- **Isolamento de Escopo (Líder Cruzado):** Garantia de que líderes vinculados a um setor específico não conseguem ler, listar, cadastrar ou gerenciar recursos (PDIs, Metas, Feedbacks, Avaliações e Reconhecimentos) de colaboradores de outros setores.
- **Isolamento de Escopo (Colaborador):** Garantia de que colaboradores conseguem ler apenas os seus próprios recursos (PDIs, Metas, Reconhecimentos e Evolução) e recebem `403` caso acessem de terceiros.
- **Prevenção de Vazamento em Listagens:** Validação de que endpoints de listagem de PDIs e Reconhecimentos filtram os registros conforme o escopo do usuário autenticado (retornando apenas os permitidos e preservando a integridade exata dos dados).
- **Mitigação de Spoofing de Autoria:** Confirmação de que as operações de escrita abrangidas pela Issue #080 derivam os respectivos campos de autoria de `g.usuario["id"]`, ignorando identificadores divergentes enviados no payload.
- **Ausência de Persistência após Bloqueio:** Garantia de que requisições bloqueadas por autorização/escopo não realizam qualquer modificação ou persistência oculta no banco de dados.
  > As verificações de persistência consultaram diretamente os models ou a sessão de banco utilizada pelos testes, comparando os registros antes e depois das requisições bloqueadas e validando os campos de autoria efetivamente armazenados.
- **Consistência entre PDI e Ação:** Garantia de que uma ação somente pode ser editada, concluída ou cancelada por meio do PDI ao qual realmente
pertence. Combinações incompatíveis de `pdi_id` e `acao_id` retornam
HTTP `404`, sem alterar a ação.
- **Filtro de Escopo do Dashboard:** Confirmação de que o endpoint `/dashboard/mvp` reflete agregados estatísticos restritos ao setor de atuação do líder.

---

## 2. Testes Executados

### A. Execução da Nova Suíte de Segurança

```bash
PYTHONPATH=. .venv/bin/pytest -v tests/test_issue_080_security_coverage.py
```

**Resultado:** 49 casos de teste aprovados, sem warnings.

```text
============================= 49 passed in XX.XXs =============================
```

### B. Execução da Suíte Completa do Backend

```bash
PYTHONPATH=. .venv/bin/pytest -v
```

**Resultado:** 208 testes aprovados, sem regressões e sem warnings.

```text
============================ 208 passed in XX.XXs =============================
```

---

## 3. Validação Estática e Limpeza

Verificação de arquivos modificados e ausência de arquivos temporários:
```bash
git diff --check
git status --short
```
* **Arquivos Criados:**
  - `docs/backend/walkthroughs/walkthrough_issue_080_security_coverage.md`
  - `backend/tests/test_issue_080_security_coverage.py`
* **Arquivos Modificados:**
  - `docs/backend/implementation-plans/implementation_plan_issue_080_security_coverage.md` (metadados atualizados)
* **Arquivos Temporários:** Nenhum criado.

## 4. Conclusão

A Issue #080 consolidou uma suíte de regressão de segurança para os
principais recursos operacionais protegidos do backend.

Os testes comprovaram:

- exigência de autenticação nas rotas protegidas;
- bloqueio por perfil insuficiente;
- isolamento de dados por colaborador e setor;
- acesso legítimo aos próprios recursos;
- autoria derivada do usuário autenticado;
- ausência de persistência após requisições bloqueadas;
- consistência entre PDIs e suas ações;
- filtragem de listagens e do dashboard conforme o escopo.

A suíte específica foi concluída com 49 casos aprovados, enquanto a suíte
completa do backend encerrou com 208 testes aprovados, sem regressões
detectadas.

Nenhuma regra de negócio do backend foi alterada nesta issue.
