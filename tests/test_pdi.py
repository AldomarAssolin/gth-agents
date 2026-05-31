import json
import os
from datetime import date, datetime
import pytest
from flask import g
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
        lider_b = UsuarioModel(
            nome="Lider B",
            email="liderb@test.com",
            senha_hash=generate_password_hash("lider123"),
            perfil=PerfilUsuario.LIDER.value,
            ativo=True,
            setor_id=setor2.id,
        )
        colab_a = UsuarioModel(
            nome="Colab A",
            email="colaba_u@test.com",
            senha_hash=generate_password_hash("colab123"),
            perfil=PerfilUsuario.COLABORADOR.value,
            ativo=True,
            colaborador_id=colab1.id,
        )
        colab_b = UsuarioModel(
            nome="Colab B",
            email="colabb_u@test.com",
            senha_hash=generate_password_hash("colab123"),
            perfil=PerfilUsuario.COLABORADOR.value,
            ativo=True,
            colaborador_id=colab2.id,
        )
        db.session.add_all([admin, rh, lider_a, lider_b, colab_a, colab_b])
        db.session.commit()

        return {
            "colab1_id": colab1.id,
            "colab2_id": colab2.id,
            "setor1_id": setor1.id,
            "setor2_id": setor2.id,
            "admin_email": "admin@test.com",
            "rh_email": "rh@test.com",
            "lidera_email": "lidera@test.com",
            "liderb_email": "liderb@test.com",
            "colaba_email": "colaba_u@test.com",
            "colabb_email": "colabb_u@test.com",
        }


def get_token(client, email, password=None):
    if hasattr(g, "usuario"):
        g.usuario = None
    if password is None:
        if "admin" in email:
            password = "admin123"
        elif "rh" in email:
            password = "rh123"
        elif "lider" in email:
            password = "lider123"
        else:
            password = "colab123"
    res = client.post("/auth/login", json={"email": email, "senha": password})
    assert res.status_code == 200
    return res.get_json()["access_token"]


def api_post(client, url, json_data, token=None):
    if hasattr(g, "usuario"):
        g.usuario = None
    headers = {}
    if token:
        headers = {"X-Enforce-Auth": "true", "Authorization": f"Bearer {token}"}
    return client.post(url, json=json_data, headers=headers)


def api_get(client, url, token=None):
    if hasattr(g, "usuario"):
        g.usuario = None
    headers = {}
    if token:
        headers = {"X-Enforce-Auth": "true", "Authorization": f"Bearer {token}"}
    return client.get(url, headers=headers)


def api_patch(client, url, json_data=None, token=None):
    if hasattr(g, "usuario"):
        g.usuario = None
    headers = {}
    if token:
        headers = {"X-Enforce-Auth": "true", "Authorization": f"Bearer {token}"}
    return client.patch(url, json=json_data, headers=headers)


# 1. ADMIN cria PDI para qualquer colaborador.
def test_admin_cria_pdi_para_qualquer_colaborador(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["admin_email"], "admin123")

    payload = {
        "colaborador_id": ids["colab2_id"],
        "titulo": "Plano de Desenvolvimento Backend",
        "descricao": "Melhorar habilidades de Python/Django/Flask",
        "origem": "MANUAL",
        "data_inicio": "2026-06-01",
        "data_fim": "2026-12-01",
        "acoes": [
            {
                "tipo": "TREINAMENTO",
                "descricao": "Curso Avançado de Flask",
                "prazo": "2026-08-01"
            }
        ]
    }
    res = api_post(client, "/pdis", payload, token)
    assert res.status_code == 201
    data = res.get_json()
    assert data["id"] is not None
    assert data["titulo"] == payload["titulo"]
    assert data["status"] == "ATIVO"
    assert len(data["acoes"]) == 1
    assert data["acoes"][0]["status"] == "PENDENTE"


# 2. RH cria PDI para qualquer colaborador.
def test_rh_cria_pdi_para_qualquer_colaborador(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["rh_email"], "rh123")

    payload = {
        "colaborador_id": ids["colab1_id"],
        "titulo": "PDI Soft Skills",
        "descricao": "Melhorar comunicacao e lideranca",
        "origem": "FEEDBACK",
        "data_inicio": "2026-06-01",
        "acoes": []
    }
    res = api_post(client, "/pdis", payload, token)
    assert res.status_code == 201
    assert res.get_json()["titulo"] == payload["titulo"]


