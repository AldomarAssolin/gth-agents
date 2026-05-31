import json
import os
from datetime import date
import pytest
from app import create_app
from app.config import Config
from app.extensions import db
from domain.enums.perfil_usuario import PerfilUsuario
from infrastructure.database.base import Base
from infrastructure.database.models.usuario_model import UsuarioModel
from infrastructure.database.models.colaborador_model import ColaboradorModel
from infrastructure.database.models.setor_model import SetorModel
from infrastructure.database.models.funcao_model import FuncaoModel
from werkzeug.security import generate_password_hash


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


def seed_data(app):
    with app.app_context():
        setor1 = SetorModel(nome="Engenharia", descricao="Eng")
        setor2 = SetorModel(nome="Marketing", descricao="Mkt")
        db.session.add_all([setor1, setor2])
        db.session.commit()

        funcao1 = FuncaoModel(nome="Desenvolvedor", descricao="Devs")

        db.session.add(funcao1)
        db.session.commit()

        colab1 = ColaboradorModel(
            nome="Colaborador A",
            matricula="M001",
            email="colabA@test.com",
            data_admissao=date(2026, 1, 1),
            status="ATIVO",
            setor_id=setor1.id,
            funcao_id=funcao1.id,
        )
        colab2 = ColaboradorModel(
            nome="Colaborador B",
            matricula="M002",
            email="colabB@test.com",
            data_admissao=date(2026, 1, 1),
            status="ATIVO",
            setor_id=setor2.id,
            funcao_id=funcao1.id,
        )
        db.session.add_all([colab1, colab2])
        db.session.commit()

        admin = UsuarioModel(
            nome="Admin",
            email="admin@test.com",
            senha_hash=generate_password_hash("admin123"),
            perfil=PerfilUsuario.ADMIN.value,
            ativo=True,
        )
        rh = UsuarioModel(
            nome="RH",
            email="rh@test.com",
            senha_hash=generate_password_hash("rh123"),
            perfil=PerfilUsuario.RH.value,
            ativo=True,
        )
        lider_a = UsuarioModel(
            nome="Lider A",
            email="lidera@test.com",
            senha_hash=generate_password_hash("lider123"),
            perfil=PerfilUsuario.LIDER.value,
            ativo=True,
            setor_id=setor1.id,
        )
        lider_sem_setor = UsuarioModel(
            nome="Lider B",
            email="liderb@test.com",
            senha_hash=generate_password_hash("lider123"),
            perfil=PerfilUsuario.LIDER.value,
            ativo=True,
            setor_id=None,
        )
        colab_a = UsuarioModel(
            nome="Colab A",
            email="colaba_u@test.com",
            senha_hash=generate_password_hash("colab123"),
            perfil=PerfilUsuario.COLABORADOR.value,
            ativo=True,
            colaborador_id=colab1.id,
        )
        colab_sem_id = UsuarioModel(
            nome="Colab Sem ID",
            email="colab_sem_id@test.com",
            senha_hash=generate_password_hash("colab123"),
            perfil=PerfilUsuario.COLABORADOR.value,
            ativo=True,
            colaborador_id=None,
        )
        db.session.add_all([admin, rh, lider_a, lider_sem_setor, colab_a, colab_sem_id])
        db.session.commit()

        return {
            "colab1_id": colab1.id,
            "colab2_id": colab2.id,
            "setor1_id": setor1.id,
            "setor2_id": setor2.id,
            "funcao1_id": funcao1.id,
        }


def get_token(client, email, password):
    res = client.post("/auth/login", json={"email": email, "senha": password})
    assert res.status_code == 200
    return res.get_json()["access_token"]


