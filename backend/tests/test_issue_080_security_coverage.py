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
from domain.enums.pdi_enums import StatusPDI, OrigemPDI
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
from infrastructure.database.models.acao_pdi_model import AcaoPDIModel
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
        # Setores
        setor1 = SetorModel(nome="TI-Engenharia", descricao="Setor de Devs")
        setor2 = SetorModel(nome="Marketing", descricao="Setor de Mkt")
        db.session.add_all([setor1, setor2])
        db.session.commit()

        # Funções
        funcao1 = FuncaoModel(nome="Desenvolvedor", descricao="Devs")
        funcao2 = FuncaoModel(nome="Analista de Marketing", descricao="Mkt")
        db.session.add_all([funcao1, funcao2])
        db.session.commit()

        # Competências
        competencia1 = CompetenciaModel(nome="Python", descricao="Flask", tipo="TECNICA", peso=1.0, ativo=True)
        db.session.add(competencia1)
        db.session.commit()

        # Colaboradores
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
            funcao_id=funcao2.id,
        )
        colab3 = ColaboradorModel(
            nome="Colaborador C",
            matricula="M003",
            email="colabC@test.com",
            data_admissao=date(2026, 1, 1),
            status="ATIVO",
            setor_id=setor1.id,
            funcao_id=funcao1.id,
        )
        db.session.add_all([colab1, colab2, colab3])
        db.session.commit()

        # Usuários
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

        # Pre-seed resources (PDI, Metas, Reconhecimentos) for Colaborador A
        pdi_a = PDIModel(
            colaborador_id=colab1.id,
            criado_por_id=lider_a.id,
            titulo="PDI Colab A",
            descricao="Desc",
            origem=OrigemPDI.MANUAL.value,
            status=StatusPDI.ATIVO.value,
            data_inicio=date(2026, 5, 1),
            data_fim=date(2026, 6, 1),
        )
        pdi_b = PDIModel(
            colaborador_id=colab2.id,
            criado_por_id=lider_b.id,
            titulo="PDI Colab B",
            descricao="Desc",
            origem=OrigemPDI.MANUAL.value,
            status=StatusPDI.ATIVO.value,
            data_inicio=date(2026, 5, 1),
            data_fim=date(2026, 6, 1),
        )
        db.session.add_all([pdi_a, pdi_b])
        db.session.commit()

        acao_a = AcaoPDIModel(
            pdi_id=pdi_a.id,
            tipo="TREINAMENTO",
            descricao="Acao A",
            prazo=date(2026, 6, 1),
            status="PENDENTE",
        )
        acao_b = AcaoPDIModel(
            pdi_id=pdi_b.id,
            tipo="LEITURA",
            descricao="Acao B",
            prazo=date(2026, 6, 1),
            status="PENDENTE",
        )
        db.session.add_all([acao_a, acao_b])
        db.session.commit()

        meta_a = MetaModel(
            colaborador_id=colab1.id,
            criado_por_id=lider_a.id,
            titulo="Meta A",
            descricao="Desc A",
            prazo=date(2026, 12, 31),
            status=StatusMeta.PENDENTE.value,
            prioridade=PrioridadeMeta.MEDIA.value,
            origem="MANUAL",
        )
        meta_b = MetaModel(
            colaborador_id=colab2.id,
            criado_por_id=lider_b.id,
            titulo="Meta B",
            descricao="Desc B",
            prazo=date(2026, 12, 31),
            status=StatusMeta.PENDENTE.value,
            prioridade=PrioridadeMeta.MEDIA.value,
            origem="MANUAL",
        )
        db.session.add_all([meta_a, meta_b])
        db.session.commit()

        recon_a = ReconhecimentoModel(
            colaborador_id=colab1.id,
            registrado_por_id=lider_a.id,
            tipo=TipoReconhecimento.DESTAQUE.value,
            descricao="Recon A",
            evidencia="Evi A",
            ativo=True,
        )
        recon_b = ReconhecimentoModel(
            colaborador_id=colab2.id,
            registrado_por_id=lider_b.id,
            tipo=TipoReconhecimento.APOIO_EQUIPE.value,
            descricao="Recon B",
            evidencia="Evi B",
            ativo=True,
        )
        db.session.add_all([recon_a, recon_b])
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
            "colabb_email": "colabb_u@test.com",
            "admin_id": admin.id,
            "lidera_id": lider_a.id,
            "liderb_id": lider_b.id,
            "pdi_a_id": pdi_a.id,
            "pdi_b_id": pdi_b.id,
            "acao_a_id": acao_a.id,
            "acao_b_id": acao_b.id,
            "meta_a_id": meta_a.id,
            "meta_b_id": meta_b.id,
            "recon_a_id": recon_a.id,
            "recon_b_id": recon_b.id,
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


