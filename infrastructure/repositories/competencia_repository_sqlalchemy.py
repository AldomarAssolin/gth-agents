from sqlalchemy import select
from sqlalchemy.orm import Session

from application.ports.competencia_repository import CompetenciaRepository
from domain.entities.competencia import Competencia
from infrastructure.database.models.competencia_model import CompetenciaModel
from infrastructure.mappers.competencia_mapper import CompetenciaMapper


class CompetenciaRepositorySQLAlchemy(CompetenciaRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, competencia_id: int) -> Competencia | None:
        return CompetenciaMapper.to_domain(self.session.get(CompetenciaModel, competencia_id))

    def list(self) -> list[Competencia]:
        models = self.session.execute(select(CompetenciaModel).order_by(CompetenciaModel.id.asc())).scalars().all()
        return [CompetenciaMapper.to_domain(model) for model in models]

    def add(self, competencia: Competencia) -> Competencia:
        model = CompetenciaMapper.to_model(competencia)
        self.session.add(model)
        self.session.flush()
        return CompetenciaMapper.to_domain(model)
