from sqlalchemy import select
from sqlalchemy.orm import Session
from application.ports.acao_pdi_repository import AcaoPDIRepository
from domain.entities.acao_pdi import AcaoPDI
from infrastructure.database.models.acao_pdi_model import AcaoPDIModel
from infrastructure.mappers.pdi_mapper import AcaoPDIMapper


class AcaoPDIRepositorySQLAlchemy(AcaoPDIRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, acao: AcaoPDI) -> AcaoPDI:
        model = AcaoPDIMapper.to_model(acao)
        self.session.add(model)
        self.session.flush()
        return AcaoPDIMapper.to_domain(model)

    def save(self, acao: AcaoPDI) -> None:
        model = AcaoPDIMapper.to_model(acao)
        self.session.merge(model)
        self.session.flush()

    def get_by_id(self, acao_id: int) -> AcaoPDI | None:
        model = self.session.query(AcaoPDIModel).filter_by(id=acao_id).first()
        if not model:
            return None
        return AcaoPDIMapper.to_domain(model)

    def list_by_pdi_id(self, pdi_id: int) -> list[AcaoPDI]:
        models = self.session.execute(
            select(AcaoPDIModel)
            .filter_by(pdi_id=pdi_id)
            .order_by(AcaoPDIModel.criado_em.asc())
        ).scalars().all()
        return [AcaoPDIMapper.to_domain(model) for model in models]
