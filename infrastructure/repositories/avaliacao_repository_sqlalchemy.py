from sqlalchemy.orm import Session

from application.ports.avaliacao_repository import AvaliacaoRepository
from domain.entities.avaliacao import Avaliacao
from infrastructure.database.models.avaliacao_model import AvaliacaoModel
from infrastructure.mappers.avaliacao_mapper import AvaliacaoMapper


class AvaliacaoRepositorySQLAlchemy(AvaliacaoRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, avaliacao: Avaliacao) -> Avaliacao:
        model = AvaliacaoMapper.to_model(avaliacao)
        self.session.add(model)
        self.session.flush()
        return AvaliacaoMapper.to_domain(model)

    def get_by_id(self, avaliacao_id: int) -> Avaliacao | None:
        return AvaliacaoMapper.to_domain(self.session.get(AvaliacaoModel, avaliacao_id))
