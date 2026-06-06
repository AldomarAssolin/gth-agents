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
from domain.enums.pdi_enums import StatusPDI, OrigemPDI, TipoAcaoPDI, StatusAcaoPDI
from domain.enums.tipo_reconhecimento import TipoReconhecimento
from infrastructure.database.base import Base
from infrastructure.database.models.usuario_model import UsuarioModel
from infrastructure.database.models.colaborador_model import ColaboradorModel
from infrastructure.database.models.setor_model import SetorModel
from infrastructure.database.models.funcao_model import FuncaoModel
from infrastructure.database.models.meta_model import MetaModel
from infrastructure.database.models.feedback_model import FeedbackModel
from infrastructure.database.models.pdi_model import PDIModel
from infrastructure.database.models.reconhecimento_model import ReconhecimentoModel
from infrastructure.database.models.perfil_talento_model import PerfilTalentoModel
from infrastructure.database.models.avaliacao_model import AvaliacaoModel
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

        # Seed dados de evolução para Colab 1
        # 1. Metas
        m1 = MetaModel(colaborador_id=colab1.id, criado_por_id=admin.id, titulo="Meta 1", descricao="Desc", prazo=date(2026, 6, 1), status=StatusMeta.CONCLUIDA.value, prioridade=PrioridadeMeta.MEDIA.value, origem="MANUAL")
        m2 = MetaModel(colaborador_id=colab1.id, criado_por_id=admin.id, titulo="Meta 2", descricao="Desc", prazo=date(2026, 5, 1), status=StatusMeta.ATRASADA.value, prioridade=PrioridadeMeta.ALTA.value, origem="MANUAL")
        m3 = MetaModel(colaborador_id=colab1.id, criado_por_id=admin.id, titulo="Meta 3", descricao="Desc", prazo=date(2026, 7, 1), status=StatusMeta.PENDENTE.value, prioridade=PrioridadeMeta.CRITICA.value, origem="MANUAL")
        db.session.add_all([m1, m2, m3])

        # 2. Feedbacks
        f1 = FeedbackModel(colaborador_id=colab1.id, autor_id=lider_a.id, contexto="Feedback 1", ponto_positivo="Bom", ponto_melhoria="Melhorar", acao_recomendada="Focar", data_feedback=datetime(2026, 5, 1, 10, 0), criado_em=datetime(2026, 5, 1, 10, 0))
        db.session.add(f1)

        # 3. PDIs
        pdi1 = PDIModel(colaborador_id=colab1.id, criado_por_id=lider_a.id, titulo="PDI 1", descricao="Desc", origem=OrigemPDI.AVALIACAO.value, status=StatusPDI.ATIVO.value, data_inicio=date(2026, 5, 1), data_fim=date(2026, 6, 1), criado_em=datetime(2026, 5, 1, 10, 0))
        pdi2 = PDIModel(colaborador_id=colab1.id, criado_por_id=lider_a.id, titulo="PDI 2", descricao="Desc", origem=OrigemPDI.MANUAL.value, status=StatusPDI.CONCLUIDO.value, data_inicio=date(2026, 5, 1), data_fim=date(2026, 6, 1), criado_em=datetime(2026, 5, 2, 10, 0))
        db.session.add_all([pdi1, pdi2])

        # 4. Reconhecimentos
        r1 = ReconhecimentoModel(colaborador_id=colab1.id, registrado_por_id=lider_a.id, tipo=TipoReconhecimento.DESTAQUE.value, descricao="Desc R1", evidencia="Evi R1", data_reconhecimento=datetime(2026, 5, 15, 10, 0), criado_em=datetime(2026, 5, 15, 10, 0), ativo=True)
        r2 = ReconhecimentoModel(colaborador_id=colab1.id, registrado_por_id=lider_a.id, tipo=TipoReconhecimento.EVOLUCAO_TECNICA.value, descricao="Desc R2", evidencia="Evi R2", data_reconhecimento=datetime(2026, 5, 10, 10, 0), criado_em=datetime(2026, 5, 10, 10, 0), ativo=False, cancelado_em=datetime(2026, 5, 11, 10, 0), cancelado_por_id=admin.id, motivo_cancelamento="Erro")
        db.session.add_all([r1, r2])

        # 5. Perfis de Talento (dois perfis para testar o mais recente)
        pt1 = PerfilTalentoModel(colaborador_id=colab1.id, classificacao="ALTO_POTENCIAL", nivel_tecnico="MEDIO", nivel_comportamental="ALTO", potencial_lideranca="ALTO", resumo="Resumo 1", criado_em=datetime(2026, 5, 1, 10, 0))
        pt2 = PerfilTalentoModel(colaborador_id=colab1.id, classificacao="ESPECIALISTA_TECNICO", nivel_tecnico="ALTO", nivel_comportamental="MEDIO", potencial_lideranca="MEDIO", resumo="Resumo 2", criado_em=datetime(2026, 5, 20, 10, 0))
        db.session.add_all([pt1, pt2])

        # 6. Avaliações
        av1 = AvaliacaoModel(colaborador_id=colab1.id, avaliador_id=lider_a.id, tipo="AVALIACAO_LIDER", observacao_geral="Avaliacao 1", data_avaliacao=datetime(2026, 5, 1, 10, 0), criado_em=datetime(2026, 5, 1, 10, 0), status="CONCLUIDA")
        db.session.add(av1)

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