# ==============================================================================
# 1. HTTP 401 Sem Autenticação (Parametrizado para rotas operacionais do issue 080)
# ==============================================================================
UNAUTH_ROUTES = [
    ("POST", "/avaliacoes", {"colaborador_id": 1}),
    ("POST", "/metas", {"colaborador_id": 1}),
    ("GET", "/colaboradores/1/metas", None),
    ("POST", "/feedbacks", {"colaborador_id": 1}),
    ("POST", "/feedbacks/estruturar", {"observacao": "Teste"}),
    ("POST", "/pdis", {"colaborador_id": 1}),
    ("GET", "/pdis", None),
    ("GET", "/pdis/1", None),
    ("PATCH", "/pdis/1", {"titulo": "Editado"}),
    ("PATCH", "/pdis/1/concluir", None),
    ("PATCH", "/pdis/1/cancelar", None),
    ("GET", "/colaboradores/1/pdis", None),
    ("POST", "/pdis/1/acoes", {"tipo": "TREINAMENTO", "descricao": "Acao", "prazo": "2026-06-01"}),
    ("GET", "/pdis/1/acoes", None),
    ("PATCH", "/pdis/1/acoes/1", {"descricao": "Editado"}),
    ("PATCH", "/pdis/1/acoes/1/concluir", None),
    ("PATCH", "/pdis/1/acoes/1/cancelar", None),
    ("POST", "/reconhecimentos", {"colaborador_id": 1, "tipo": "DESTAQUE", "descricao": "Rec"}),
    ("GET", "/reconhecimentos", None),
    ("GET", "/reconhecimentos/1", None),
    ("PATCH", "/reconhecimentos/1/cancelar", {"motivo_cancelamento": "Erro"}),
    ("GET", "/colaboradores/1/reconhecimentos", None),
    ("GET", "/colaboradores/1/evolucao", None),
    ("GET", "/dashboard/mvp", None),
]


@pytest.mark.parametrize("method, url_tpl, payload", UNAUTH_ROUTES)
def test_issue_080_http_401_sem_autenticacao(client, method, url_tpl, payload):
    ids = seed_data(client.application)
    # Substituir marcador opcional de IDs nos templates de rotas
    url = url_tpl.replace("1", str(ids["colab1_id"])) if "1" in url_tpl else url_tpl
    res = make_request(client, method, url, payload)
    assert res.status_code == 401
    assert res.get_json()["error"] == "UNAUTHORIZED"


# ==============================================================================
# 2. HTTP 403 Perfil Insuficiente para COLABORADOR
# ==============================================================================
FORBIDDEN_COLAB_ROUTES = [
    ("POST", "/avaliacoes", {"colaborador_id": 1, "tipo": "AVALIACAO_LIDER", "observacao_geral": "Obs", "itens": []}),
    ("POST", "/metas", {"colaborador_id": 1, "titulo": "Meta A", "descricao": "Desc", "prazo": "2026-12-31", "prioridade": "MEDIA"}),
    ("POST", "/feedbacks", {"colaborador_id": 1, "contexto": "Feedback"}),
    ("POST", "/feedbacks/estruturar", {"observacao": "Teste observacao"}),
    ("POST", "/pdis", {"colaborador_id": 1, "titulo": "PDI A", "descricao": "Desc", "origem": "MANUAL", "data_inicio": "2026-05-01", "data_fim": "2026-06-01"}),
    ("PATCH", "/pdis/1", {"titulo": "Editado"}),
    ("PATCH", "/pdis/1/concluir", None),
    ("PATCH", "/pdis/1/cancelar", None),
    ("POST", "/pdis/1/acoes", {"tipo": "TREINAMENTO", "descricao": "Acao", "prazo": "2026-06-01"}),
    ("PATCH", "/pdis/1/acoes/1", {"descricao": "Editado"}),
    ("PATCH", "/pdis/1/acoes/1/concluir", None),
    ("PATCH", "/pdis/1/acoes/1/cancelar", None),
    ("POST", "/reconhecimentos", {"colaborador_id": 1, "tipo": "DESTAQUE", "descricao": "Rec"}),
    ("PATCH", "/reconhecimentos/1/cancelar", {"motivo_cancelamento": "Erro"}),
    ("GET", "/dashboard/mvp", None),
]


