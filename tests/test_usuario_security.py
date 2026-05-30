from application.dtos.cadastro_dto import CriarUsuarioDTO
from application.use_cases.cadastros_basicos_uc import CriarUsuarioUC
from domain.enums.perfil_usuario import PerfilUsuario
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
