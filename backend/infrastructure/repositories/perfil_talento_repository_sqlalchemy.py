from sqlalchemy import select
from sqlalchemy.orm import Session

from application.ports.perfil_talento_repository import PerfilTalentoRepository
from domain.entities.perfil_talento import PerfilTalento
from infrastructure.database.models.perfil_talento_model import PerfilTalentoModel
from infrastructure.mappers.perfil_talento_mapper import PerfilTalentoMapper


class PerfilTalentoRepositorySQLAlchemy(PerfilTalentoRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, perfil_talento: PerfilTalento) -> PerfilTalento:
        model = PerfilTalentoMapper.to_model(perfil_talento)
        self.session.add(model)
        self.session.flush()
        return PerfilTalentoMapper.to_domain(model)

    def get_ultimo_by_colaborador_id(self, colaborador_id: int) -> PerfilTalento | None:
        model = self.session.execute(
            select(PerfilTalentoModel)
            .filter_by(colaborador_id=colaborador_id)
            .order_by(PerfilTalentoModel.criado_em.desc())
            .limit(1)
        ).scalar_one_or_none()
        return PerfilTalentoMapper.to_domain(model)