@pytest.mark.parametrize("method, url_tpl, payload", FORBIDDEN_COLAB_ROUTES)
def test_issue_080_http_403_perfil_insuficiente_colaborador(client, method, url_tpl, payload):
    ids = seed_data(client.application)
    token = get_token(client, ids["colaba_email"])

    # Ajustar IDs
    url = url_tpl
    if "/pdis/1/acoes/1" in url_tpl:
        url = f"/pdis/{ids['pdi_a_id']}/acoes/{ids['acao_a_id']}"
    elif "/pdis/1/acoes" in url_tpl:
        url = f"/pdis/{ids['pdi_a_id']}/acoes"
    elif "/pdis/1" in url_tpl:
        url = f"/pdis/{ids['pdi_a_id']}"
    elif "/reconhecimentos/1" in url_tpl:
        url = f"/reconhecimentos/{ids['recon_a_id']}/cancelar"

    if payload:
        # Se contiver colaborador_id ou similar, corrigir
        if "colaborador_id" in payload:
            payload = payload.copy()
            payload["colaborador_id"] = ids["colab1_id"]

    res = make_request(client, method, url, payload, token)
    assert res.status_code == 403
    assert res.get_json()["error"] == "FORBIDDEN"


# ==============================================================================
# 2.C.1 Acesso Permitido do COLABORADOR aos Próprios Recursos
# ==============================================================================
def test_issue_080_colaborador_acessa_proprios_recursos(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["colaba_email"])

    # GET /colaboradores/<id>/metas
    res = make_request(client, "GET", f"/colaboradores/{ids['colab1_id']}/metas", token=token)
    assert res.status_code == 200
    assert len(res.get_json()) == 1
    assert res.get_json()[0]["titulo"] == "Meta A"

    # GET /colaboradores/<id>/pdis
    res = make_request(client, "GET", f"/colaboradores/{ids['colab1_id']}/pdis", token=token)
    assert res.status_code == 200
    assert len(res.get_json()) == 1
    assert res.get_json()[0]["titulo"] == "PDI Colab A"

    # GET /pdis (Listagem geral - deve retornar apenas do próprio)
    res = make_request(client, "GET", "/pdis", token=token)
    assert res.status_code == 200
    pdis = res.get_json()
    assert len(pdis) == 1
    assert pdis[0]["id"] == ids["pdi_a_id"]

    # GET /pdis/<id>
    res = make_request(client, "GET", f"/pdis/{ids['pdi_a_id']}", token=token)
    assert res.status_code == 200

    # GET /pdis/<id>/acoes
    res = make_request(client, "GET", f"/pdis/{ids['pdi_a_id']}/acoes", token=token)
    assert res.status_code == 200
    assert len(res.get_json()) == 1
    assert res.get_json()[0]["id"] == ids["acao_a_id"]

    # GET /colaboradores/<id>/reconhecimentos
    res = make_request(client, "GET", f"/colaboradores/{ids['colab1_id']}/reconhecimentos", token=token)
    assert res.status_code == 200
    assert len(res.get_json()) == 1
    assert res.get_json()[0]["descricao"] == "Recon A"

    # GET /reconhecimentos (Listagem geral - apenas do próprio)
    res = make_request(client, "GET", "/reconhecimentos", token=token)
    assert res.status_code == 200
    recons = res.get_json()
    assert len(recons) == 1
    assert recons[0]["id"] == ids["recon_a_id"]

    # GET /reconhecimentos/<id>
    res = make_request(client, "GET", f"/reconhecimentos/{ids['recon_a_id']}", token=token)
    assert res.status_code == 200

    # GET /colaboradores/<id>/evolucao
    res = make_request(client, "GET", f"/colaboradores/{ids['colab1_id']}/evolucao", token=token)
    assert res.status_code == 200
    assert res.get_json()["colaborador"]["nome"] == "Colaborador A"


# ==============================================================================
# 2.C.2 Bloqueio do COLABORADOR ao Acessar Recursos de Outro Colaborador
# ==============================================================================
def test_issue_080_colaborador_bloqueado_recursos_alheios(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["colaba_email"]) # Colaborador A

    # GET /colaboradores/<colab2_id>/metas
    res = make_request(client, "GET", f"/colaboradores/{ids['colab2_id']}/metas", token=token)
    assert res.status_code == 403
    assert res.get_json()["error"] == "FORBIDDEN"

    # GET /colaboradores/<colab2_id>/pdis
    res = make_request(client, "GET", f"/colaboradores/{ids['colab2_id']}/pdis", token=token)
    assert res.status_code == 403

    # GET /pdis/<pdi_b_id>
    res = make_request(client, "GET", f"/pdis/{ids['pdi_b_id']}", token=token)
    assert res.status_code == 403

    # GET /pdis/<pdi_b_id>/acoes
    res = make_request(client, "GET", f"/pdis/{ids['pdi_b_id']}/acoes", token=token)
    assert res.status_code == 403

    # GET /colaboradores/<colab2_id>/reconhecimentos
    res = make_request(client, "GET", f"/colaboradores/{ids['colab2_id']}/reconhecimentos", token=token)
    assert res.status_code == 403

    # GET /reconhecimentos/<recon_b_id>
    res = make_request(client, "GET", f"/reconhecimentos/{ids['recon_b_id']}", token=token)
    assert res.status_code == 403

    # GET /colaboradores/<colab2_id>/evolucao
    res = make_request(client, "GET", f"/colaboradores/{ids['colab2_id']}/evolucao", token=token)
    assert res.status_code == 403


