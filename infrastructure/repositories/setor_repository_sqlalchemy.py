from sqlalchemy import select
from sqlalchemy.orm import Session

from application.ports.setor_repository import SetorRepository
from domain.entities.setor import Setor
from infrastructure.database.models.setor_model import SetorModel
from infrastructure.mappers.setor_mapper import SetorMapper


class SetorRepositorySQLAlchemy(SetorRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, setor_id: int) -> Setor | None:
        return SetorMapper.to_domain(self.session.get(SetorModel, setor_id))

    def list(self) -> list[Setor]:
        models = self.session.execute(select(SetorModel).order_by(SetorModel.id.asc())).scalars().all()
        return [SetorMapper.to_domain(model) for model in models]

    def get_by_nome(self, nome: str) -> Setor | None:
        model = self.session.execute(select(SetorModel).filter_by(nome=nome)).scalar_one_or_none()
        return SetorMapper.to_domain(model)

    def add(self, setor: Setor) -> Setor:
        model = SetorMapper.to_model(setor)
        self.session.add(model)
        self.session.flush()
        return SetorMapper.to_domain(model)

    def save(self, setor: Setor) -> None:
        model = self.session.get(SetorModel, setor.id)
        if model:
            model.nome = setor.nome
            model.descricao = setor.descricao
            model.ativo = setor.ativo
            self.session.flush()
