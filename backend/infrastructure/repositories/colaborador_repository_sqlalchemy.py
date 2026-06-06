from typing import List
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

    def list(self) -> List[Colaborador]:
        models = self.session.execute(select(ColaboradorModel).order_by(ColaboradorModel.id.asc())).scalars().all()
        return [ColaboradorMapper.to_domain(model) for model in models]

    def list_by_setor_id(self, setor_id: int) -> List[Colaborador]:
        models = self.session.execute(
            select(ColaboradorModel)
            .filter_by(setor_id=setor_id)
            .order_by(ColaboradorModel.id.asc())
        ).scalars().all()
        return [ColaboradorMapper.to_domain(model) for model in models]


    def save(self, colaborador: Colaborador) -> None:

        model = self.session.get(ColaboradorModel, colaborador.id)
        if model:
            model.nome = colaborador.nome
            model.matricula = colaborador.matricula
            model.email = colaborador.email
            model.data_admissao = colaborador.data_admissao
            model.setor_id = colaborador.setor_id
            model.funcao_id = colaborador.funcao_id
            model.status = colaborador.status.value if hasattr(colaborador.status, "value") else colaborador.status
            self.session.flush()