# ==============================================================================
# 2.C.3 Integridade entre pdi_id e acao_id (Retorna 404 para Acao que não pertence ao PDI)
# ==============================================================================
def test_issue_080_integridade_pdi_e_acao(client):
    ids = seed_data(client.application)
    token = get_token(client, ids["admin_email"])

    # Tenta atualizar acao_b associando-a com pdi_a (acao_b pertence a pdi_b)
    url = f"/pdis/{ids['pdi_a_id']}/acoes/{ids['acao_b_id']}"
    payload = {"tipo": "TREINAMENTO", "descricao": "Editando com PDI errado", "prazo": "2026-06-01"}

    res = make_request(client, "PATCH", url, payload, token)
    assert res.status_code == 404
    assert res.get_json()["error"] == "NOT_FOUND"
    assert "Acao nao encontrada para este PDI" in res.get_json()["message"]

    # Mesma integridade em Concluir Ação
    res_concluir = make_request(client, "PATCH", f"/pdis/{ids['pdi_a_id']}/acoes/{ids['acao_b_id']}/concluir", None, token)
    assert res_concluir.status_code == 404

    # Mesma integridade em Cancelar Ação
    res_cancelar = make_request(client, "PATCH", f"/pdis/{ids['pdi_a_id']}/acoes/{ids['acao_b_id']}/cancelar", None, token)
    assert res_cancelar.status_code == 404


# ==============================================================================
# 3. HTTP 403 Fora de Escopo (Líder Cruzado tentando mexer em outro setor)
# ==============================================================================
def test_issue_080_lider_fora_do_escopo(client):
    ids = seed_data(client.application)
    token_a = get_token(client, ids["lidera_email"]) # Líder do Setor 1

    # 1. Criar avaliação para Colaborador B (Setor 2)
    payload_av = {
        "colaborador_id": ids["colab2_id"],
        "tipo": "AVALIACAO_LIDER",
        "observacao_geral": "Obs",
        "itens": [{"competencia_id": ids["competencia1_id"], "nota": 4, "comentario": "Ok"}]
    }
    res = make_request(client, "POST", "/avaliacoes", payload_av, token_a)
    assert res.status_code == 403

    # 2. Criar meta para Colaborador B
    payload_meta = {
        "colaborador_id": ids["colab2_id"],
        "titulo": "Meta cruzada",
        "descricao": "Desc",
        "prazo": "2026-12-31",
        "prioridade": "MEDIA"
    }
    res = make_request(client, "POST", "/metas", payload_meta, token_a)
    assert res.status_code == 403

    # 3. Listar metas de Colaborador B
    res = make_request(client, "GET", f"/colaboradores/{ids['colab2_id']}/metas", token=token_a)
    assert res.status_code == 403

    # 4. Criar feedback para Colaborador B
    payload_fb = {
        "colaborador_id": ids["colab2_id"],
        "contexto": "Feedback cruzado",
        "ponto_positivo": "Bom trabalho",
        "acao_recomendada": "Continuar assim"
    }
    res = make_request(client, "POST", "/feedbacks", payload_fb, token_a)
    assert res.status_code == 403

    # 5. Criar PDI para Colaborador B
    payload_pdi = {
        "colaborador_id": ids["colab2_id"],
        "titulo": "PDI Cruzado",
        "descricao": "Desc",
        "origem": "MANUAL",
        "data_inicio": "2026-05-01",
        "data_fim": "2026-06-01"
    }
    res = make_request(client, "POST", "/pdis", payload_pdi, token_a)
    assert res.status_code == 403

    # 6. Atualizar PDI B (Setor 2)
    res = make_request(client, "PATCH", f"/pdis/{ids['pdi_b_id']}", {"titulo": "Editado por Lider A"}, token_a)
    assert res.status_code == 403

    # 7. Concluir PDI B
    res = make_request(client, "PATCH", f"/pdis/{ids['pdi_b_id']}/concluir", None, token_a)
    assert res.status_code == 403

    # 8. Cancelar PDI B
    res = make_request(client, "PATCH", f"/pdis/{ids['pdi_b_id']}/cancelar", None, token_a)
    assert res.status_code == 403

    # 9. Listar PDIs do Colaborador B
    res = make_request(client, "GET", f"/colaboradores/{ids['colab2_id']}/pdis", token=token_a)
    assert res.status_code == 403

    # 10. Criar Ação no PDI B
    res = make_request(client, "POST", f"/pdis/{ids['pdi_b_id']}/acoes", {"tipo": "LEITURA", "descricao": "A", "prazo": "2026-06-01"}, token_a)
    assert res.status_code == 403

    # 11. Atualizar Ação no PDI B
    res = make_request(client, "PATCH", f"/pdis/{ids['pdi_b_id']}/acoes/{ids['acao_b_id']}", {"tipo": "TREINAMENTO", "descricao": "Editada", "prazo": "2026-06-01"}, token_a)
    assert res.status_code == 403

    # 12. Criar Reconhecimento para Colaborador B
    payload_rec = {"colaborador_id": ids["colab2_id"], "tipo": "APOIO_EQUIPE", "descricao": "Recon", "evidencia": "Fez um excelente trabalho"}
    res = make_request(client, "POST", "/reconhecimentos", payload_rec, token_a)
    assert res.status_code == 403

    # 13. Cancelar Reconhecimento B
    res = make_request(client, "PATCH", f"/reconhecimentos/{ids['recon_b_id']}/cancelar", {"motivo_cancelamento": "Cancelado por Lider A"}, token_a)
    assert res.status_code == 403

    # 14. Listar reconhecimentos de Colaborador B
    res = make_request(client, "GET", f"/colaboradores/{ids['colab2_id']}/reconhecimentos", token=token_a)
    assert res.status_code == 403

    # 15. Acessar evolução de Colaborador B
    res = make_request(client, "GET", f"/colaboradores/{ids['colab2_id']}/evolucao", token=token_a)
    assert res.status_code == 403


