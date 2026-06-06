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
from domain.enums.pdi_enums import StatusPDI, OrigemPDI
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
            status="INATIVO",
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

        # Seed dados de evolução para Colab 1
        m1 = MetaModel(colaborador_id=colab1.id, criado_por_id=admin.id, titulo="Meta 1", descricao="Desc", prazo=date(2026, 6, 1), status=StatusMeta.CONCLUIDA.value, prioridade=PrioridadeMeta.MEDIA.value, origem="MANUAL")
        m2 = MetaModel(colaborador_id=colab1.id, criado_por_id=admin.id, titulo="Meta 2", descricao="Desc", prazo=date(2026, 5, 1), status=StatusMeta.ATRASADA.value, prioridade=PrioridadeMeta.ALTA.value, origem="MANUAL")
        m3 = MetaModel(colaborador_id=colab1.id, criado_por_id=admin.id, titulo="Meta 3", descricao="Desc", prazo=date(2026, 7, 1), status=StatusMeta.PENDENTE.value, prioridade=PrioridadeMeta.CRITICA.value, origem="MANUAL")
        db.session.add_all([m1, m2, m3])

        f1 = FeedbackModel(colaborador_id=colab1.id, autor_id=lider_a.id, contexto="Feedback 1", ponto_positivo="Bom", ponto_melhoria="Melhorar", acao_recomendada="Focar", data_feedback=datetime(2026, 5, 1, 10, 0), criado_em=datetime(2026, 5, 1, 10, 0))
        db.session.add(f1)

        pdi1 = PDIModel(colaborador_id=colab1.id, criado_por_id=lider_a.id, titulo="PDI 1", descricao="Desc", origem=OrigemPDI.AVALIACAO.value, status=StatusPDI.ATIVO.value, data_inicio=date(2026, 5, 1), data_fim=date(2026, 6, 1), criado_em=datetime(2026, 5, 1, 10, 0))
        pdi2 = PDIModel(colaborador_id=colab1.id, criado_por_id=lider_a.id, titulo="PDI 2", descricao="Desc", origem=OrigemPDI.MANUAL.value, status=StatusPDI.CONCLUIDO.value, data_inicio=date(2026, 5, 1), data_fim=date(2026, 6, 1), criado_em=datetime(2026, 5, 2, 10, 0))
        db.session.add_all([pdi1, pdi2])

        r1 = ReconhecimentoModel(colaborador_id=colab1.id, registrado_por_id=lider_a.id, tipo=TipoReconhecimento.DESTAQUE.value, descricao="Desc R1", evidencia="Evi R1", data_reconhecimento=datetime(2026, 5, 15, 10, 0), criado_em=datetime(2026, 5, 15, 10, 0), ativo=True)
        r2 = ReconhecimentoModel(colaborador_id=colab1.id, registrado_por_id=lider_a.id, tipo=TipoReconhecimento.EVOLUCAO_TECNICA.value, descricao="Desc R2", evidencia="Evi R2", data_reconhecimento=datetime(2026, 5, 10, 10, 0), criado_em=datetime(2026, 5, 10, 10, 0), ativo=False, cancelado_em=datetime(2026, 5, 11, 10, 0), cancelado_por_id=admin.id, motivo_cancelamento="Erro")
        db.session.add_all([r1, r2])

        pt1 = PerfilTalentoModel(colaborador_id=colab1.id, classificacao="ALTA_PERFORMANCE", nivel_tecnico="MEDIO", nivel_comportamental="ALTO", potencial_lideranca="ALTO", resumo="Resumo 1", criado_em=datetime(2026, 5, 1, 10, 0))
        pt2 = PerfilTalentoModel(colaborador_id=colab1.id, classificacao="ESPECIALISTA_TECNICO", nivel_tecnico="ALTO", nivel_comportamental="MEDIO", potencial_lideranca="MEDIO", resumo="Resumo 2", criado_em=datetime(2026, 5, 20, 10, 0))
        db.session.add_all([pt1, pt2])

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


# 1. ADMIN acessa dashboard geral.
def test_admin_acessa_dashboard_geral(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["admin_email"])

    res = api_get(client, "/dashboard/mvp", token)
    assert res.status_code == 200
    data = res.get_json()
    assert data["resumo_geral"]["total_colaboradores"] == 2


# 2. RH acessa dashboard geral.
def test_rh_acessa_dashboard_geral(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["rh_email"])

    res = api_get(client, "/dashboard/mvp", token)
    assert res.status_code == 200
    data = res.get_json()
    assert data["resumo_geral"]["total_colaboradores"] == 2


# 3. LIDER acessa dashboard apenas com dados do seu setor.
def test_lider_acessa_dashboard_apenas_seu_setor(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["lidera_email"]) # Líder do Setor 1

    res = api_get(client, "/dashboard/mvp", token)
    assert res.status_code == 200
    data = res.get_json()
    # No Setor 1 temos apenas o Colaborador A
    assert data["resumo_geral"]["total_colaboradores"] == 1


# 4. LIDER não enxerga dados de colaboradores de outro setor.
def test_lider_nao_enxerga_dados_de_outro_setor(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["lidera_email"]) # Líder do Setor 1

    res = api_get(client, "/dashboard/mvp", token)
    assert res.status_code == 200
    data = res.get_json()
    
    # O Colaborador B (Setor 2) é inativo. Se o líder 1 visse o Colaborador B, colaboradores_inativos seria 1.
    assert data["resumo_geral"]["colaboradores_inativos"] == 0


