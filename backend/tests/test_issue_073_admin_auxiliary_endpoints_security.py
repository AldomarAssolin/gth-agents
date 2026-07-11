import json
import pytest
from flask import g
from app import create_app
from app.config import Config
from app.extensions import db
from domain.enums.perfil_usuario import PerfilUsuario
from infrastructure.database.base import Base
from infrastructure.database.models.usuario_model import UsuarioModel
from infrastructure.database.models.setor_model import SetorModel
from infrastructure.database.models.funcao_model import FuncaoModel
from infrastructure.database.models.competencia_model import CompetenciaModel
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


def reset_db(app):
    with app.app_context():
        db.session.remove()
        Base.metadata.drop_all(db.engine)
        Base.metadata.create_all(db.engine)


def seed_data(app):
    with app.app_context():
        # 1. Sementes para evitar 404/409 nos testes
        setor = SetorModel(nome="TI", descricao="Tecnologia da Informacao")
        db.session.add(setor)
        db.session.commit()

        funcao = FuncaoModel(nome="Programador", descricao="Escreve codigo")
        db.session.add(funcao)
        db.session.commit()

        competencia = CompetenciaModel(
            nome="Python",
            descricao="Linguagem basica",
            tipo="TECNICA",
            peso=2.0,
            ativo=True
        )
        db.session.add(competencia)
        db.session.commit()

        # 2. Usuários para Login e Perfis do JWT
        admin = UsuarioModel(
            nome="Administrador",
            email="admin@test.com",
            senha_hash=generate_password_hash("admin123"),
            perfil=PerfilUsuario.ADMIN.value,
            ativo=True,
        )
        rh = UsuarioModel(
            nome="Recursos Humanos",
            email="rh@test.com",
            senha_hash=generate_password_hash("rh123"),
            perfil=PerfilUsuario.RH.value,
            ativo=True,
        )
        lider = UsuarioModel(
            nome="Lider de Equipe",
            email="lider@test.com",
            senha_hash=generate_password_hash("lider123"),
            perfil=PerfilUsuario.LIDER.value,
            ativo=True,
            setor_id=setor.id,
        )
        colab = UsuarioModel(
            nome="Colaborador",
            email="colab@test.com",
            senha_hash=generate_password_hash("colab123"),
            perfil=PerfilUsuario.COLABORADOR.value,
            ativo=True,
        )
        db.session.add_all([admin, rh, lider, colab])
        db.session.commit()

        return {
            "setor_id": setor.id,
            "funcao_id": funcao.id,
            "competencia_id": competencia.id,
            "usuario_id": colab.id,
            "admin_email": "admin@test.com",
            "rh_email": "rh@test.com",
            "lider_email": "lider@test.com",
            "colab_email": "colab@test.com",
        }


def get_token(client, email):
    if hasattr(g, "usuario"):
        g.usuario = None

    password = "admin123" if "admin" in email else (
        "rh123" if "rh" in email else (
            "lider123" if "lider" in email else "colab123"
        )
    )
    res = client.post("/auth/login", json={"email": email, "senha": password})
    assert res.status_code == 200
    return res.get_json()["access_token"]