# 3. LIDER cria PDI para colaborador do seu setor.
def test_lider_cria_pdi_do_seu_setor(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["lidera_email"], "lider123")

    payload = {
        "colaborador_id": ids["colab1_id"],
        "titulo": "PDI Tecnico Liderado Setor 1",
        "descricao": "Desenvolvimento do profissional do setor",
        "origem": "INDICACAO_LIDER",
        "data_inicio": "2026-06-01",
        "acoes": []
    }
    res = api_post(client, "/pdis", payload, token)
    assert res.status_code == 201
    assert res.get_json()["titulo"] == payload["titulo"]


# 4. LIDER não cria PDI para colaborador de outro setor.
def test_lider_nao_cria_pdi_de_outro_setor(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["lidera_email"], "lider123") # Lider do Setor 1

    payload = {
        "colaborador_id": ids["colab2_id"], # Colaborador do Setor 2
        "titulo": "PDI Nao Autorizado",
        "descricao": "Este PDI nao deve ser criado",
        "origem": "INDICACAO_LIDER",
        "data_inicio": "2026-06-01",
        "acoes": []
    }
    res = api_post(client, "/pdis", payload, token)
    assert res.status_code == 403
    assert res.get_json()["error"] == "FORBIDDEN"


# 5. COLABORADOR não cria PDI.
def test_colaborador_nao_cria_pdi(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["colaba_email"], "colab123")

    payload = {
        "colaborador_id": ids["colab1_id"],
        "titulo": "Meu Proprio PDI",
        "descricao": "Quero me autopromover",
        "origem": "MANUAL",
        "acoes": []
    }
    res = api_post(client, "/pdis", payload, token)
    assert res.status_code == 403
    assert res.get_json()["error"] == "FORBIDDEN"


# 6. COLABORADOR consulta seu próprio PDI.
def test_colaborador_consulta_proprio_pdi(client):
    ids = seed_data(client.application)
    admin_token = get_token(client, ids["admin_email"], "admin123")
    create_res = api_post(
        client,
        "/pdis",
        {
            "colaborador_id": ids["colab1_id"],
            "titulo": "PDI do Colab A",
            "descricao": "Descricao do PDI",
            "origem": "MANUAL",
            "acoes": []
        },
        admin_token
    )
    pdi_id = create_res.get_json()["id"]

    colab_token = get_token(client, ids["colaba_email"], "colab123")
    res = api_get(client, f"/pdis/{pdi_id}", colab_token)
    assert res.status_code == 200
    assert res.get_json()["titulo"] == "PDI do Colab A"

    # Testando tambem o list_pdis do colaborador
    res_list = api_get(client, f"/colaboradores/{ids['colab1_id']}/pdis", colab_token)
    assert res_list.status_code == 200
    assert len(res_list.get_json()) == 1
    assert res_list.get_json()[0]["id"] == pdi_id


# 7. COLABORADOR não consulta PDI de outro colaborador.
def test_colaborador_nao_consulta_pdi_alheio(client):
    ids = seed_data(client.application)
    admin_token = get_token(client, ids["admin_email"], "admin123")
    create_res = api_post(
        client,
        "/pdis",
        {
            "colaborador_id": ids["colab2_id"],
            "titulo": "PDI do Colab B",
            "descricao": "Descricao",
            "acoes": []
        },
        admin_token
    )
    pdi_id = create_res.get_json()["id"]

    colab_token = get_token(client, ids["colaba_email"], "colab123")
    res = api_get(client, f"/pdis/{pdi_id}", colab_token)
    assert res.status_code == 403
    assert res.get_json()["error"] == "FORBIDDEN"

    # Colab A tenta listar os PDI do Colab B
    res_list = api_get(client, f"/colaboradores/{ids['colab2_id']}/pdis", colab_token)
    assert res_list.status_code == 403
    assert res_list.get_json()["error"] == "FORBIDDEN"


# 8. PDI sem título retorna 400.
def test_pdi_sem_titulo_retorna_400(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["admin_email"], "admin123")
    res = api_post(
        client,
        "/pdis",
        {
            "colaborador_id": ids["colab1_id"],
            "titulo": "",
            "descricao": "Descricao",
            "acoes": []
        },
        token
    )
    assert res.status_code == 400
    assert "titulo" in res.get_json()["message"].lower()


# 9. PDI sem descrição retorna 400.
def test_pdi_sem_descricao_retorna_400(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["admin_email"], "admin123")
    res = api_post(
        client,
        "/pdis",
        {
            "colaborador_id": ids["colab1_id"],
            "titulo": "Titulo",
            "descricao": "",
            "acoes": []
        },
        token
    )
    assert res.status_code == 400
    assert "descricao" in res.get_json()["message"].lower()


