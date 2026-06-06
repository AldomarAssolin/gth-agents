import pytest
import json
from decimal import Decimal

from app import create_app
from app.config import Config
from app.extensions import db

from application.dtos.cadastro_dto import CriarUsuarioDTO
from application.use_cases.cadastros_basicos_uc import CriarUsuarioUC

from domain.entities.avaliacao import Avaliacao
from domain.entities.item_avaliacao import ItemAvaliacao
from domain.entities.competencia import Competencia
from domain.enums.tipo_competencia import TipoCompetencia
from domain.enums.perfil_usuario import PerfilUsuario
from domain.services.calculadora_competencias import CalculadoraCompetencias

from infrastructure.database.base import Base
# Force loading models to register in metadata
import infrastructure.database.models  # noqa
from interface.schemas.serializers import serialize


class FakeUsuarioRepository:
    def __init__(self):
        self.usuarios = []

    def get_by_id(self, usuario_id: int):
        return next((usuario for usuario in self.usuarios if usuario.id == usuario_id), None)

    def list(self):
        return self.usuarios

    def get_by_email(self, email: str):
        return next((usuario for usuario in self.usuarios if usuario.email == email), None)

    def add(self, usuario):
        usuario.id = 1
        self.usuarios.append(usuario)
        return usuario


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


def test_criar_usuario_hash_senha_e_nao_retorna_hash():
    repo = FakeUsuarioRepository()
    uc = CriarUsuarioUC(repo)
    senha = "senha-super-secreta"

    usuario = uc.execute(
        CriarUsuarioDTO(
            nome="Usuario Seguro",
            email="seguro@example.com",
            senha=senha,
            perfil=PerfilUsuario.RH,
        )
    )

    response_data = serialize(usuario)

    assert "senha" not in response_data
    assert "senha_hash" not in response_data
    assert usuario.senha_hash != senha
    assert usuario.check_password_hash(senha)


def test_post_usuarios_endpoint_security(client):
    payload = {
        "nome": "Usuario Seguro HTTP",
        "email": "seguro_http@example.com",
        "senha": "senha-super-secreta-http",
        "perfil": "RH"
    }
    response = client.post(
        "/usuarios",
        data=json.dumps(payload),
        content_type="application/json"
    )

    assert response.status_code == 201
    response_data = response.get_json()

    # 1. O endpoint POST /usuarios não deve retornar senha nem senha_hash.
    assert "senha" not in response_data
    assert "senha_hash" not in response_data

    # 2. A senha deve ser armazenada usando generate_password_hash.
    with client.application.app_context():
        from infrastructure.database.models.usuario_model import UsuarioModel
        from werkzeug.security import check_password_hash

        db_user = db.session.query(UsuarioModel).filter_by(email="seguro_http@example.com").first()
        assert db_user is not None
        assert db_user.senha_hash != payload["senha"]
        assert check_password_hash(db_user.senha_hash, payload["senha"])


def test_calculadora_competencias_medias():
    calculadora = CalculadoraCompetencias()

    comp_tecnica = Competencia(
        id=1,
        nome="Python",
        tipo="TECNICA",  # testa string maiúscula
        peso=Decimal("1.00")
    )
    comp_comportamental = Competencia(
        id=2,
        nome="Comunicação",
        tipo=TipoCompetencia.COMPORTAMENTAL,  # testa Enum
        peso=Decimal("1.00")
    )
    comp_lideranca = Competencia(
        id=3,
        nome="Gestão",
        tipo="lideranca",  # testa string minúscula (normalização)
        peso=Decimal("1.00")
    )

    competencias = {
        1: comp_tecnica,
        2: comp_comportamental,
        3: comp_lideranca
    }

    avaliacao = Avaliacao(
        colaborador_id=1,
        avaliador_id=2,
        tipo=None,
        observacao_geral="Avaliação de Teste",
        itens=[
            ItemAvaliacao(id=1, competencia_id=1, nota=5, comentario="Nota 5 em técnica"),
            ItemAvaliacao(id=2, competencia_id=2, nota=3, comentario="Nota 3 em comportamental"),
            ItemAvaliacao(id=3, competencia_id=3, nota=4, comentario="Nota 4 em liderança"),
        ]
    )

    resultado = calculadora.calcular(avaliacao, competencias)

    # 3. O cálculo de competências com notas 5, 3 e 4 retorna médias 5.0, 3.0 e 4.0
    assert resultado.media_tecnica == 5.0
    assert resultado.media_comportamental == 3.0
    assert resultado.media_lideranca == 4.0
    assert resultado.media_geral == 4.0