# 1. COLABORADOR acessa seus próprios dados.
def test_colaborador_acessa_proprios_dados(client):
    ids = seed_data(client.application)
    token = get_token(client, "colaba_u@test.com", "colab123")

    res = client.get(
        f"/colaboradores/{ids['colab1_id']}",
        headers={"X-Enforce-Auth": "true", "Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200
    assert res.get_json()["nome"] == "Colaborador A"


# 2. COLABORADOR não acessa dados de outro colaborador.
def test_colaborador_nao_acessa_dados_alheios(client):
    ids = seed_data(client.application)
    token = get_token(client, "colaba_u@test.com", "colab123")

    res = client.get(
        f"/colaboradores/{ids['colab2_id']}",
        headers={"X-Enforce-Auth": "true", "Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 403
    assert res.get_json()["error"] == "FORBIDDEN"


# 3. COLABORADOR sem colaborador_id recebe 403.
def test_colaborador_sem_id_recebe_403(client):
    ids = seed_data(client.application)
    token = get_token(client, "colab_sem_id@test.com", "colab123")

    res = client.get(
        f"/colaboradores/{ids['colab1_id']}",
        headers={"X-Enforce-Auth": "true", "Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 403
    assert res.get_json()["error"] == "FORBIDDEN"

    # Test list too
    res = client.get(
        "/colaboradores",
        headers={"X-Enforce-Auth": "true", "Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 403


# 4. LIDER acessa colaborador do seu setor.
def test_lider_acessa_colaborador_do_setor(client):
    ids = seed_data(client.application)
    token = get_token(client, "lidera@test.com", "lider123")

    res = client.get(
        f"/colaboradores/{ids['colab1_id']}",
        headers={"X-Enforce-Auth": "true", "Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200
    assert res.get_json()["nome"] == "Colaborador A"


# 5. LIDER não acessa colaborador de outro setor.
def test_lider_nao_acessa_colaborador_de_outro_setor(client):
    ids = seed_data(client.application)
    token = get_token(client, "lidera@test.com", "lider123")

    res = client.get(
        f"/colaboradores/{ids['colab2_id']}",
        headers={"X-Enforce-Auth": "true", "Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 403
    assert res.get_json()["error"] == "FORBIDDEN"


# 6. LIDER sem setor_id recebe 403.
def test_lider_sem_setor_recebe_403(client):
    ids = seed_data(client.application)
    token = get_token(client, "liderb@test.com", "lider123")

    res = client.get(
        f"/colaboradores/{ids['colab1_id']}",
        headers={"X-Enforce-Auth": "true", "Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 403
    assert res.get_json()["error"] == "FORBIDDEN"


# 7. RH acessa qualquer colaborador.
def test_rh_acessa_qualquer_colaborador(client):
    ids = seed_data(client.application)
    token = get_token(client, "rh@test.com", "rh123")

    res1 = client.get(
        f"/colaboradores/{ids['colab1_id']}",
        headers={"X-Enforce-Auth": "true", "Authorization": f"Bearer {token}"},
    )
    assert res1.status_code == 200

    res2 = client.get(
        f"/colaboradores/{ids['colab2_id']}",
        headers={"X-Enforce-Auth": "true", "Authorization": f"Bearer {token}"},
    )
    assert res2.status_code == 200


# 8. ADMIN acessa qualquer colaborador.
def test_admin_acessa_qualquer_colaborador(client):
    ids = seed_data(client.application)
    token = get_token(client, "admin@test.com", "admin123")

    res1 = client.get(
        f"/colaboradores/{ids['colab1_id']}",
        headers={"X-Enforce-Auth": "true", "Authorization": f"Bearer {token}"},
    )
    assert res1.status_code == 200

    res2 = client.get(
        f"/colaboradores/{ids['colab2_id']}",
        headers={"X-Enforce-Auth": "true", "Authorization": f"Bearer {token}"},
    )
    assert res2.status_code == 200


# 9. Rota protegida sem token retorna 401.
def test_rota_protegida_sem_token(client):
    ids = seed_data(client.application)
    res = client.get(
        f"/colaboradores/{ids['colab1_id']}",
        headers={"X-Enforce-Auth": "true"},
    )
    assert res.status_code == 401
    assert res.get_json()["error"] == "UNAUTHORIZED"


# 10. Token válido com perfil insuficiente retorna 403.
def test_token_valido_perfil_insuficiente(client):
    ids = seed_data(client.application)
    token = get_token(client, "colaba_u@test.com", "colab123")

    # Colaborador trying to register evaluation
    eval_payload = {
        "colaborador_id": ids["colab1_id"],
        "tipo": "DESEMPENHO",
        "observacao_geral": "Boa performance",
        "itens": [],
    }
    res = client.post(
        "/avaliacoes",
        json=eval_payload,
        headers={"X-Enforce-Auth": "true", "Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 403
    assert res.get_json()["error"] == "FORBIDDEN"


# 11. Atualização fora do escopo retorna 403.
def test_atualizacao_fora_do_escopo(client):
    ids = seed_data(client.application)
    token = get_token(client, "lidera@test.com", "lider123")

    # Leader A trying to update Colab B (sector 2)
    update_payload = {
        "nome": "Colaborador B Atualizado",
        "matricula": "M002",
        "email": "colabB@test.com",
        "data_admissao": "2026-01-01",
        "setor_id": ids["setor2_id"],
        "funcao_id": ids["funcao1_id"],
    }
    res = client.put(
        f"/colaboradores/{ids['colab2_id']}",
        json=update_payload,
        headers={"X-Enforce-Auth": "true", "Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 403
    assert res.get_json()["error"] == "FORBIDDEN"


# 12. Desativação fora do escopo retorna 403.
def test_desativacao_fora_do_escopo(client):
    ids = seed_data(client.application)
    token = get_token(client, "lidera@test.com", "lider123")

    # Leader A trying to deactivate Colab B (sector 2)
    res = client.patch(
        f"/colaboradores/{ids['colab2_id']}/inativar",
        headers={"X-Enforce-Auth": "true", "Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 403
    assert res.get_json()["error"] == "FORBIDDEN"


# 13. Ativação fora do escopo retorna 403.
def test_ativacao_fora_do_escopo(client):
    ids = seed_data(client.application)
    token = get_token(client, "lidera@test.com", "lider123")

    # Leader A trying to activate Colab B (sector 2)
    res = client.patch(
        f"/colaboradores/{ids['colab2_id']}/ativar",
        headers={"X-Enforce-Auth": "true", "Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 403
    assert res.get_json()["error"] == "FORBIDDEN"