# 10. PDI com colaborador inexistente retorna 404.
def test_pdi_colaborador_inexistente_retorna_404(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["admin_email"], "admin123")
    res = api_post(
        client,
        "/pdis",
        {
            "colaborador_id": 9999,
            "titulo": "Titulo",
            "descricao": "Descricao",
            "acoes": []
        },
        token
    )
    assert res.status_code == 404
    assert res.get_json()["error"] == "NOT_FOUND"


# 11. PDI com origem inválida retorna 400.
def test_pdi_origem_invalida_retorna_400(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["admin_email"], "admin123")
    res = api_post(
        client,
        "/pdis",
        {
            "colaborador_id": ids["colab1_id"],
            "titulo": "Titulo",
            "descricao": "Descricao",
            "origem": "INVALID_ORIGIN",
            "acoes": []
        },
        token
    )
    assert res.status_code == 400
    assert "origem" in res.get_json()["message"].lower()


# 12. Criar ação de PDI com sucesso.
def test_criar_acao_com_sucesso(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["admin_email"], "admin123")

    create_res = api_post(
        client,
        "/pdis",
        {
            "colaborador_id": ids["colab1_id"],
            "titulo": "PDI com acoes",
            "descricao": "Descricao",
            "acoes": []
        },
        token
    )
    pdi_id = create_res.get_json()["id"]

    res_acao = api_post(
        client,
        f"/pdis/{pdi_id}/acoes",
        {
            "tipo": "MENTORIA",
            "descricao": "Mentoria semanal com dev senior",
            "prazo": "2026-09-01"
        },
        token
    )
    assert res_acao.status_code == 201
    data = res_acao.get_json()
    assert data["id"] is not None
    assert data["tipo"] == "MENTORIA"
    assert data["status"] == "PENDENTE"


# 13. Ação sem descrição retorna 400.
def test_acao_sem_descricao_retorna_400(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["admin_email"], "admin123")

    create_res = api_post(
        client,
        "/pdis",
        {
            "colaborador_id": ids["colab1_id"],
            "titulo": "PDI",
            "descricao": "Desc",
            "acoes": []
        },
        token
    )
    pdi_id = create_res.get_json()["id"]

    res_acao = api_post(
        client,
        f"/pdis/{pdi_id}/acoes",
        {
            "tipo": "MENTORIA",
            "descricao": "",
            "prazo": "2026-09-01"
        },
        token
    )
    assert res_acao.status_code == 400
    assert "descricao" in res_acao.get_json()["message"].lower()


# 14. Ação sem prazo retorna 400.
def test_acao_sem_prazo_retorna_400(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["admin_email"], "admin123")

    create_res = api_post(
        client,
        "/pdis",
        {
            "colaborador_id": ids["colab1_id"],
            "titulo": "PDI",
            "descricao": "Desc",
            "acoes": []
        },
        token
    )
    pdi_id = create_res.get_json()["id"]

    res_acao = api_post(
        client,
        f"/pdis/{pdi_id}/acoes",
        {
            "tipo": "MENTORIA",
            "descricao": "Mentoria",
            "prazo": ""
        },
        token
    )
    assert res_acao.status_code == 400
    assert "prazo" in res_acao.get_json()["message"].lower()


# 15. Concluir ação de PDI com sucesso.
def test_concluir_acao_com_sucesso(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["admin_email"], "admin123")

    create_res = api_post(
        client,
        "/pdis",
        {
            "colaborador_id": ids["colab1_id"],
            "titulo": "PDI",
            "descricao": "Desc",
            "acoes": [
                {
                    "tipo": "LEITURA",
                    "descricao": "Livro Clean Code",
                    "prazo": "2026-08-01"
                }
            ]
        },
        token
    )
    pdi_data = create_res.get_json()
    pdi_id = pdi_data["id"]
    acao_id = pdi_data["acoes"][0]["id"]

    res_concluir = api_patch(
        client,
        f"/pdis/{pdi_id}/acoes/{acao_id}/concluir",
        token=token
    )
    assert res_concluir.status_code == 200
    assert res_concluir.get_json()["status"] == "CONCLUIDA"


