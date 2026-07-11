import json
from datetime import date, datetime
import pytest
from flask import g
from app import create_app
from app.config import Config
from app.extensions import db
from domain.enums.perfil_usuario import PerfilUsuario
from domain.enums.status_meta import StatusMeta
from domain.enums.prioridade_meta import PrioridadeMeta
from domain.enums.tipo_reconhecimento import TipoReconhecimento
from infrastructure.database.base import Base
from infrastructure.database.models.usuario_model import UsuarioModel
from infrastructure.database.models.colaborador_model import ColaboradorModel
from infrastructure.database.models.setor_model import SetorModel
from infrastructure.database.models.funcao_model import FuncaoModel
from infrastructure.database.models.competencia_model import CompetenciaModel
from infrastructure.database.models.avaliacao_model import AvaliacaoModel
from infrastructure.database.models.meta_model import MetaModel
from infrastructure.database.models.feedback_model import FeedbackModel
from infrastructure.database.models.pdi_model import PDIModel
from infrastructure.database.models.reconhecimento_model import ReconhecimentoModel
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

        competencia1 = CompetenciaModel(nome="Python", descricao="Flask", tipo="TECNICA", peso=1.0, ativo=True)
        db.session.add(competencia1)
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
        db.session.add_all([admin, rh, lider_a, lider_b, colab_a])
        db.session.commit()

        return {
            "colab1_id": colab1.id,
            "colab2_id": colab2.id,
            "competencia1_id": competencia1.id,
            "admin_email": "admin@test.com",
            "rh_email": "rh@test.com",
            "lidera_email": "lidera@test.com",
            "liderb_email": "liderb@test.com",
            "colaba_email": "colaba_u@test.com",
            "admin_id": admin.id,
            "lidera_id": lider_a.id,
            "liderb_id": lider_b.id,
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
    headers = {"X-Enforce-Auth": "true"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return client.post(url, json=json_data, headers=headers)


def api_patch(client, url, json_data=None, token=None):
    if hasattr(g, "usuario"):
        g.usuario = None
    headers = {"X-Enforce-Auth": "true"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return client.patch(url, json=json_data, headers=headers)


# ==============================================================================
# TESTES DE SEGURANÇA (Avaliações, Metas e Feedbacks)
# ==============================================================================

def test_seguranca_avaliacao_derivada_jwt(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["lidera_email"])

    payload_base = {
        "colaborador_id": ids["colab1_id"],
        "tipo": "AVALIACAO_LIDER",
        "observacao_geral": "Teste Geral",
        "itens": [{"competencia_id": ids["competencia1_id"], "nota": 4, "comentario": "Bom"}]
    }

    # 1. Criação sem campo de autoria no payload
    res = api_post(client, "/avaliacoes", payload_base, token)
    assert res.status_code == 201
    data = res.get_json()
    assert data is not None

    with client.application.app_context():
        pt = db.session.query(AvaliacaoModel).filter_by(colaborador_id=ids["colab1_id"]).first()
        assert pt is not None
        assert pt.avaliador_id == ids["lidera_id"]

    # 2. Envio de ID de outro usuário existente (Spoofing)
    payload_spoof = payload_base.copy()
    payload_spoof["avaliador_id"] = ids["liderb_id"]
    res = api_post(client, "/avaliacoes", payload_spoof, token)
    assert res.status_code == 201

    with client.application.app_context():
        # Pega a última avaliação criada
        pt = db.session.query(AvaliacaoModel).order_by(AvaliacaoModel.id.desc()).first()
        # 3. Persistência do usuário autenticado e mitigação de spoofing
        assert pt.avaliador_id == ids["lidera_id"]
        assert pt.avaliador_id != ids["liderb_id"]

    # 4. Envio de ID inexistente (Spoofing)
    payload_fake = payload_base.copy()
    payload_fake["avaliador_id"] = 99999
    res = api_post(client, "/avaliacoes", payload_fake, token)
    assert res.status_code == 201

    with client.application.app_context():
        pt = db.session.query(AvaliacaoModel).order_by(AvaliacaoModel.id.desc()).first()
        # Garante que 99999 foi totalmente ignorado e o ID correto persistido
        assert pt.avaliador_id == ids["lidera_id"]
        assert pt.avaliador_id != 99999

    # 5. HTTP 401 sem autenticação
    res = api_post(client, "/avaliacoes", payload_base)
    assert res.status_code == 401

    # 6. HTTP 403 fora do perfil ou escopo
    # Lider A tenta avaliar Colaborador B (do setor 2) -> Lider A é do setor 1.
    payload_escopo = payload_base.copy()
    payload_escopo["colaborador_id"] = ids["colab2_id"]
    res = api_post(client, "/avaliacoes", payload_escopo, token)
    assert res.status_code == 403


def test_seguranca_meta_derivada_jwt(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["lidera_email"])

    payload_base = {
        "colaborador_id": ids["colab1_id"],
        "titulo": "Meta A",
        "descricao": "Desc Meta",
        "prazo": "2026-12-31",
        "prioridade": "MEDIA"
    }

    # 1. Criação sem campo de autoria no payload
    res = api_post(client, "/metas", payload_base, token)
    assert res.status_code == 201

    with client.application.app_context():
        meta = db.session.query(MetaModel).filter_by(titulo="Meta A").first()
        assert meta is not None
        assert meta.criado_por_id == ids["lidera_id"]

    # 2. Envio de ID de outro usuário existente (Spoofing)
    payload_spoof = payload_base.copy()
    payload_spoof["titulo"] = "Meta Spoof"
    payload_spoof["criado_por_id"] = ids["liderb_id"]
    res = api_post(client, "/metas", payload_spoof, token)
    assert res.status_code == 201

    with client.application.app_context():
        meta = db.session.query(MetaModel).filter_by(titulo="Meta Spoof").first()
        # 3. Persistência do usuário autenticado e mitigação de spoofing
        assert meta.criado_por_id == ids["lidera_id"]
        assert meta.criado_por_id != ids["liderb_id"]

    # 4. Envio de ID inexistente (Spoofing)
    payload_fake = payload_base.copy()
    payload_fake["titulo"] = "Meta Fake ID"
    payload_fake["criado_por_id"] = 99999
    res = api_post(client, "/metas", payload_fake, token)
    assert res.status_code == 201

    with client.application.app_context():
        meta = db.session.query(MetaModel).filter_by(titulo="Meta Fake ID").first()
        assert meta.criado_por_id == ids["lidera_id"]
        assert meta.criado_por_id != 99999

    # 5. HTTP 401 sem autenticação
    res = api_post(client, "/metas", payload_base)
    assert res.status_code == 401

    # 6. HTTP 403 fora do perfil ou escopo (Lider A gerenciar Colab B)
    payload_escopo = payload_base.copy()
    payload_escopo["colaborador_id"] = ids["colab2_id"]
    res = api_post(client, "/metas", payload_escopo, token)
    assert res.status_code == 403


def test_seguranca_feedback_derivado_jwt(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["lidera_email"])

    payload_base = {
        "colaborador_id": ids["colab1_id"],
        "contexto": "Contexto Feedback",
        "ponto_positivo": "Pontos Positivos",
        "ponto_melhoria": "Pontos Melhoria",
        "acao_recomendada": "Recomendacao"
    }

    # 1. Criação sem campo de autoria no payload
    res = api_post(client, "/feedbacks", payload_base, token)
    assert res.status_code == 201

    with client.application.app_context():
        fb = db.session.query(FeedbackModel).filter_by(colaborador_id=ids["colab1_id"]).first()
        assert fb is not None
        assert fb.autor_id == ids["lidera_id"]

    # 2. Envio de ID de outro usuário existente (Spoofing)
    payload_spoof = payload_base.copy()
    payload_spoof["autor_id"] = ids["liderb_id"]
    res = api_post(client, "/feedbacks", payload_spoof, token)
    assert res.status_code == 201

    with client.application.app_context():
        fb = db.session.query(FeedbackModel).order_by(FeedbackModel.id.desc()).first()
        # 3. Persistência do usuário autenticado e mitigação de spoofing
        assert fb.autor_id == ids["lidera_id"]
        assert fb.autor_id != ids["liderb_id"]

    # 4. Envio de ID inexistente (Spoofing)
    payload_fake = payload_base.copy()
    payload_fake["autor_id"] = 99999
    res = api_post(client, "/feedbacks", payload_fake, token)
    assert res.status_code == 201

    with client.application.app_context():
        fb = db.session.query(FeedbackModel).order_by(FeedbackModel.id.desc()).first()
        assert fb.autor_id == ids["lidera_id"]
        assert fb.autor_id != 99999

    # 5. HTTP 401 sem autenticação
    res = api_post(client, "/feedbacks", payload_base)
    assert res.status_code == 401

    # 6. HTTP 403 fora do perfil ou escopo (Lider A em Colab B)
    payload_escopo = payload_base.copy()
    payload_escopo["colaborador_id"] = ids["colab2_id"]
    res = api_post(client, "/feedbacks", payload_escopo, token)
    assert res.status_code == 403


# ==============================================================================
# TESTES DE REGRESSÃO E CONSISTÊNCIA (PDI e Reconhecimentos)
# ==============================================================================

def test_regressao_pdi_derivada_jwt(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["lidera_email"])

    payload_base = {
        "colaborador_id": ids["colab1_id"],
        "titulo": "PDI Tecnico",
        "descricao": "Desc PDI",
        "origem": "MANUAL",
        "data_inicio": "2026-06-01",
        "data_fim": "2026-12-01",
        "acoes": []
    }

    # 1. Envio de ID de outro usuário existente (Spoofing) no payload
    payload_spoof = payload_base.copy()
    payload_spoof["criado_por_id"] = ids["liderb_id"]
    res = api_post(client, "/pdis", payload_spoof, token)
    assert res.status_code == 201

    with client.application.app_context():
        pdi = db.session.query(PDIModel).filter_by(titulo="PDI Tecnico").first()
        assert pdi is not None
        # O ID deve ser o do JWT do Lider A e não o do Lider B
        assert pdi.criado_por_id == ids["lidera_id"]
        assert pdi.criado_por_id != ids["liderb_id"]

    # 2. Envio de ID inexistente (Spoofing)
    payload_fake = payload_base.copy()
    payload_fake["titulo"] = "PDI Fake ID"
    payload_fake["criado_por_id"] = 99999
    res = api_post(client, "/pdis", payload_fake, token)
    assert res.status_code == 201

    with client.application.app_context():
        pdi = db.session.query(PDIModel).filter_by(titulo="PDI Fake ID").first()
        assert pdi.criado_por_id == ids["lidera_id"]
        assert pdi.criado_por_id != 99999

    # 3. HTTP 401 sem autenticação
    res = api_post(client, "/pdis", payload_base)
    assert res.status_code == 401

    # 4. HTTP 403 fora do perfil ou escopo (Lider A criar PDI para Colab B)
    payload_escopo = payload_base.copy()
    payload_escopo["colaborador_id"] = ids["colab2_id"]
    res = api_post(client, "/pdis", payload_escopo, token)
    assert res.status_code == 403


def test_regressao_reconhecimento_derivada_jwt(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["lidera_email"])

    payload_base = {
        "colaborador_id": ids["colab1_id"],
        "tipo": "DESTAQUE",
        "descricao": "Descricao Rec",
        "evidencia": "Evidencia Rec"
    }

    # 1. Envio de ID de outro usuário existente (Spoofing) no payload na criação
    payload_spoof = payload_base.copy()
    payload_spoof["registrado_por_id"] = ids["liderb_id"]
    res = api_post(client, "/reconhecimentos", payload_spoof, token)
    assert res.status_code == 201
    rec_id = res.get_json()["id"]

    with client.application.app_context():
        rec = db.session.query(ReconhecimentoModel).filter_by(id=rec_id).first()
        assert rec is not None
        assert rec.registrado_por_id == ids["lidera_id"]
        assert rec.registrado_por_id != ids["liderb_id"]

    # 2. Envio de ID inexistente (Spoofing) na criação
    payload_fake = payload_base.copy()
    payload_fake["registrado_por_id"] = 99999
    res = api_post(client, "/reconhecimentos", payload_fake, token)
    assert res.status_code == 201
    rec_id_fake = res.get_json()["id"]

    with client.application.app_context():
        rec = db.session.query(ReconhecimentoModel).filter_by(id=rec_id_fake).first()
        assert rec.registrado_por_id == ids["lidera_id"]
        assert rec.registrado_por_id != 99999

    # 3. Spoofing no cancelamento
    # O cancelamento de reconhecimento exige perfil ADMIN ou RH.
    admin_token = get_token(client, ids["admin_email"])
    res_cancel = api_patch(
        client,
        f"/reconhecimentos/{rec_id}/cancelar",
        {"motivo_cancelamento": "Teste", "cancelado_por_id": ids["liderb_id"]},
        admin_token
    )
    assert res_cancel.status_code == 200

    with client.application.app_context():
        rec = db.session.query(ReconhecimentoModel).filter_by(id=rec_id).first()
        assert rec.cancelado_por_id == ids["admin_id"]
        assert rec.cancelado_por_id != ids["liderb_id"]

    # 4. HTTP 401 sem autenticação
    res = api_post(client, "/reconhecimentos", payload_base)
    assert res.status_code == 401

    # 5. HTTP 403 fora do perfil ou escopo (Lider A criar reconhecimento para Colab B)
    payload_escopo = payload_base.copy()
    payload_escopo["colaborador_id"] = ids["colab2_id"]
    res = api_post(client, "/reconhecimentos", payload_escopo, token)
    assert res.status_code == 403
