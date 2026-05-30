from sqlalchemy import select
from sqlalchemy.orm import Session

from application.ports.usuario_repository import UsuarioRepository
from domain.entities.usuario import Usuario
from infrastructure.database.models.usuario_model import UsuarioModel
from infrastructure.mappers.usuario_mapper import UsuarioMapper


class UsuarioRepositorySQLAlchemy(UsuarioRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, usuario_id: int) -> Usuario | None:
        return UsuarioMapper.to_domain(self.session.get(UsuarioModel, usuario_id))

    def list(self) -> list[Usuario]:
        models = self.session.execute(select(UsuarioModel).order_by(UsuarioModel.id.asc())).scalars().all()
        return [UsuarioMapper.to_domain(model) for model in models]

    def get_by_email(self, email: str) -> Usuario | None:
        model = self.session.execute(select(UsuarioModel).filter_by(email=email)).scalar_one_or_none()
        return UsuarioMapper.to_domain(model)

    def add(self, usuario: Usuario) -> Usuario:
        model = UsuarioMapper.to_model(usuario)
        self.session.add(model)
        self.session.flush()
        return UsuarioMapper.to_domain(model)
