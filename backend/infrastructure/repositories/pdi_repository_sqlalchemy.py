from sqlalchemy import select
from sqlalchemy.orm import Session
from application.ports.pdi_repository import PDIRepository
from domain.entities.pdi import PDI
from infrastructure.database.models.pdi_model import PDIModel
from infrastructure.mappers.pdi_mapper import PDIMapper


class PDIRepositorySQLAlchemy(PDIRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, pdi: PDI) -> PDI:
        model = PDIMapper.to_model(pdi)
        self.session.add(model)
        self.session.flush()
        return PDIMapper.to_domain(model)

    def save(self, pdi: PDI) -> None:
        model = PDIMapper.to_model(pdi)
        self.session.merge(model)
        self.session.flush()

    def get_by_id(self, pdi_id: int) -> PDI | None:
        # Avoid using session.get if it caches relationship states in memory without refreshing.
        # Let's perform a fresh query with joinedload or just normal execution.
        model = self.session.query(PDIModel).filter_by(id=pdi_id).first()
        if not model:
            return None
        return PDIMapper.to_domain(model)

    def list_all(self) -> list[PDI]:
        models = self.session.execute(
            select(PDIModel).order_by(PDIModel.criado_em.desc())
        ).scalars().all()
        return [PDIMapper.to_domain(model) for model in models]

    def list_by_colaborador_id(self, colaborador_id: int) -> list[PDI]:
        models = self.session.execute(
            select(PDIModel)
            .filter_by(colaborador_id=colaborador_id)
            .order_by(PDIModel.criado_em.desc())
        ).scalars().all()
        return [PDIMapper.to_domain(model) for model in models]