def api_get(client, url, token=None):
    if hasattr(g, "usuario"):
        g.usuario = None
    headers = {"X-Enforce-Auth": "true"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return client.get(url, headers=headers)



# 1. ADMIN consulta evolução de qualquer colaborador.
def test_admin_consulta_evolucao_de_qualquer_colaborador(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["admin_email"])

    res = api_get(client, f"/colaboradores/{ids['colab1_id']}/evolucao", token)
    assert res.status_code == 200
    data = res.get_json()
    assert data["colaborador"]["nome"] == "Colaborador A"


# 2. RH consulta evolução de qualquer colaborador.
def test_rh_consulta_evolucao_de_qualquer_colaborador(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["rh_email"])

    res = api_get(client, f"/colaboradores/{ids['colab2_id']}/evolucao", token)
    assert res.status_code == 200
    data = res.get_json()
    assert data["colaborador"]["nome"] == "Colaborador B"


# 3. LIDER consulta evolução de colaborador do seu setor.
def test_lider_consulta_evolucao_do_seu_setor(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["lidera_email"])

    res = api_get(client, f"/colaboradores/{ids['colab1_id']}/evolucao", token)
    assert res.status_code == 200
    data = res.get_json()
    assert data["colaborador"]["nome"] == "Colaborador A"


# 4. LIDER não consulta evolução de colaborador de outro setor.
def test_lider_nao_consulta_evolucao_de_outro_setor(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["lidera_email"]) # Líder do Setor 1

    res = api_get(client, f"/colaboradores/{ids['colab2_id']}/evolucao", token) # Colaborador do Setor 2
    assert res.status_code == 403
    assert res.get_json()["error"] == "FORBIDDEN"


# 5. COLABORADOR consulta sua própria evolução.
def test_colaborador_consulta_propria_evolucao(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["colaba_email"])

    res = api_get(client, f"/colaboradores/{ids['colab1_id']}/evolucao", token)
    assert res.status_code == 200
    data = res.get_json()
    assert data["colaborador"]["id"] == ids["colab1_id"]


# 6. COLABORADOR não consulta evolução de outro colaborador.
def test_colaborador_nao_consulta_evolucao_alheia(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["colaba_email"]) # Colaborador A

    res = api_get(client, f"/colaboradores/{ids['colab2_id']}/evolucao", token) # Colaborador B
    assert res.status_code == 403
    assert res.get_json()["error"] == "FORBIDDEN"


# 7. Colaborador inexistente retorna 404.
def test_colaborador_inexistente_retorna_404(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["admin_email"])

    res = api_get(client, "/colaboradores/9999/evolucao", token)
    assert res.status_code == 404
    assert res.get_json()["error"] == "NOT_FOUND"


# 8. Evolução retorna perfil mais recente.
def test_evolucao_retorna_perfil_mais_recente(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["admin_email"])

    res = api_get(client, f"/colaboradores/{ids['colab1_id']}/evolucao", token)
    assert res.status_code == 200
    data = res.get_json()
    assert data["perfil_atual"]["classificacao"] == "ESPECIALISTA_TECNICO"
    assert data["perfil_atual"]["resumo"] == "Resumo 2"


# 9. Evolução retorna perfil_atual = null quando colaborador não possui perfil.
def test_evolucao_retorna_perfil_nulo_quando_nao_possui(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["admin_email"])

    res = api_get(client, f"/colaboradores/{ids['colab2_id']}/evolucao", token)
    assert res.status_code == 200
    data = res.get_json()
    assert data["perfil_atual"] is None


# 10. Indicador total_avaliacoes é calculado corretamente.
def test_indicador_total_avaliacoes_calculado_corretamente(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["admin_email"])

    res = api_get(client, f"/colaboradores/{ids['colab1_id']}/evolucao", token)
    assert res.status_code == 200
    data = res.get_json()
    assert data["indicadores"]["total_avaliacoes"] == 1


# 11. Indicador total_metas é calculado corretamente.
def test_indicador_total_metas_calculado_corretamente(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["admin_email"])

    res = api_get(client, f"/colaboradores/{ids['colab1_id']}/evolucao", token)
    assert res.status_code == 200
    data = res.get_json()
    assert data["indicadores"]["total_metas"] == 3


# 12. Indicador metas_concluidas é calculado corretamente.
def test_indicador_metas_concluidas_calculado_corretamente(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["admin_email"])

    res = api_get(client, f"/colaboradores/{ids['colab1_id']}/evolucao", token)
    assert res.status_code == 200
    data = res.get_json()
    assert data["indicadores"]["metas_concluidas"] == 1


# 13. Indicador metas_atrasadas é calculado corretamente.
def test_indicador_metas_atrasadas_calculado_corretamente(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["admin_email"])

    res = api_get(client, f"/colaboradores/{ids['colab1_id']}/evolucao", token)
    assert res.status_code == 200
    data = res.get_json()
    assert data["indicadores"]["metas_atrasadas"] == 1


# 14. Indicador total_feedbacks é calculado corretamente.
def test_indicador_total_feedbacks_calculado_corretamente(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["admin_email"])

    res = api_get(client, f"/colaboradores/{ids['colab1_id']}/evolucao", token)
    assert res.status_code == 200
    data = res.get_json()
    assert data["indicadores"]["total_feedbacks"] == 1


# 15. Indicador pdis_ativos é calculado corretamente.
def test_indicador_pdis_ativos_calculado_corretamente(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["admin_email"])

    res = api_get(client, f"/colaboradores/{ids['colab1_id']}/evolucao", token)
    assert res.status_code == 200
    data = res.get_json()
    assert data["indicadores"]["pdis_ativos"] == 1


# 16. Indicador reconhecimentos considera reconhecimentos ativos.
def test_indicador_reconhecimentos_considera_ativos_apenas(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["admin_email"])

    res = api_get(client, f"/colaboradores/{ids['colab1_id']}/evolucao", token)
    assert res.status_code == 200
    data = res.get_json()
    assert data["indicadores"]["reconhecimentos"] == 1
    assert len(data["reconhecimentos"]) == 1
    assert data["reconhecimentos"][0]["ativo"] is True


# 17. Response contém chaves principais esperadas.
def test_response_contem_chaves_principais_esperadas(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["admin_email"])

    res = api_get(client, f"/colaboradores/{ids['colab1_id']}/evolucao", token)
    assert res.status_code == 200
    data = res.get_json()
    assert "colaborador" in data
    assert "perfil_atual" in data
    assert "indicadores" in data
    assert "ultimas_avaliacoes" in data
    assert "metas" in data
    assert "feedbacks" in data
    assert "pdis" in data
    assert "reconhecimentos" in data


# 18. Endpoint sem token retorna 401.
def test_endpoint_sem_token_retorna_401(client):
    ids = seed_data(client.application)
    res = api_get(client, f"/colaboradores/{ids['colab1_id']}/evolucao")
    assert res.status_code == 401
