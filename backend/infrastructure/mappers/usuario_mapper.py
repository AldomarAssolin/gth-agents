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
            colaborador_id=model.colaborador_id,
            setor_id=model.setor_id,
            criado_em=model.criado_em,
        )

    @staticmethod
    def to_model(entity: Usuario) -> UsuarioModel:
        return UsuarioModel(
            id=entity.id,
            nome=entity.nome,
            email=entity.email,
            senha_hash=entity.senha_hash,
            perfil=entity.perfil.value if hasattr(entity.perfil, "value") else str(entity.perfil),
            ativo=entity.ativo,
            colaborador_id=entity.colaborador_id,
            setor_id=entity.setor_id,
        )

