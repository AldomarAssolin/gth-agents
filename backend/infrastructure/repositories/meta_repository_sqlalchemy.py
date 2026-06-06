from sqlalchemy import select
from sqlalchemy.orm import Session

from application.ports.meta_repository import MetaRepository
from domain.entities.meta import Meta
from infrastructure.database.models.meta_model import MetaModel
from infrastructure.mappers.meta_mapper import MetaMapper


class MetaRepositorySQLAlchemy(MetaRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, meta: Meta) -> Meta:
        model = MetaMapper.to_model(meta)
        self.session.add(model)
        self.session.flush()
        return MetaMapper.to_domain(model)

    def list_by_colaborador(self, colaborador_id: int) -> list[Meta]:
        models = self.session.execute(
            select(MetaModel)
            .filter_by(colaborador_id=colaborador_id)
            .order_by(MetaModel.criado_em.asc())
        ).scalars().all()
        return [MetaMapper.to_domain(model) for model in models]
