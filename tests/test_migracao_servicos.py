import pytest
from datetime import date
from app import create_app
from app.config import Config
from app.extensions import db
from infrastructure.database.base import Base
from infrastructure.database.models.execucao_agente_model import ExecucaoAgenteModel
from infrastructure.database.models.meta_model import MetaModel

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


def test_estruturar_feedback(client):
    # Fluxo feliz
    res = client.post("/feedbacks/estruturar", json={"observacao": "Sempre ajuda o time nas sprints."})
    assert res.status_code == 200
    data = res.get_json()
    assert data["contexto"] == "Sempre ajuda o time nas sprints."
    assert "ponto_positivo" in data
    assert "ponto_melhoria" in data
    assert "acao_recomendada" in data
    assert data["tom"] == "CONSTRUTIVO"

    # Erro de validação
    res = client.post("/feedbacks/estruturar", json={"observacao": ""})
    assert res.status_code == 400


def test_colaborador_metas(client):
    # 1. Tentar obter de colaborador inexistente
    res = client.get("/colaboradores/999/metas")
    assert res.status_code == 404

    # 2. Criar setor, funcao e colaborador
    res = client.post("/setores", json={"nome": "TI", "descricao": "Tecnologia"})
    setor_id = res.get_json()["id"]

    res = client.post("/funcoes", json={"nome": "Developer", "descricao": "Dev", "setor_id": setor_id})
    funcao_id = res.get_json()["id"]

    res = client.post("/colaboradores", json={
        "nome": "John Doe",
        "email": "john@doe.com",
        "matricula": "12345",
        "funcao_id": funcao_id,
        "setor_id": setor_id,
    })
    colaborador_id = res.get_json()["id"]

    # 3. GET metas (deve vir vazio)
    res = client.get(f"/colaboradores/{colaborador_id}/metas")
    assert res.status_code == 200
    assert res.get_json() == []

    # 4. Adicionar uma meta diretamente no DB para testar listagem
    # (Poderíamos também criar via caso de uso se houvesse endpoint exposto)
    meta_model = MetaModel(
        colaborador_id=colaborador_id,
        criado_por_id=1,  # mock
        titulo="Melhorar Python",
        descricao="Estudar async",
        indicador="Concluir curso",
        prazo=date(2026, 12, 31),
        prioridade="MEDIA",
        status="PENDENTE",
        origem="MANUAL",
    )
    db.session.add(meta_model)
    db.session.commit()

    # 5. GET metas novamente
    res = client.get(f"/colaboradores/{colaborador_id}/metas")
    assert res.status_code == 200
    metas = res.get_json()
    assert len(metas) == 1
    assert metas[0]["titulo"] == "Melhorar Python"


def test_colaborador_evolucao_e_logs_agente(client):
    # 1. Tentar obter de colaborador inexistente
    res = client.get("/colaboradores/999/evolucao")
    assert res.status_code == 404

    # 2. Criar setor, funcao, colaborador e usuario avaliador
    res = client.post("/setores", json={"nome": "TI", "descricao": "Tecnologia"})
    setor_id = res.get_json()["id"]

    res = client.post("/funcoes", json={"nome": "Developer", "descricao": "Dev", "setor_id": setor_id})
    funcao_id = res.get_json()["id"]

    res = client.post("/colaboradores", json={
        "nome": "Jane Doe",
        "email": "jane@doe.com",
        "matricula": "54321",
        "funcao_id": funcao_id,
        "setor_id": setor_id,
    })
    colaborador_id = res.get_json()["id"]

    res = client.post("/usuarios", json={
        "nome": "Manager",
        "email": "manager@company.com",
        "perfil": "ADMIN",
        "senha": "password123",
    })
    assert res.status_code == 201
    avaliador_id = res.get_json()["id"]

    # 3. GET evolucao inicial
    res = client.get(f"/colaboradores/{colaborador_id}/evolucao")
    assert res.status_code == 200
    evolucao = res.get_json()
    assert evolucao["indicadores"]["media_tecnica"] == 0.0
    assert evolucao["indicadores"]["media_comportamental"] == 0.0
    assert evolucao["indicadores"]["perfil_atual"] is None

    # 4. Criar competências para poder avaliar
    res = client.post("/competencias", json={"nome": "Python", "tipo": "TECNICA", "peso": 2.0})
    comp_tecnica_id = res.get_json()["id"]

    res = client.post("/competencias", json={"nome": "Comunicacao", "tipo": "COMPORTAMENTAL", "peso": 1.0})
    comp_comportamental_id = res.get_json()["id"]

    # 5. Registrar Avaliacao (isso gera perfil e logs de ExecucaoAgente)
    res = client.post("/avaliacoes", json={
        "colaborador_id": colaborador_id,
        "avaliador_id": avaliador_id,
        "tipo": "AVALIACAO_LIDER",
        "observacao_geral": "Otimo desempenho",
        "itens": [
            {"competencia_id": comp_tecnica_id, "nota": 4, "comentario": "Bom codigo"},
            {"competencia_id": comp_comportamental_id, "nota": 5, "comentario": "Excelente comunicacao"}
        ]
    })
    assert res.status_code == 201

    # 6. Validar que logs de ExecucaoAgente foram salvos no DB
    execucoes = db.session.query(ExecucaoAgenteModel).all()
    assert len(execucoes) == 2
    agente_nomes = [e.agente_nome for e in execucoes]
    assert "Agente Avaliador" in agente_nomes
    assert "Agente Perfilador" in agente_nomes

    # 7. GET evolucao apos avaliacao
    res = client.get(f"/colaboradores/{colaborador_id}/evolucao")
    assert res.status_code == 200
    evolucao = res.get_json()
    assert evolucao["indicadores"]["media_tecnica"] == 4.0
    assert evolucao["indicadores"]["media_comportamental"] == 5.0
    assert evolucao["indicadores"]["perfil_atual"] is not None
    assert len(evolucao["avaliacoes"]) == 1
    assert len(evolucao["avaliacoes"][0]["itens"]) == 2
