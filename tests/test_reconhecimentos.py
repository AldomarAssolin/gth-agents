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


# 1. ADMIN cria reconhecimento para qualquer colaborador.
def test_admin_cria_reconhecimento_para_qualquer_colaborador(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["admin_email"])

    payload = {
        "colaborador_id": ids["colab2_id"],
        "tipo": "EVOLUCAO_TECNICA",
        "descricao": "Apresentou evolucao consistente",
        "evidencia": "Entrega com menos de 1% de retrabalho"
    }
    res = api_post(client, "/reconhecimentos", payload, token)
    assert res.status_code == 201
    data = res.get_json()
    assert data["id"] is not None
    assert data["tipo"] == "EVOLUCAO_TECNICA"
    assert data["descricao"] == payload["descricao"]
    assert data["ativo"] is True


# 2. RH cria reconhecimento para qualquer colaborador.
def test_rh_cria_reconhecimento_para_qualquer_colaborador(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["rh_email"])

    payload = {
        "colaborador_id": ids["colab1_id"],
        "tipo": "DESTAQUE",
        "descricao": "Destaque do mes de Maio",
        "evidencia": "Liderou a implementacao da Issue #011"
    }
    res = api_post(client, "/reconhecimentos", payload, token)
    assert res.status_code == 201
    assert res.get_json()["descricao"] == payload["descricao"]


# 3. LIDER cria reconhecimento para colaborador do seu setor.
def test_lider_cria_reconhecimento_do_seu_setor(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["lidera_email"])

    payload = {
        "colaborador_id": ids["colab1_id"], # Liderado no Setor 1
        "tipo": "APOIO_EQUIPE",
        "descricao": "Excelente apoio aos juniores",
        "evidencia": "Apoio diario na resolucao de bugs"
    }
    res = api_post(client, "/reconhecimentos", payload, token)
    assert res.status_code == 201
    assert res.get_json()["descricao"] == payload["descricao"]


# 4. LIDER não cria reconhecimento para colaborador de outro setor.
def test_lider_nao_cria_reconhecimento_de_outro_setor(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["lidera_email"]) # Lider do Setor 1

    payload = {
        "colaborador_id": ids["colab2_id"], # Colaborador do Setor 2
        "tipo": "APOIO_EQUIPE",
        "descricao": "Apoio a outra equipe",
        "evidencia": "Evidencia invalida"
    }
    res = api_post(client, "/reconhecimentos", payload, token)
    assert res.status_code == 403
    assert res.get_json()["error"] == "FORBIDDEN"


# 5. COLABORADOR não cria reconhecimento.
def test_colaborador_nao_cria_reconhecimento(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["colaba_email"])

    payload = {
        "colaborador_id": ids["colab1_id"],
        "tipo": "DESTAQUE",
        "descricao": "Quero me destacar",
        "evidencia": "Eu sou legal"
    }
    res = api_post(client, "/reconhecimentos", payload, token)
    assert res.status_code == 403
    assert res.get_json()["error"] == "FORBIDDEN"


# 6. COLABORADOR consulta seus próprios reconhecimentos.
def test_colaborador_consulta_proprios_reconhecimentos(client):
    ids = seed_data(client.application)
    admin_token = get_token(client, ids["admin_email"])

    # Criamos um reconhecimento para o Colab A
    create_res = api_post(
        client,
        "/reconhecimentos",
        {
            "colaborador_id": ids["colab1_id"],
            "tipo": "META_ATINGIDA",
            "descricao": "Meta batida",
            "evidencia": "Evidencia 100%"
        },
        admin_token
    )
    rec_id = create_res.get_json()["id"]

    colab_token = get_token(client, ids["colaba_email"])

    # Consulta individual
    res = api_get(client, f"/reconhecimentos/{rec_id}", colab_token)
    assert res.status_code == 200
    assert res.get_json()["descricao"] == "Meta batida"

    # Listagem por colaborador
    res_list = api_get(client, f"/colaboradores/{ids['colab1_id']}/reconhecimentos", colab_token)
    assert res_list.status_code == 200
    assert len(res_list.get_json()) == 1
    assert res_list.get_json()[0]["id"] == rec_id


# 7. COLABORADOR não consulta reconhecimento de outro colaborador.
def test_colaborador_nao_consulta_reconhecimento_alheio(client):
    ids = seed_data(client.application)
    admin_token = get_token(client, ids["admin_email"])

    # Criamos um reconhecimento para o Colab B
    create_res = api_post(
        client,
        "/reconhecimentos",
        {
            "colaborador_id": ids["colab2_id"],
            "tipo": "COMPORTAMENTO_POSITIVO",
            "descricao": "Comportamento excelente",
            "evidencia": "Evidencia"
        },
        admin_token
    )
    rec_id = create_res.get_json()["id"]

    colab_token = get_token(client, ids["colaba_email"]) # Colab A tenta ver

    # Consulta individual alheia
    res = api_get(client, f"/reconhecimentos/{rec_id}", colab_token)
    assert res.status_code == 403
    assert res.get_json()["error"] == "FORBIDDEN"

    # Listagem alheia
    res_list = api_get(client, f"/colaboradores/{ids['colab2_id']}/reconhecimentos", colab_token)
    assert res_list.status_code == 403
    assert res_list.get_json()["error"] == "FORBIDDEN"


