import pytest
import json
from decimal import Decimal

from app import create_app
from app.config import Config
from app.extensions import db
from infrastructure.database.base import Base
import infrastructure.database.models  # noqa


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


@pytest.fixture
def client():
    app = create_app(TestConfig)
    with app.app_context():
        Base.metadata.create_all(db.engine)
        yield app.test_client()
        Base.metadata.drop_all(db.engine)


def test_setores_crud(client):
    # 1. POST Create
    res = client.post("/setores", json={"nome": "TI", "descricao": "Tecnologia"})
    assert res.status_code == 201
    setor = res.get_json()
    assert setor["nome"] == "TI"
    assert setor["ativo"] is True
    setor_id = setor["id"]

    # 2. GET by id
    res = client.get(f"/setores/{setor_id}")
    assert res.status_code == 200
    assert res.get_json()["nome"] == "TI"

    # GET non-existent
    res = client.get("/setores/999")
    assert res.status_code == 404

    # 3. GET list
    res = client.get("/setores")
    assert res.status_code == 200
    assert len(res.get_json()) == 1

    # 4. PUT Update
    res = client.put(f"/setores/{setor_id}", json={"nome": "TI Atualizado", "descricao": "TI Novo"})
    assert res.status_code == 200
    assert res.get_json()["nome"] == "TI Atualizado"

    # Create another one to test conflict on update
    client.post("/setores", json={"nome": "RH", "descricao": "Recursos"})
    res = client.put(f"/setores/{setor_id}", json={"nome": "RH", "descricao": "Conflito"})
    assert res.status_code == 409

    # 5. PATCH Desativar
    res = client.patch(f"/setores/{setor_id}/desativar")
    assert res.status_code == 200
    assert res.get_json()["ativo"] is False


def test_funcoes_crud(client):
    # 1. POST Create
    res = client.post("/funcoes", json={"nome": "Developer", "descricao": "Dev"})
    assert res.status_code == 201
    funcao = res.get_json()
    assert funcao["nome"] == "Developer"
    assert funcao["ativo"] is True
    funcao_id = funcao["id"]

    # 2. GET by id
    res = client.get(f"/funcoes/{funcao_id}")
    assert res.status_code == 200
    assert res.get_json()["nome"] == "Developer"

    # GET non-existent
    res = client.get("/funcoes/999")
    assert res.status_code == 404

    # 3. GET list
    res = client.get("/funcoes")
    assert res.status_code == 200
    assert len(res.get_json()) == 1

    # 4. PUT Update
    res = client.put(f"/funcoes/{funcao_id}", json={"nome": "Dev Lead", "descricao": "Lideranca"})
    assert res.status_code == 200
    assert res.get_json()["nome"] == "Dev Lead"

    # Conflict
    client.post("/funcoes", json={"nome": "RH Analyst"})
    res = client.put(f"/funcoes/{funcao_id}", json={"nome": "RH Analyst"})
    assert res.status_code == 409

    # 5. PATCH Desativar
    res = client.patch(f"/funcoes/{funcao_id}/desativar")
    assert res.status_code == 200
    assert res.get_json()["ativo"] is False


def test_usuarios_crud(client):
    # 1. POST Create
    res = client.post("/usuarios", json={
        "nome": "User A",
        "email": "user_a@example.com",
        "senha": "password",
        "perfil": "COLABORADOR"
    })
    assert res.status_code == 201
    user = res.get_json()
    assert user["nome"] == "User A"
    assert user["email"] == "user_a@example.com"
    assert "senha" not in user
    assert "senha_hash" not in user
    user_id = user["id"]

    # 2. GET by id
    res = client.get(f"/usuarios/{user_id}")
    assert res.status_code == 200
    user_get = res.get_json()
    assert user_get["nome"] == "User A"
    assert "senha" not in user_get
    assert "senha_hash" not in user_get

    # GET non-existent
    res = client.get("/usuarios/999")
    assert res.status_code == 404

    # 3. GET list
    res = client.get("/usuarios")
    assert res.status_code == 200
    assert len(res.get_json()) == 1

    # 4. PUT Update
    res = client.put(f"/usuarios/{user_id}", json={
        "nome": "User A Updated",
        "email": "user_a_new@example.com",
        "perfil": "LIDER"
    })
    assert res.status_code == 200
    user_put = res.get_json()
    assert user_put["nome"] == "User A Updated"
    assert user_put["email"] == "user_a_new@example.com"
    assert user_put["perfil"] == "LIDER"

    # Conflict
    client.post("/usuarios", json={
        "nome": "User B",
        "email": "user_b@example.com",
        "senha": "password",
        "perfil": "COLABORADOR"
    })
    res = client.put(f"/usuarios/{user_id}", json={
        "nome": "User A Updated",
        "email": "user_b@example.com",
        "perfil": "LIDER"
    })
    assert res.status_code == 409

    # 5. PATCH Desativar
    res = client.patch(f"/usuarios/{user_id}/desativar")
    assert res.status_code == 200
    assert res.get_json()["ativo"] is False