# ==============================================================================
# 2.C.4 Ausência de Persistência para Bloqueios nos Módulos de Escrita
# ==============================================================================
def test_issue_080_ausencia_de_persistencia_apos_bloqueio(client):
    ids = seed_data(client.application)
    token_a = get_token(client, ids["lidera_email"]) # Lider do Setor 1

    # 1. POST /avaliacoes para Colab B
    payload_av = {
        "colaborador_id": ids["colab2_id"],
        "tipo": "AVALIACAO_LIDER",
        "observacao_geral": "Invalida",
        "itens": []
    }
    make_request(client, "POST", "/avaliacoes", payload_av, token_a)
    with client.application.app_context():
        assert db.session.query(AvaliacaoModel).filter_by(observacao_geral="Invalida").first() is None

    # 2. POST /metas para Colab B
    payload_meta = {
        "colaborador_id": ids["colab2_id"],
        "titulo": "Meta Invalida",
        "descricao": "Desc",
        "prazo": "2026-12-31",
        "prioridade": "MEDIA"
    }
    make_request(client, "POST", "/metas", payload_meta, token_a)
    with client.application.app_context():
        assert db.session.query(MetaModel).filter_by(titulo="Meta Invalida").first() is None

    # 3. POST /feedbacks para Colab B
    payload_fb = {
        "colaborador_id": ids["colab2_id"],
        "contexto": "Feedback Invalido",
        "ponto_positivo": "Bom trabalho",
        "acao_recomendada": "Continuar assim"
    }
    make_request(client, "POST", "/feedbacks", payload_fb, token_a)
    with client.application.app_context():
        assert db.session.query(FeedbackModel).filter_by(contexto="Feedback Invalido").first() is None

    # 4. POST /pdis para Colab B
    payload_pdi = {
        "colaborador_id": ids["colab2_id"],
        "titulo": "PDI Invalido",
        "descricao": "Desc",
        "origem": "MANUAL",
        "data_inicio": "2026-05-01",
        "data_fim": "2026-06-01"
    }
    make_request(client, "POST", "/pdis", payload_pdi, token_a)
    with client.application.app_context():
        assert db.session.query(PDIModel).filter_by(titulo="PDI Invalido").first() is None

    # 5. POST /pdis/<pdi_b_id>/acoes (Lider A tenta adicionar ação no PDI B)
    make_request(client, "POST", f"/pdis/{ids['pdi_b_id']}/acoes", {"tipo": "LEITURA", "descricao": "Acao Invalida", "prazo": "2026-06-01"}, token_a)
    with client.application.app_context():
        assert db.session.query(AcaoPDIModel).filter_by(descricao="Acao Invalida").first() is None

    # 6. POST /reconhecimentos para Colab B
    payload_rec = {"colaborador_id": ids["colab2_id"], "tipo": "APOIO_EQUIPE", "descricao": "Recon Invalido", "evidencia": "Fez um excelente trabalho"}
    make_request(client, "POST", "/reconhecimentos", payload_rec, token_a)
    with client.application.app_context():
        assert db.session.query(ReconhecimentoModel).filter_by(descricao="Recon Invalido").first() is None

    # 7. PATCH /pdis/<pdi_b_id> (Título original é "PDI Colab B")
    make_request(client, "PATCH", f"/pdis/{ids['pdi_b_id']}", {"titulo": "Tentativa de Alteracao"}, token_a)
    with client.application.app_context():
        pdi = db.session.get(PDIModel, ids["pdi_b_id"])
        assert pdi.titulo == "PDI Colab B"

    # 8. PATCH /pdis/<pdi_b_id>/concluir (Status original é ATIVO)
    make_request(client, "PATCH", f"/pdis/{ids['pdi_b_id']}/concluir", None, token_a)
    with client.application.app_context():
        pdi = db.session.get(PDIModel, ids["pdi_b_id"])
        assert pdi.status == "ATIVO"

    # 9. PATCH /reconhecimentos/<recon_b_id>/cancelar (Ativo original é True)
    make_request(client, "PATCH", f"/reconhecimentos/{ids['recon_b_id']}/cancelar", {"motivo_cancelamento": "Erro"}, token_a)
    with client.application.app_context():
        rec = db.session.get(ReconhecimentoModel, ids["recon_b_id"])
        assert rec.ativo is True
        assert rec.cancelado_por_id is None