# 8. Reconhecimento sem descrição retorna 400.
def test_reconhecimento_sem_descricao_retorna_400(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["admin_email"])

    payload = {
        "colaborador_id": ids["colab1_id"],
        "tipo": "DESTAQUE",
        "descricao": "",
        "evidencia": "Evidencia"
    }
    res = api_post(client, "/reconhecimentos", payload, token)
    assert res.status_code == 400
    assert "descricao" in res.get_json()["message"].lower()


# 9. Reconhecimento sem evidência retorna 400.
def test_reconhecimento_sem_evidencia_retorna_400(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["admin_email"])

    payload = {
        "colaborador_id": ids["colab1_id"],
        "tipo": "DESTAQUE",
        "descricao": "Descricao",
        "evidencia": ""
    }
    res = api_post(client, "/reconhecimentos", payload, token)
    assert res.status_code == 400
    assert "evidencia" in res.get_json()["message"].lower()


# 10. Reconhecimento com tipo inválido retorna 400.
def test_reconhecimento_tipo_invalido_retorna_400(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["admin_email"])

    payload = {
        "colaborador_id": ids["colab1_id"],
        "tipo": "INVALID_TYPE",
        "descricao": "Descricao",
        "evidencia": "Evidencia"
    }
    res = api_post(client, "/reconhecimentos", payload, token)
    assert res.status_code == 400
    assert "tipo" in res.get_json()["message"].lower()


# 11. Reconhecimento com colaborador inexistente retorna 404.
def test_reconhecimento_colaborador_inexistente_retorna_404(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["admin_email"])

    payload = {
        "colaborador_id": 9999,
        "tipo": "DESTAQUE",
        "descricao": "Descricao",
        "evidencia": "Evidencia"
    }
    res = api_post(client, "/reconhecimentos", payload, token)
    assert res.status_code == 404
    assert res.get_json()["error"] == "NOT_FOUND"


# 12. Buscar reconhecimento por ID com sucesso.
def test_buscar_reconhecimento_por_id_com_sucesso(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["admin_email"])

    create_res = api_post(
        client,
        "/reconhecimentos",
        {
            "colaborador_id": ids["colab1_id"],
            "tipo": "POTENCIAL_LIDERANCA",
            "descricao": "Lider nato",
            "evidencia": "Apoio geral"
        },
        token
    )
    rec_id = create_res.get_json()["id"]

    res = api_get(client, f"/reconhecimentos/{rec_id}", token)
    assert res.status_code == 200
    assert res.get_json()["descricao"] == "Lider nato"


# 13. Buscar reconhecimento inexistente retorna 404.
def test_buscar_reconhecimento_inexistente_retorna_404(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["admin_email"])

    res = api_get(client, "/reconhecimentos/9999", token)
    assert res.status_code == 404
    assert res.get_json()["error"] == "NOT_FOUND"


# 14. Cancelar reconhecimento com sucesso.
def test_cancelar_reconhecimento_com_sucesso(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["admin_email"])

    # Criar
    create_res = api_post(
        client,
        "/reconhecimentos",
        {
            "colaborador_id": ids["colab1_id"],
            "tipo": "OUTRO",
            "descricao": "Treinamento rapido",
            "evidencia": "Certificado"
        },
        token
    )
    rec_id = create_res.get_json()["id"]

    # Cancelar
    res = api_patch(
        client,
        f"/reconhecimentos/{rec_id}/cancelar",
        {"motivo_cancelamento": "Criado por engano"},
        token
    )
    assert res.status_code == 200
    data = res.get_json()
    assert data["ativo"] is False
    assert data["motivo_cancelamento"] == "Criado por engano"
    assert data["cancelado_por_id"] is not None
    assert data["cancelado_em"] is not None