# 16. Cancelar ação de PDI com sucesso.
def test_cancelar_acao_com_sucesso(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["admin_email"], "admin123")

    create_res = api_post(
        client,
        "/pdis",
        {
            "colaborador_id": ids["colab1_id"],
            "titulo": "PDI",
            "descricao": "Desc",
            "acoes": [
                {
                    "tipo": "LEITURA",
                    "descricao": "Livro Clean Architecture",
                    "prazo": "2026-08-01"
                }
            ]
        },
        token
    )
    pdi_data = create_res.get_json()
    pdi_id = pdi_data["id"]
    acao_id = pdi_data["acoes"][0]["id"]

    res_cancelar = api_patch(
        client,
        f"/pdis/{pdi_id}/acoes/{acao_id}/cancelar",
        token=token
    )
    assert res_cancelar.status_code == 200
    assert res_cancelar.get_json()["status"] == "CANCELADA"


# 17. Concluir PDI com ações pendentes retorna 400.
def test_concluir_pdi_com_acoes_pendentes_retorna_400(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["admin_email"], "admin123")

    create_res = api_post(
        client,
        "/pdis",
        {
            "colaborador_id": ids["colab1_id"],
            "titulo": "PDI",
            "descricao": "Desc",
            "acoes": [
                {
                    "tipo": "LEITURA",
                    "descricao": "Livro",
                    "prazo": "2026-08-01"
                }
            ]
        },
        token
    )
    pdi_id = create_res.get_json()["id"]

    res_concluir = api_patch(
        client,
        f"/pdis/{pdi_id}/concluir",
        token=token
    )
    assert res_concluir.status_code == 400
    assert "pendentes" in res_concluir.get_json()["message"].lower()


# 18. Concluir PDI com ações concluídas/canceladas retorna 200.
def test_concluir_pdi_com_acoes_concluidas_ou_canceladas(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["admin_email"], "admin123")

    create_res = api_post(
        client,
        "/pdis",
        {
            "colaborador_id": ids["colab1_id"],
            "titulo": "PDI",
            "descricao": "Desc",
            "acoes": [
                {
                    "tipo": "LEITURA",
                    "descricao": "Livro A",
                    "prazo": "2026-08-01"
                },
                {
                    "tipo": "TREINAMENTO",
                    "descricao": "Treinamento B",
                    "prazo": "2026-08-01"
                }
            ]
        },
        token
    )
    pdi_data = create_res.get_json()
    pdi_id = pdi_data["id"]
    acao1_id = pdi_data["acoes"][0]["id"]
    acao2_id = pdi_data["acoes"][1]["id"]

    # Conclui ação 1
    api_patch(client, f"/pdis/{pdi_id}/acoes/{acao1_id}/concluir", token=token)
    # Cancela ação 2
    api_patch(client, f"/pdis/{pdi_id}/acoes/{acao2_id}/cancelar", token=token)

    # Conclui PDI
    res_concluir = api_patch(client, f"/pdis/{pdi_id}/concluir", token=token)
    assert res_concluir.status_code == 200
    assert res_concluir.get_json()["status"] == "CONCLUIDO"


# 19. Cancelar PDI concluído retorna 400.
def test_cancelar_pdi_concluido_retorna_400(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["admin_email"], "admin123")

    create_res = api_post(
        client,
        "/pdis",
        {
            "colaborador_id": ids["colab1_id"],
            "titulo": "PDI",
            "descricao": "Desc",
            "acoes": []
        },
        token
    )
    pdi_id = create_res.get_json()["id"]

    # Conclui PDI
    api_patch(client, f"/pdis/{pdi_id}/concluir", token=token)

    # Tenta cancelar
    res_cancelar = api_patch(client, f"/pdis/{pdi_id}/cancelar", token=token)
    assert res_cancelar.status_code == 400
    assert "concluido" in res_cancelar.get_json()["message"].lower()


# 20. Alterar PDI cancelado retorna 400.
def test_alterar_pdi_cancelado_retorna_400(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["admin_email"], "admin123")

    create_res = api_post(
        client,
        "/pdis",
        {
            "colaborador_id": ids["colab1_id"],
            "titulo": "PDI",
            "descricao": "Desc",
            "acoes": []
        },
        token
    )
    pdi_id = create_res.get_json()["id"]

    # Cancela PDI
    api_patch(client, f"/pdis/{pdi_id}/cancelar", token=token)

    # Tenta atualizar
    res_update = api_patch(
        client,
        f"/pdis/{pdi_id}",
        {"titulo": "Novo Titulo", "descricao": "Nova Descricao"},
        token
    )
    assert res_update.status_code == 400
    assert "cancelado" in res_update.get_json()["message"].lower()