def make_request(client, method, url, json_data=None, token=None):
    if hasattr(g, "usuario"):
        g.usuario = None

    headers = {"X-Enforce-Auth": "true"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    if method == "GET":
        return client.get(url, headers=headers)
    elif method == "POST":
        return client.post(url, json=json_data, headers=headers)
    elif method == "PUT":
        return client.put(url, json=json_data, headers=headers)
    elif method == "PATCH":
        return client.patch(url, json=json_data, headers=headers)
    raise ValueError(f"Unknown method {method}")


# Matriz de Parâmetros para 24 rotas
ROUTES_MATRIX = [
    # Setores
    ("GET", "/setores", None, ["ADMIN", "RH", "LIDER", "COLABORADOR"]),
    ("GET", "/setores/{setor_id}", None, ["ADMIN", "RH"]),
    ("POST", "/setores", {"nome": "Setor Novo Unico", "descricao": "Descricao"}, ["ADMIN", "RH"]),
    ("PUT", "/setores/{setor_id}", {"nome": "TI Editado", "descricao": "Nova Desc"}, ["ADMIN", "RH"]),
    ("PATCH", "/setores/{setor_id}/ativar", None, ["ADMIN", "RH"]),
    ("PATCH", "/setores/{setor_id}/desativar", None, ["ADMIN", "RH"]),

    # Funções
    ("GET", "/funcoes", None, ["ADMIN", "RH", "LIDER", "COLABORADOR"]),
    ("GET", "/funcoes/{funcao_id}", None, ["ADMIN", "RH"]),
    ("POST", "/funcoes", {"nome": "Funcao Nova Unica", "descricao": "Descricao"}, ["ADMIN", "RH"]),
    ("PUT", "/funcoes/{funcao_id}", {"nome": "Programador Editado", "descricao": "Nova Desc"}, ["ADMIN", "RH"]),
    ("PATCH", "/funcoes/{funcao_id}/ativar", None, ["ADMIN", "RH"]),
    ("PATCH", "/funcoes/{funcao_id}/desativar", None, ["ADMIN", "RH"]),

    # Usuários
    ("GET", "/usuarios", None, ["ADMIN", "RH"]),
    ("GET", "/usuarios/{usuario_id}", None, ["ADMIN", "RH"]),
    ("POST", "/usuarios", {"nome": "User Novo Unico", "email": "new_unique_user@test.com", "senha": "password123", "perfil": "COLABORADOR"}, ["ADMIN", "RH"]),
    ("PUT", "/usuarios/{usuario_id}", {"nome": "Colab Editado", "email": "colab_editado@test.com", "perfil": "COLABORADOR"}, ["ADMIN", "RH"]),
    ("PATCH", "/usuarios/{usuario_id}/ativar", None, ["ADMIN", "RH"]),
    ("PATCH", "/usuarios/{usuario_id}/desativar", None, ["ADMIN", "RH"]),

    # Competências
    ("GET", "/competencias", None, ["ADMIN", "RH", "LIDER", "COLABORADOR"]),
    ("GET", "/competencias/{competencia_id}", None, ["ADMIN", "RH"]),
    ("POST", "/competencias", {"nome": "Competencia Nova Unica", "tipo": "TECNICA", "descricao": "Desc", "peso": 1.5}, ["ADMIN", "RH"]),
    ("PUT", "/competencias/{competencia_id}", {"nome": "Python Editada", "tipo": "TECNICA", "descricao": "Nova Desc", "peso": 2.5}, ["ADMIN", "RH"]),
    ("PATCH", "/competencias/{competencia_id}/ativar", None, ["ADMIN", "RH"]),
    ("PATCH", "/competencias/{competencia_id}/desativar", None, ["ADMIN", "RH"]),
]


@pytest.mark.parametrize("method, url_tpl, payload, allowed_roles", ROUTES_MATRIX)
def test_issue_073_autenticacao_e_autorizacao_parametrizada(client, method, url_tpl, payload, allowed_roles):
    # 1. Sem token JWT -> HTTP 401 Unauthorized
    reset_db(client.application)
    seeds = seed_data(client.application)
    url = url_tpl.format(
        setor_id=seeds["setor_id"],
        funcao_id=seeds["funcao_id"],
        usuario_id=seeds["usuario_id"],
        competencia_id=seeds["competencia_id"]
    )
    res_no_auth = make_request(client, method, url, payload)
    assert res_no_auth.status_code == 401
    assert res_no_auth.get_json()["error"] == "UNAUTHORIZED"

    # 2. Com token -> Validar controle de acesso por papel
    profiles = [
        ("ADMIN", "admin@test.com"),
        ("RH", "rh@test.com"),
        ("LIDER", "lider@test.com"),
        ("COLABORADOR", "colab@test.com"),
    ]

    for role_name, email in profiles:
        reset_db(client.application)
        seeds = seed_data(client.application)
        url = url_tpl.format(
            setor_id=seeds["setor_id"],
            funcao_id=seeds["funcao_id"],
            usuario_id=seeds["usuario_id"],
            competencia_id=seeds["competencia_id"]
        )
        token = get_token(client, email)
        res = make_request(client, method, url, payload, token)

        if role_name in allowed_roles:
            # Operação permitida
            assert res.status_code in (200, 201)
        else:
            # Operação proibida -> HTTP 403 Forbidden
            assert res.status_code == 403
            assert res.get_json()["error"] == "FORBIDDEN"


def test_issue_073_mitigacao_spoofing_perfil(client):
    reset_db(client.application)
    seeds = seed_data(client.application)
    colab_token = get_token(client, seeds["colab_email"])

    # Simular requisição de criação de setor enviando dados com "perfil" ou tentativa de spoofing
    payload = {"nome": "Setor Invisivel", "descricao": "Tentativa de Spoofing"}

    # 1. COLABORADOR tenta cadastrar informando que é ADMIN no payload (ou similar)
    res = make_request(client, "POST", "/setores", payload, colab_token)
    assert res.status_code == 403

    # Garantir que o perfil considerado para acesso é estritamente o do JWT decodificado
    with client.application.app_context():
        setor = db.session.query(SetorModel).filter_by(nome="Setor Invisivel").first()
        assert setor is None


def test_issue_073_bloqueios_sem_persistencia(client):
    reset_db(client.application)
    seeds = seed_data(client.application)
    colab_token = get_token(client, seeds["colab_email"])

    # 1. POST Setores negado não deve persistir
    make_request(client, "POST", "/setores", {"nome": "Novo Setor Invalido"}, colab_token)
    with client.application.app_context():
        assert db.session.query(SetorModel).filter_by(nome="Novo Setor Invalido").first() is None

    # 2. PUT Setores negado não deve alterar o registro original
    make_request(client, "PUT", f"/setores/{seeds['setor_id']}", {"nome": "TI Alterado Invalido"}, colab_token)
    with client.application.app_context():
        setor = db.session.query(SetorModel).filter_by(id=seeds["setor_id"]).first()
        assert setor.nome == "TI"

    # 3. PATCH desativar setor negado não deve alterar o status
    make_request(client, "PATCH", f"/setores/{seeds['setor_id']}/desativar", None, colab_token)
    with client.application.app_context():
        setor = db.session.query(SetorModel).filter_by(id=seeds["setor_id"]).first()
        assert setor.ativo is True


def test_issue_073_usuarios_serialization_security(client):
    reset_db(client.application)
    seeds = seed_data(client.application)
    admin_token = get_token(client, seeds["admin_email"])

    # 1. GET Listagem não deve expor senhas
    res_list = make_request(client, "GET", "/usuarios", None, admin_token)
    assert res_list.status_code == 200
    for user_data in res_list.get_json():
        assert "senha" not in user_data
        assert "senha_hash" not in user_data

    # 2. GET Obter Individual não deve expor senhas
    res_get = make_request(client, "GET", f"/usuarios/{seeds['usuario_id']}", None, admin_token)
    assert res_get.status_code == 200
    user_data = res_get.get_json()
    assert "senha" not in user_data
    assert "senha_hash" not in user_data

    # 3. POST Criar não deve expor senhas
    payload_create = {
        "nome": "Usuario de Teste Senha",
        "email": "user_senha@test.com",
        "senha": "senha123",
        "perfil": "COLABORADOR"
    }
    res_create = make_request(client, "POST", "/usuarios", payload_create, admin_token)
    assert res_create.status_code == 201
    created_data = res_create.get_json()
    assert "senha" not in created_data
    assert "senha_hash" not in created_data

    # 4. PUT Atualizar não deve expor senhas
    payload_update = {
        "nome": "Usuario de Teste Senha Editado",
        "email": "colab_editado@test.com",
        "perfil": "LIDER"
    }
    res_update = make_request(client, "PUT", f"/usuarios/{seeds['usuario_id']}", payload_update, admin_token)
    assert res_update.status_code == 200
    updated_data = res_update.get_json()
    assert "senha" not in updated_data
    assert "senha_hash" not in updated_data


def test_issue_073_regressao_operacional_leituras(client):
    reset_db(client.application)
    seeds = seed_data(client.application)
    colab_token = get_token(client, seeds["colab_email"])
    lider_token = get_token(client, seeds["lider_email"])

    # 1. Listagem de setores por Colaborador e Líder (necessários para páginas e formulários)
    assert make_request(client, "GET", "/setores", None, colab_token).status_code == 200
    assert make_request(client, "GET", "/setores", None, lider_token).status_code == 200

    # 2. Listagem de funções por Colaborador e Líder
    assert make_request(client, "GET", "/funcoes", None, colab_token).status_code == 200
    assert make_request(client, "GET", "/funcoes", None, lider_token).status_code == 200

    # 3. Listagem de competências por Colaborador e Líder
    assert make_request(client, "GET", "/competencias", None, colab_token).status_code == 200
    assert make_request(client, "GET", "/competencias", None, lider_token).status_code == 200