# 15. Cancelar reconhecimento já cancelado retorna 400.
def test_cancelar_reconhecimento_duplicado_retorna_400(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["admin_email"])

    # Criar
    create_res = api_post(
        client,
        "/reconhecimentos",
        {
            "colaborador_id": ids["colab1_id"],
            "tipo": "OUTRO",
            "descricao": "Treinamento rapido",
            "evidencia": "Certificado"
        },
        token
    )
    rec_id = create_res.get_json()["id"]

    # Cancelar 1
    api_patch(client, f"/reconhecimentos/{rec_id}/cancelar", {"motivo_cancelamento": "Motivo"}, token)

    # Cancelar 2
    res2 = api_patch(client, f"/reconhecimentos/{rec_id}/cancelar", {"motivo_cancelamento": "Novo Motivo"}, token)
    assert res2.status_code == 400
    assert "ja esta cancelado" in res2.get_json()["message"].lower()


# 16. Cancelar reconhecimento fora do escopo retorna 403.
def test_cancelar_reconhecimento_fora_do_escopo_retorna_403(client):
    ids = seed_data(client.application)
    admin_token = get_token(client, ids["admin_email"])

    # Admin cria reconhecimento para Colab B (Setor 2)
    create_res = api_post(
        client,
        "/reconhecimentos",
        {
            "colaborador_id": ids["colab2_id"],
            "tipo": "DESTAQUE",
            "descricao": "Reconhecimento do B",
            "evidencia": "Evidencia"
        },
        admin_token
    )
    rec_id = create_res.get_json()["id"]

    # Lider A (Setor 1) tenta cancelar reconhecimento do Colab B (Setor 2)
    lider_token = get_token(client, ids["lidera_email"])
    res = api_patch(
        client,
        f"/reconhecimentos/{rec_id}/cancelar",
        {"motivo_cancelamento": "Nao gosto dele"},
        lider_token
    )
    assert res.status_code == 403
    assert res.get_json()["error"] == "FORBIDDEN"


# 17. LIDER lista apenas reconhecimentos do seu setor.
def test_lider_lista_apenas_reconhecimentos_do_seu_setor(client):
    ids = seed_data(client.application)
    admin_token = get_token(client, ids["admin_email"])

    # Reconhecimento para Colab A (Setor 1)
    api_post(
        client,
        "/reconhecimentos",
        {
            "colaborador_id": ids["colab1_id"],
            "tipo": "DESTAQUE",
            "descricao": "Reconhecimento A",
            "evidencia": "Evi"
        },
        admin_token
    )

    # Reconhecimento para Colab B (Setor 2)
    api_post(
        client,
        "/reconhecimentos",
        {
            "colaborador_id": ids["colab2_id"],
            "tipo": "DESTAQUE",
            "descricao": "Reconhecimento B",
            "evidencia": "Evi"
        },
        admin_token
    )

    lider_token = get_token(client, ids["lidera_email"]) # Lider do Setor 1
    res = api_get(client, "/reconhecimentos", lider_token)
    assert res.status_code == 200
    data = res.get_json()
    assert len(data) == 1
    assert data[0]["colaborador_id"] == ids["colab1_id"]


# 18. RH lista todos os reconhecimentos.
def test_rh_lista_todos_os_reconhecimentos(client):
    ids = seed_data(client.application)
    admin_token = get_token(client, ids["admin_email"])

    # Reconhecimento para Colab A (Setor 1)
    api_post(
        client,
        "/reconhecimentos",
        {
            "colaborador_id": ids["colab1_id"],
            "tipo": "DESTAQUE",
            "descricao": "Reconhecimento A",
            "evidencia": "Evi"
        },
        admin_token
    )

    # Reconhecimento para Colab B (Setor 2)
    api_post(
        client,
        "/reconhecimentos",
        {
            "colaborador_id": ids["colab2_id"],
            "tipo": "DESTAQUE",
            "descricao": "Reconhecimento B",
            "evidencia": "Evi"
        },
        admin_token
    )

    rh_token = get_token(client, ids["rh_email"])
    res = api_get(client, "/reconhecimentos", rh_token)
    assert res.status_code == 200
    data = res.get_json()
    assert len(data) == 2


# 19. ADMIN lista todos os reconhecimentos.
def test_admin_lista_todos_os_reconhecimentos(client):
    ids = seed_data(client.application)
    admin_token = get_token(client, ids["admin_email"])

    # Reconhecimento para Colab A (Setor 1)
    api_post(
        client,
        "/reconhecimentos",
        {
            "colaborador_id": ids["colab1_id"],
            "tipo": "DESTAQUE",
            "descricao": "Reconhecimento A",
            "evidencia": "Evi"
        },
        admin_token
    )

    # Reconhecimento para Colab B (Setor 2)
    api_post(
        client,
        "/reconhecimentos",
        {
            "colaborador_id": ids["colab2_id"],
            "tipo": "DESTAQUE",
            "descricao": "Reconhecimento B",
            "evidencia": "Evi"
        },
        admin_token
    )

    res = api_get(client, "/reconhecimentos", admin_token)
    assert res.status_code == 200
    data = res.get_json()
    assert len(data) == 2
