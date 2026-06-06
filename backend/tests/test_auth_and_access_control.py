import json
import os
from datetime import datetime, timedelta, timezone
import jwt
import pytest
from app import create_app
from app.config import Config
from app.extensions import db
from domain.enums.perfil_usuario import PerfilUsuario
from infrastructure.database.base import Base
from infrastructure.database.models.usuario_model import UsuarioModel
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


def seed_users(app):
    with app.app_context():
        admin_pw = generate_password_hash("admin123")
        rh_pw = generate_password_hash("rh123")
        colab_pw = generate_password_hash("colab123")
        inactive_pw = generate_password_hash("inactive123")

        admin = UsuarioModel(
            nome="Admin User",
            email="admin@test.com",
            senha_hash=admin_pw,
            perfil=PerfilUsuario.ADMIN.value,
            ativo=True,
        )
        rh = UsuarioModel(
            nome="RH User",
            email="rh@test.com",
            senha_hash=rh_pw,
            perfil=PerfilUsuario.RH.value,
            ativo=True,
        )
        colab = UsuarioModel(
            nome="Colab User",
            email="colab@test.com",
            senha_hash=colab_pw,
            perfil=PerfilUsuario.COLABORADOR.value,
            ativo=True,
        )
        inactive = UsuarioModel(
            nome="Inactive User",
            email="inactive@test.com",
            senha_hash=inactive_pw,
            perfil=PerfilUsuario.COLABORADOR.value,
            ativo=False,
        )

        db.session.add_all([admin, rh, colab, inactive])
        db.session.commit()


def test_login_valido(client):
    seed_users(client.application)

    payload = {"email": "admin@test.com", "senha": "admin123"}
    res = client.post("/auth/login", json=payload)
    assert res.status_code == 200

    data = res.get_json()
    assert "access_token" in data
    assert data["token_type"] == "Bearer"
    assert data["usuario"]["email"] == "admin@test.com"
    assert data["usuario"]["perfil"] == "ADMIN"
    assert "senha" not in data["usuario"]
    assert "senha_hash" not in data["usuario"]


def test_login_invalido_senha(client):
    seed_users(client.application)

    payload = {"email": "admin@test.com", "senha": "senha-incorreta"}
    res = client.post("/auth/login", json=payload)
    assert res.status_code == 401
    assert res.get_json()["error"] == "UNAUTHORIZED"


def test_login_invalido_email(client):
    seed_users(client.application)

    payload = {"email": "naoexiste@test.com", "senha": "senha"}
    res = client.post("/auth/login", json=payload)
    assert res.status_code == 401
    assert res.get_json()["error"] == "UNAUTHORIZED"


def test_login_usuario_inativo(client):
    seed_users(client.application)

    payload = {"email": "inactive@test.com", "senha": "inactive123"}
    res = client.post("/auth/login", json=payload)
    assert res.status_code == 403
    assert res.get_json()["error"] == "FORBIDDEN"


def test_rota_protegida_sem_token(client):
    res = client.post("/usuarios", json={}, headers={"X-Enforce-Auth": "true"})
    assert res.status_code == 401
    assert res.get_json()["error"] == "UNAUTHORIZED"


def test_rota_protegida_token_invalido(client):
    res = client.post(
        "/usuarios",
        json={},
        headers={
            "X-Enforce-Auth": "true",
            "Authorization": "Bearer token-invalido-qualquer",
        },
    )
    assert res.status_code == 401
    assert res.get_json()["error"] == "UNAUTHORIZED"


def test_rota_protegida_token_expirado(client):
    secret = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret-change-me")
    algorithm = os.getenv("JWT_ALGORITHM", "HS256")

    expired_time = datetime.now(timezone.utc) - timedelta(minutes=10)
    payload = {
        "id": 1,
        "email": "admin@test.com",
        "perfil": "ADMIN",
        "iat": expired_time - timedelta(minutes=1),
        "exp": expired_time,
    }
    expired_token = jwt.encode(payload, secret, algorithm=algorithm)

    res = client.post(
        "/usuarios",
        json={},
        headers={
            "X-Enforce-Auth": "true",
            "Authorization": f"Bearer {expired_token}",
        },
    )
    assert res.status_code == 401
    assert res.get_json()["error"] == "UNAUTHORIZED"
    assert "expirado" in res.get_json()["message"].lower()


def test_rota_administrativa_perfil_insuficiente(client):
    seed_users(client.application)

    login_res = client.post(
        "/auth/login", json={"email": "colab@test.com", "senha": "colab123"}
    )
    token = login_res.get_json()["access_token"]

    res = client.post(
        "/setores",
        json={"nome": "TI", "descricao": "Tecnologia"},
        headers={"X-Enforce-Auth": "true", "Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 403
    assert res.get_json()["error"] == "FORBIDDEN"


def test_rota_administrativa_com_admin(client):
    seed_users(client.application)

    login_res = client.post(
        "/auth/login", json={"email": "admin@test.com", "senha": "admin123"}
    )
    token = login_res.get_json()["access_token"]

    res = client.post(
        "/setores",
        json={"nome": "TI", "descricao": "Tecnologia"},
        headers={"X-Enforce-Auth": "true", "Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 201
    assert res.get_json()["nome"] == "TI"


def test_rota_administrativa_com_rh(client):
    seed_users(client.application)

    login_res = client.post(
        "/auth/login", json={"email": "rh@test.com", "senha": "rh123"}
    )
    token = login_res.get_json()["access_token"]

    res = client.post(
        "/setores",
        json={"nome": "TI", "descricao": "Tecnologia"},
        headers={"X-Enforce-Auth": "true", "Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 201
    assert res.get_json()["nome"] == "TI"