def test_competencias_crud(client):
    # 1. POST Create
    res = client.post("/competencias", json={
        "nome": "Python Programming",
        "tipo": "TECNICA",
        "descricao": "Coding",
        "peso": 2.0
    })
    assert res.status_code == 201
    comp = res.get_json()
    assert comp["nome"] == "Python Programming"
    assert comp["tipo"] == "TECNICA"
    assert comp["ativo"] is True
    comp_id = comp["id"]

    # 2. GET by id
    res = client.get(f"/competencias/{comp_id}")
    assert res.status_code == 200
    assert res.get_json()["nome"] == "Python Programming"

    # GET non-existent
    res = client.get("/competencias/999")
    assert res.status_code == 404

    # 3. GET list
    res = client.get("/competencias")
    assert res.status_code == 200
    assert len(res.get_json()) == 1

    # 4. PUT Update
    res = client.put(f"/competencias/{comp_id}", json={
        "nome": "Python Advanced",
        "tipo": "TECNICA",
        "descricao": "Coding Adv",
        "peso": 3.0
    })
    assert res.status_code == 200
    comp_put = res.get_json()
    assert comp_put["nome"] == "Python Advanced"
    assert float(comp_put["peso"]) == 3.0

    # 5. PATCH Desativar
    res = client.patch(f"/competencias/{comp_id}/desativar")
    assert res.status_code == 200
    assert res.get_json()["ativo"] is False


def test_setor_put_errors_and_routing(client):
    # 1. PUT /setores/{id} existente retorna 200
    res = client.post("/setores", json={"nome": "TI", "descricao": "Tecnologia"})
    assert res.status_code == 201
    setor_id = res.get_json()["id"]

    res = client.put(f"/setores/{setor_id}", json={"nome": "TI Atualizado", "descricao": "TI Novo"})
    assert res.status_code == 200

    # 2. PUT /setores/{id} inexistente retorna 404
    res = client.put("/setores/999", json={"nome": "Inexistente", "descricao": "Nao existe"})
    assert res.status_code == 404

    # 3. rota inexistente retorna 404, não 500
    res = client.get("/rotas_totalmente_inexistentes")
    assert res.status_code == 404
    assert res.get_json()["error"] != "INTERNAL_SERVER_ERROR"


def test_cadastro_reactivations(client):
    # Setores
    res = client.post("/setores", json={"nome": "Comercial", "descricao": "Vendas"})
    assert res.status_code == 201
    setor_id = res.get_json()["id"]

    # Desativar
    client.patch(f"/setores/{setor_id}/desativar")
    # 1. Reativar setor inativo retorna 200
    res = client.patch(f"/setores/{setor_id}/ativar")
    assert res.status_code == 200
    assert res.get_json()["ativo"] is True

    # 2. Reativar setor já ativo retorna 200
    res = client.patch(f"/setores/{setor_id}/ativar")
    assert res.status_code == 200
    assert res.get_json()["ativo"] is True

    # 3. Reativar setor inexistente retorna 404
    res = client.patch("/setores/999/ativar")
    assert res.status_code == 404

    # Funcoes
    res = client.post("/funcoes", json={"nome": "Analista", "descricao": "Negocios", "setor_id": setor_id})
    assert res.status_code == 201
    funcao_id = res.get_json()["id"]

    # Desativar
    client.patch(f"/funcoes/{funcao_id}/desativar")
    # 1. Reativar função inativa retorna 200
    res = client.patch(f"/funcoes/{funcao_id}/ativar")
    assert res.status_code == 200
    assert res.get_json()["ativo"] is True

    # 2. Reativar função já ativa retorna 200
    res = client.patch(f"/funcoes/{funcao_id}/ativar")
    assert res.status_code == 200
    assert res.get_json()["ativo"] is True

    # 3. Reativar função inexistente retorna 404
    res = client.patch("/funcoes/999/ativar")
    assert res.status_code == 404

    # Usuarios
    res = client.post("/usuarios", json={"nome": "User1", "email": "user1@company.com", "perfil": "ADMIN", "senha": "pwd"})
    assert res.status_code == 201
    usuario_id = res.get_json()["id"]

    # Desativar
    client.patch(f"/usuarios/{usuario_id}/desativar")
    # 1. Reativar usuário inativo retorna 200
    res = client.patch(f"/usuarios/{usuario_id}/ativar")
    assert res.status_code == 200
    assert res.get_json()["ativo"] is True

    # 2. Reativar usuário já ativo retorna 200
    res = client.patch(f"/usuarios/{usuario_id}/ativar")
    assert res.status_code == 200
    assert res.get_json()["ativo"] is True

    # 3. Reativar usuário inexistente retorna 404
    res = client.patch("/usuarios/999/ativar")
    assert res.status_code == 404

    # Competencias
    res = client.post("/competencias", json={"nome": "SQL", "tipo": "TECNICA", "peso": 2.0})
    assert res.status_code == 201
    competencia_id = res.get_json()["id"]

    # Desativar
    client.patch(f"/competencias/{competencia_id}/desativar")
    # 1. Reativar competência inativa retorna 200
    res = client.patch(f"/competencias/{competencia_id}/ativar")
    assert res.status_code == 200
    assert res.get_json()["ativo"] is True

    # 2. Reativar competência já ativa retorna 200
    res = client.patch(f"/competencias/{competencia_id}/ativar")
    assert res.status_code == 200
    assert res.get_json()["ativo"] is True

    # 3. Reativar competência inexistente retorna 404
    res = client.patch("/competencias/999/ativar")
    assert res.status_code == 404

