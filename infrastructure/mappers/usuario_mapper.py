from infrastructure.database.models.usuario_model import UsuarioModel
from domain.entities.usuario import Usuario
from domain.enums.perfil_usuario import PerfilUsuario


class UsuarioMapper:
    @staticmethod
    def to_domain(model: UsuarioModel | None) -> Usuario | None:
        if model is None:
            return None
        return Usuario(
            id=model.id,
            nome=model.nome,
            email=model.email,
            senha_hash=model.senha_hash,
            perfil=PerfilUsuario(model.perfil),
            ativo=model.ativo,
            criado_em=model.criado_em,
        )

    @staticmethod
    def to_model(entity: Usuario) -> UsuarioModel:
        return UsuarioModel(
            id=entity.id,
            nome=entity.nome,
            email=entity.email,
            senha_hash=entity.senha_hash,
            perfil=entity.perfil.value,
            ativo=entity.ativo,
        )
