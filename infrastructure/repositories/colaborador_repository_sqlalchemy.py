from sqlalchemy import select
from sqlalchemy.orm import Session

from application.ports.colaborador_repository import ColaboradorRepository
from domain.entities.colaborador import Colaborador
from infrastructure.database.models.colaborador_model import ColaboradorModel
from infrastructure.mappers.colaborador_mapper import ColaboradorMapper


class ColaboradorRepositorySQLAlchemy(ColaboradorRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, colaborador_id: int) -> Colaborador | None:
        return ColaboradorMapper.to_domain(self.session.get(ColaboradorModel, colaborador_id))

    def get_by_matricula(self, matricula: str) -> Colaborador | None:
        model = self.session.execute(select(ColaboradorModel).filter_by(matricula=matricula)).scalar_one_or_none()
        return ColaboradorMapper.to_domain(model)

    def add(self, colaborador: Colaborador) -> Colaborador:
        model = ColaboradorMapper.to_model(colaborador)
        self.session.add(model)
        self.session.flush()
        return ColaboradorMapper.to_domain(model)