# ==============================================================================
# 2.C.5 Operações representativas executadas com RH
# ==============================================================================
def test_issue_080_operacoes_permitidas_rh(client):
    ids = seed_data(client.application)
    token_rh = get_token(client, ids["rh_email"])

    # RH cria avaliação para Colaborador B (Setor 2)
    payload_av = {
        "colaborador_id": ids["colab2_id"],
        "tipo": "AVALIACAO_LIDER",
        "observacao_geral": "RH Avaliacao",
        "itens": [{"competencia_id": ids["competencia1_id"], "nota": 5, "comentario": "Otimo"}]
    }
    res = make_request(client, "POST", "/avaliacoes", payload_av, token_rh)
    assert res.status_code == 201

    # RH cria meta para Colaborador B
    payload_meta = {
        "colaborador_id": ids["colab2_id"],
        "titulo": "Meta RH",
        "descricao": "Desc",
        "prazo": "2026-12-31",
        "prioridade": "MEDIA"
    }
    res = make_request(client, "POST", "/metas", payload_meta, token_rh)
    assert res.status_code == 201

    # RH cria feedback para Colaborador B
    payload_fb = {
        "colaborador_id": ids["colab2_id"],
        "contexto": "Feedback RH",
        "ponto_positivo": "Bom trabalho",
        "acao_recomendada": "Continuar assim"
    }
    res = make_request(client, "POST", "/feedbacks", payload_fb, token_rh)
    assert res.status_code == 201

    # RH cria PDI para Colaborador B
    payload_pdi = {
        "colaborador_id": ids["colab2_id"],
        "titulo": "PDI RH",
        "descricao": "Desc",
        "origem": "MANUAL",
        "data_inicio": "2026-05-01",
        "data_fim": "2026-06-01"
    }
    res = make_request(client, "POST", "/pdis", payload_pdi, token_rh)
    assert res.status_code == 201
    pdi_id = res.get_json()["id"]

    # RH cancela Reconhecimento B
    res = make_request(client, "PATCH", f"/reconhecimentos/{ids['recon_b_id']}/cancelar", {"motivo_cancelamento": "RH Cancelou"}, token_rh)
    assert res.status_code == 200
    with client.application.app_context():
        rec = db.session.get(ReconhecimentoModel, ids["recon_b_id"])
        assert rec.ativo is False
        assert rec.motivo_cancelamento == "RH Cancelou"


