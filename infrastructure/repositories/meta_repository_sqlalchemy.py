from sqlalchemy.orm import Session

from application.ports.meta_repository import MetaRepository
from domain.entities.meta import Meta
from infrastructure.mappers.meta_mapper import MetaMapper


class MetaRepositorySQLAlchemy(MetaRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, meta: Meta) -> Meta:
        model = MetaMapper.to_model(meta)
        self.session.add(model)
        self.session.flush()
        return MetaMapper.to_domain(model)
