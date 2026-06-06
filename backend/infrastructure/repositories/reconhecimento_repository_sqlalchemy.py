from sqlalchemy import select
from sqlalchemy.orm import Session
from application.ports.reconhecimento_repository import ReconhecimentoRepository
from domain.entities.reconhecimento import Reconhecimento
from infrastructure.database.models.reconhecimento_model import ReconhecimentoModel
from infrastructure.mappers.reconhecimento_mapper import ReconhecimentoMapper


class ReconhecimentoRepositorySQLAlchemy(ReconhecimentoRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, reconhecimento: Reconhecimento) -> Reconhecimento:
        model = ReconhecimentoMapper.to_model(reconhecimento)
        self.session.add(model)
        self.session.flush()
        return ReconhecimentoMapper.to_domain(model)

    def save(self, reconhecimento: Reconhecimento) -> Reconhecimento:
        model = ReconhecimentoMapper.to_model(reconhecimento)
        merged = self.session.merge(model)
        self.session.flush()
        return ReconhecimentoMapper.to_domain(merged)

    def get_by_id(self, reconhecimento_id: int) -> Reconhecimento | None:
        model = self.session.query(ReconhecimentoModel).filter_by(id=reconhecimento_id).first()
        if not model:
            return None
        return ReconhecimentoMapper.to_domain(model)

    def list_all(self) -> list[Reconhecimento]:
        stmt = select(ReconhecimentoModel).order_by(ReconhecimentoModel.id.desc())
        models = self.session.execute(stmt).scalars().all()
        return [ReconhecimentoMapper.to_domain(model) for model in models]

    def list_by_colaborador_id(self, colaborador_id: int) -> list[Reconhecimento]:
        stmt = (
            select(ReconhecimentoModel)
            .filter_by(colaborador_id=colaborador_id)
            .order_by(ReconhecimentoModel.id.desc())
        )
        models = self.session.execute(stmt).scalars().all()
        return [ReconhecimentoMapper.to_domain(model) for model in models]

    def list_by_colaboradores_ids(self, colaboradores_ids: list[int]) -> list[Reconhecimento]:
        if not colaboradores_ids:
            return []
        stmt = (
            select(ReconhecimentoModel)
            .where(ReconhecimentoModel.colaborador_id.in_(colaboradores_ids))
            .order_by(ReconhecimentoModel.id.desc())
        )
        models = self.session.execute(stmt).scalars().all()
        return [ReconhecimentoMapper.to_domain(model) for model in models]