# ==============================================================================
# 5. Autoria e Spoofing Ignorado
# ==============================================================================
def test_issue_080_autoria_jwt_e_mitigacao_spoofing(client):
    ids = seed_data(client.application)
    token_a = get_token(client, ids["lidera_email"])

    # 1. POST /avaliacoes com spoofing de avaliador_id
    payload_av = {
        "colaborador_id": ids["colab1_id"],
        "tipo": "AVALIACAO_LIDER",
        "observacao_geral": "Teste Autoria",
        "avaliador_id": ids["liderb_id"], # Tentativa de Spoofing
        "itens": [{"competencia_id": ids["competencia1_id"], "nota": 4, "comentario": "Ok"}]
    }
    res = make_request(client, "POST", "/avaliacoes", payload_av, token_a)
    assert res.status_code == 201
    with client.application.app_context():
        av = db.session.query(AvaliacaoModel).filter_by(observacao_geral="Teste Autoria").first()
        assert av.avaliador_id == ids["lidera_id"] # Deve persistir LIDER A

    # 2. POST /metas com spoofing de criado_por_id
    payload_meta = {
        "colaborador_id": ids["colab1_id"],
        "titulo": "Meta Autoria",
        "descricao": "Desc",
        "prazo": "2026-12-31",
        "prioridade": "MEDIA",
        "criado_por_id": ids["liderb_id"] # Tentativa de Spoofing
    }
    res = make_request(client, "POST", "/metas", payload_meta, token_a)
    assert res.status_code == 201
    with client.application.app_context():
        meta = db.session.query(MetaModel).filter_by(titulo="Meta Autoria").first()
        assert meta.criado_por_id == ids["lidera_id"]

    # 3. POST /feedbacks com spoofing de autor_id
    payload_fb = {
        "colaborador_id": ids["colab1_id"],
        "contexto": "Feedback Autoria",
        "ponto_positivo": "Bom trabalho",
        "acao_recomendada": "Continuar assim",
        "autor_id": ids["liderb_id"] # Tentativa de Spoofing
    }
    res = make_request(client, "POST", "/feedbacks", payload_fb, token_a)
    assert res.status_code == 201
    with client.application.app_context():
        fb = db.session.query(FeedbackModel).filter_by(contexto="Feedback Autoria").first()
        assert fb.autor_id == ids["lidera_id"]

    # 4. POST /pdis com spoofing de criado_por_id
    payload_pdi = {
        "colaborador_id": ids["colab1_id"],
        "titulo": "PDI Autoria",
        "descricao": "Desc",
        "origem": "MANUAL",
        "data_inicio": "2026-05-01",
        "data_fim": "2026-06-01",
        "criado_por_id": ids["liderb_id"] # Tentativa de Spoofing
    }
    res = make_request(client, "POST", "/pdis", payload_pdi, token_a)
    assert res.status_code == 201
    with client.application.app_context():
        pdi = db.session.query(PDIModel).filter_by(titulo="PDI Autoria").first()
        assert pdi.criado_por_id == ids["lidera_id"]

    # 5. POST /reconhecimentos com spoofing de registrado_por_id
    payload_rec = {
        "colaborador_id": ids["colab1_id"],
        "tipo": "DESTAQUE",
        "descricao": "Recon Autoria",
        "evidencia": "Fez um excelente trabalho",
        "registrado_por_id": ids["liderb_id"] # Tentativa de Spoofing
    }
    res = make_request(client, "POST", "/reconhecimentos", payload_rec, token_a)
    assert res.status_code == 201
    with client.application.app_context():
        rec = db.session.query(ReconhecimentoModel).filter_by(descricao="Recon Autoria").first()
        assert rec.registrado_por_id == ids["lidera_id"]

    # 6. PATCH /reconhecimentos/<id>/cancelar com spoofing de cancelado_por_id
    # RH faz o cancelamento mas envia liderb no payload
    token_rh = get_token(client, ids["rh_email"])
    payload_cancel = {
        "motivo_cancelamento": "Cancelado RH",
        "cancelado_por_id": ids["liderb_id"] # Tentativa de Spoofing
    }
    res = make_request(client, "PATCH", f"/reconhecimentos/{ids['recon_a_id']}/cancelar", payload_cancel, token_rh)
    assert res.status_code == 200
    with client.application.app_context():
        rec = db.session.get(ReconhecimentoModel, ids["recon_a_id"])
        assert rec.ativo is False
        assert rec.cancelado_por_id == ids["rh_email"] or rec.cancelado_por_id is not None
        # O ID deve corresponder ao usuário logado (RH)
        rh_user = db.session.query(UsuarioModel).filter_by(email=ids["rh_email"]).first()
        assert rec.cancelado_por_id == rh_user.id


# ==============================================================================
# 2.C.6 Identidade Exata dos Registros nas Listagens (Garante que Lider/Colaborador só vê os seus)
# ==============================================================================
def test_issue_080_identidade_exata_nas_listagens(client):
    ids = seed_data(client.application)
    token_lider_a = get_token(client, ids["lidera_email"])
    token_colab_a = get_token(client, ids["colaba_email"])

    # A. LISTAGEM DE PDI (/pdis)
    # Lider A deve ver apenas PDI A (Setor 1)
    res_la_pdi = make_request(client, "GET", "/pdis", token=token_lider_a)
    assert res_la_pdi.status_code == 200
    data_la_pdi = res_la_pdi.get_json()
    assert len(data_la_pdi) == 1
    assert data_la_pdi[0]["id"] == ids["pdi_a_id"]
    assert data_la_pdi[0]["colaborador_id"] == ids["colab1_id"]

    # Colaborador A deve ver apenas PDI A
    res_ca_pdi = make_request(client, "GET", "/pdis", token=token_colab_a)
    assert res_ca_pdi.status_code == 200
    data_ca_pdi = res_ca_pdi.get_json()
    assert len(data_ca_pdi) == 1
    assert data_ca_pdi[0]["id"] == ids["pdi_a_id"]

    # B. LISTAGEM DE RECONHECIMENTOS (/reconhecimentos)
    # Lider A deve ver apenas Recon A
    res_la_rec = make_request(client, "GET", "/reconhecimentos", token=token_lider_a)
    assert res_la_rec.status_code == 200
    data_la_rec = res_la_rec.get_json()
    assert len(data_la_rec) == 1
    assert data_la_rec[0]["id"] == ids["recon_a_id"]

    # Colaborador A deve ver apenas Recon A
    res_ca_rec = make_request(client, "GET", "/reconhecimentos", token=token_colab_a)
    assert res_ca_rec.status_code == 200
    data_ca_rec = res_ca_rec.get_json()
    assert len(data_ca_rec) == 1
    assert data_ca_rec[0]["id"] == ids["recon_a_id"]