# 5. COLABORADOR recebe 403 ao acessar dashboard.
def test_colaborador_recebe_403(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["colaba_email"])

    res = api_get(client, "/dashboard/mvp", token)
    assert res.status_code == 403
    assert res.get_json()["error"] == "FORBIDDEN"


# 6. Requisição sem token retorna 401.
def test_dashboard_sem_token_retorna_401(client):
    ids = seed_data(client.application)
    res = api_get(client, "/dashboard/mvp")
    assert res.status_code == 401


# 7. resumo_geral.total_colaboradores é calculado corretamente.
def test_total_colaboradores_calculado_corretamente(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["admin_email"])

    res = api_get(client, "/dashboard/mvp", token)
    data = res.get_json()
    assert data["resumo_geral"]["total_colaboradores"] == 2


# 8. colaboradores.ativos é calculado corretamente.
def test_colaboradores_ativos_calculado_corretamente(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["admin_email"])

    res = api_get(client, "/dashboard/mvp", token)
    data = res.get_json()
    assert data["colaboradores"]["ativos"] == 1
    assert data["colaboradores"]["inativos"] == 1


# 9. metas.concluidas é calculado corretamente.
def test_metas_concluidas_calculado_corretamente(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["admin_email"])

    res = api_get(client, "/dashboard/mvp", token)
    data = res.get_json()
    assert data["metas"]["concluidas"] == 1


# 10. metas.atrasadas é calculado corretamente.
def test_metas_atrasadas_calculado_corretamente(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["admin_email"])

    res = api_get(client, "/dashboard/mvp", token)
    data = res.get_json()
    assert data["metas"]["atrasadas"] == 1


# 11. pdis.ativos é calculado corretamente.
def test_pdis_ativos_calculado_corretamente(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["admin_email"])

    res = api_get(client, "/dashboard/mvp", token)
    data = res.get_json()
    assert data["pdis"]["ativos"] == 1


# 12. reconhecimentos.ativos considera apenas reconhecimentos ativos.
def test_reconhecimentos_ativos_calculado_corretamente(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["admin_email"])

    res = api_get(client, "/dashboard/mvp", token)
    data = res.get_json()
    assert data["reconhecimentos"]["ativos"] == 1
    assert data["reconhecimentos"]["cancelados"] == 1


# 13. perfis_talento considera apenas perfil mais recente de cada colaborador.
def test_perfis_talento_considera_apenas_mais_recente(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["admin_email"])

    res = api_get(client, "/dashboard/mvp", token)
    data = res.get_json()
    # Colaborador A: ESPECIALISTA_TECNICO (mais recente). Colaborador B: SEM_PERFIL.
    assert data["perfis_talento"]["ESPECIALISTA_TECNICO"] == 1
    assert data["perfis_talento"]["ALTA_PERFORMANCE"] == 0
    assert data["perfis_talento"]["SEM_PERFIL"] == 1


# 14. alertas.colaboradores_sem_avaliacao é calculado corretamente.
def test_colaboradores_sem_avaliacao_calculado_corretamente(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["admin_email"])

    res = api_get(client, "/dashboard/mvp", token)
    data = res.get_json()
    # Colaborador B não tem avaliações
    assert data["alertas"]["colaboradores_sem_avaliacao"] == 1


# 15. alertas.colaboradores_sem_perfil é calculado corretamente.
def test_colaboradores_sem_perfil_calculado_corretamente(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["admin_email"])

    res = api_get(client, "/dashboard/mvp", token)
    data = res.get_json()
    # Colaborador B não tem perfil
    assert data["alertas"]["colaboradores_sem_perfil"] == 1


# 16. Response contém todas as chaves principais esperadas.
def test_dashboard_response_contem_chaves_principais(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["admin_email"])

    res = api_get(client, "/dashboard/mvp", token)
    data = res.get_json()
    expected = [
        "resumo_geral",
        "colaboradores",
        "avaliacoes",
        "metas",
        "pdis",
        "feedbacks",
        "reconhecimentos",
        "perfis_talento",
        "alertas",
    ]
    for key in expected:
        assert key in data


# 17. Listas de últimos registros respeitam limite de 5 itens.
def test_listas_ultimos_respeitam_limite_de_5(client):
    ids = seed_data(client.application)
    # Vamos adicionar mais avaliações para o colaborador A para termos mais de 5 avaliações
    with client.application.app_context():
        for i in range(10):
            av = AvaliacaoModel(
                colaborador_id=ids["colab1_id"],
                avaliador_id=1,
                tipo="AVALIACAO_LIDER",
                observacao_geral=f"Extra {i}",
                data_avaliacao=datetime(2026, 5, 20 + i, 10, 0),
                criado_em=datetime(2026, 5, 20 + i, 10, 0),
                status="CONCLUIDA",
            )
            db.session.add(av)
        db.session.commit()

    token = get_token(client, ids["admin_email"])
    res = api_get(client, "/dashboard/mvp", token)
    data = res.get_json()

    assert len(data["avaliacoes"]["ultimas"]) == 5
