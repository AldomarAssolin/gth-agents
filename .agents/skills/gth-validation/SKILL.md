---
name: gth-validation
description: Valida implementações do GTH Agents com lint, build, testes, Docker, migrations, saúde dos serviços, persistência e cenários funcionais. Use ao revisar ou concluir uma ISSUE, preparar walkthrough, verificar regressões ou avaliar se uma entrega pode ser fechada.
---

# GTH Validation

## Objetivo

Produzir evidências confiáveis de que a alteração funciona sem confundir inspeção estática com execução.

## Matriz de validação

Selecione apenas o que se aplica à ISSUE.

### Frontend

```bash
cd frontend
npm run lint
npm run build
```

Verifique também:

- rota direta e reload;
- navegação;
- loading, erro e vazio;
- 401, 403 e 404 relevantes;
- envio duplicado;
- integração com API real;
- responsividade quando exigida.

### Backend

Execute testes específicos primeiro e suíte completa quando viável.

Exemplos:

```bash
docker compose exec api pytest -q <arquivo-ou-filtro>
docker compose exec api pytest -q
```

Verifique migrations quando houver mudança de banco:

```bash
docker compose run --rm -e PYTHONPATH=. api alembic upgrade head
```

### Docker e serviços

```bash
docker compose config
docker compose ps
curl -i http://localhost:5000/health
curl -I http://localhost:5173
```

`docker compose config` valida configuração, não prova que os serviços subiram.

### Persistência

Quando a ISSUE cria ou altera dados, confirme a persistência no PostgreSQL por consulta segura e focada. Não exponha segredos nem dados desnecessários.

### Git

```bash
git diff --check
git status --short
```

## Classificação das evidências

Relate em quatro grupos:

1. Cenários validados por execução.
2. Comportamentos verificados por inspeção estática.
3. Cenários não validados.
4. Bloqueios de ambiente ou contrato.

## Restrições

- Não inventar saídas de comandos.
- Não declarar `100%` sem métrica real.
- Não chamar bloqueio visual de resposta HTTP 403.
- Não considerar `docker compose config` como teste de inicialização.
- Não declarar persistência sem consulta ou evidência equivalente.
- Não executar operações destrutivas para fabricar cenário de teste.