# ==============================================================================
# 2.C.7 Contagens, Listas Recentes e Alertas do Dashboard Dentro do Escopo
# ==============================================================================
def test_issue_080_dashboard_dentro_do_escopo(client):
    ids = seed_data(client.application)

    # Adicionar uma avaliação para Colaborador A para que Lider A tenha no dashboard
    token_admin = get_token(client, ids["admin_email"])
    payload_av = {
        "colaborador_id": ids["colab1_id"],
        "tipo": "AVALIACAO_LIDER",
        "observacao_geral": "Avaliacao Recente A",
        "itens": [{"competencia_id": ids["competencia1_id"], "nota": 4, "comentario": "Ok"}]
    }
    make_request(client, "POST", "/avaliacoes", payload_av, token_admin)

    # Lider A do Setor 1 consulta o dashboard
    token_lider_a = get_token(client, ids["lidera_email"])
    res = make_request(client, "GET", "/dashboard/mvp", token=token_lider_a)
    assert res.status_code == 200
    data = res.get_json()

    # Contagens gerais do dashboard
    # Setor 1 tem 2 colaboradores (Colaborador A e C). O Colaborador B (Setor 2) deve ser omitido.
    assert data["resumo_geral"]["total_colaboradores"] == 2
    assert data["colaboradores"]["ativos"] == 2
    assert data["colaboradores"]["inativos"] == 0

    # Metas, PDIs e Reconhecimentos
    assert data["metas"]["pendentes"] == 1 # Apenas Meta A
    assert data["pdis"]["ativos"] == 1 # Apenas PDI A
    assert data["reconhecimentos"]["ativos"] == 1 # Apenas Recon A

    # Alertas
    # Colaborador C não tem perfil de talento associado (1 sem perfil). Colaborador A agora tem (graças à avaliação recente).
    assert data["alertas"]["colaboradores_sem_perfil"] == 1
    assert data["alertas"]["colaboradores_sem_avaliacao"] == 1

    # Listas recentes
    assert len(data["avaliacoes"]["ultimas"]) == 1
    assert data["avaliacoes"]["ultimas"][0]["tipo"] == "AVALIACAO_LIDER"


# ==============================================================================
# 2.C.8 Separação do Endpoint /feedbacks/estruturar (Autorização Perfil, Sem Escopo Colaborador)
# ==============================================================================
def test_issue_080_estruturar_feedback_sem_escopo_colaborador(client):
    ids = seed_data(client.application)

    payload = {"observacao": "Colaborador tem demonstrado muito esforco e dedicação."}

    # Lider A (LIDER) acessa com sucesso
    token_lider = get_token(client, ids["lidera_email"])
    res_lider = make_request(client, "POST", "/feedbacks/estruturar", payload, token_lider)
    assert res_lider.status_code == 200
    data_lider = res_lider.get_json()
    assert data_lider["contexto"] == payload["observacao"]
    assert "ponto_positivo" in data_lider

    # RH (RH) acessa com sucesso
    token_rh = get_token(client, ids["rh_email"])
    res_rh = make_request(client, "POST", "/feedbacks/estruturar", payload, token_rh)
    assert res_rh.status_code == 200

    # Admin (ADMIN) acessa com sucesso
    token_admin = get_token(client, ids["admin_email"])
    res_admin = make_request(client, "POST", "/feedbacks/estruturar", payload, token_admin)
    assert res_admin.status_code == 200

    # Colaborador A (COLABORADOR) tenta acessar -> 403 Forbidden (por causa do decorator roles_required)
    token_colab = get_token(client, ids["colaba_email"])
    res_colab = make_request(client, "POST", "/feedbacks/estruturar", payload, token_colab)
    assert res_colab.status_code == 403
    assert res_colab.get_json()["error"] == "FORBIDDEN"
