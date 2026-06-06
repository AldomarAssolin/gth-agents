import pytest
from app import create_app
from app.config import Config
from app.extensions import db
from infrastructure.database.base import Base


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


def test_colaborador_crud_and_status_transitions(client):
    # Setup: Criar setor e funcao obrigatórios
    res = client.post("/setores", json={"nome": "Engenharia", "descricao": "Eng"})
    assert res.status_code == 201
    setor_id = res.get_json()["id"]

    res = client.post("/funcoes", json={"nome": "Software Engineer", "descricao": "Devs", "setor_id": setor_id})
    assert res.status_code == 201
    funcao_id = res.get_json()["id"]

    # 1. GET List (vazio inicialmente)
    res = client.get("/colaboradores")
    assert res.status_code == 200
    assert res.get_json() == []

    # 2. POST Create Colaborador
    colab_payload = {
        "nome": "Alice Smith",
        "matricula": "M12345",
        "email": "alice@company.com",
        "data_admissao": "2026-01-15",
        "setor_id": setor_id,
        "funcao_id": funcao_id,
    }
    res = client.post("/colaboradores", json=colab_payload)
    assert res.status_code == 201
    alice = res.get_json()
    assert alice["nome"] == "Alice Smith"
    assert alice["status"] == "ATIVO"
    alice_id = alice["id"]

    # 3. GET List (agora contendo 1)
    res = client.get("/colaboradores")
    assert res.status_code == 200
    colaboradores = res.get_json()
    assert len(colaboradores) == 1
    assert colaboradores[0]["id"] == alice_id

    # 4. GET by ID existente e inexistente
    res = client.get(f"/colaboradores/{alice_id}")
    assert res.status_code == 200
    assert res.get_json()["matricula"] == "M12345"

    res = client.get("/colaboradores/999")
    assert res.status_code == 404

    # 5. PUT Update existente e inexistente/erros
    update_payload = {
        "nome": "Alice S. Smith",
        "matricula": "M12345",
        "email": "alice.smith@company.com",
        "data_admissao": "2026-01-15",
        "setor_id": setor_id,
        "funcao_id": funcao_id,
    }
    res = client.put(f"/colaboradores/{alice_id}", json=update_payload)
    assert res.status_code == 200
    alice_updated = res.get_json()
    assert alice_updated["nome"] == "Alice S. Smith"
    assert alice_updated["email"] == "alice.smith@company.com"

    res = client.put("/colaboradores/999", json=update_payload)
    assert res.status_code == 404

    # Conflito de matricula
    # Criar outro colaborador
    res = client.post("/colaboradores", json={
        "nome": "Bob Jones",
        "matricula": "M67890",
        "email": "bob@company.com",
        "data_admissao": "2026-02-10",
        "setor_id": setor_id,
        "funcao_id": funcao_id,
    })
    assert res.status_code == 201
    bob_id = res.get_json()["id"]

    # Tentar atualizar Bob com a matricula de Alice
    res = client.put(f"/colaboradores/{bob_id}", json={
        "nome": "Bob Jones",
        "matricula": "M12345", # Conflito com Alice
        "email": "bob@company.com",
        "data_admissao": "2026-02-10",
        "setor_id": setor_id,
        "funcao_id": funcao_id,
    })
    assert res.status_code == 409

    # 6. Transições de Status
    # Inativar
    res = client.patch(f"/colaboradores/{alice_id}/inativar")
    assert res.status_code == 200
    assert res.get_json()["status"] == "INATIVO"

    # Afastar
    res = client.patch(f"/colaboradores/{alice_id}/afastar")
    assert res.status_code == 200
    assert res.get_json()["status"] == "AFASTADO"

    # Desligar
    res = client.patch(f"/colaboradores/{alice_id}/desligar")
    assert res.status_code == 200
    assert res.get_json()["status"] == "DESLIGADO"

    # Ativar novamente
    res = client.patch(f"/colaboradores/{alice_id}/ativar")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ATIVO"

    # Testar erros de status para id inexistente
    res = client.patch("/colaboradores/999/ativar")
    assert res.status_code == 404
