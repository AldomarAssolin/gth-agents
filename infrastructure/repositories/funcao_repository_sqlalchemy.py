from sqlalchemy import select
from sqlalchemy.orm import Session

from application.ports.funcao_repository import FuncaoRepository
from domain.entities.funcao import Funcao
from infrastructure.database.models.funcao_model import FuncaoModel
from infrastructure.mappers.funcao_mapper import FuncaoMapper


class FuncaoRepositorySQLAlchemy(FuncaoRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, funcao_id: int) -> Funcao | None:
        return FuncaoMapper.to_domain(self.session.get(FuncaoModel, funcao_id))

    def list(self) -> list[Funcao]:
        models = self.session.execute(select(FuncaoModel).order_by(FuncaoModel.id.asc())).scalars().all()
        return [FuncaoMapper.to_domain(model) for model in models]

    def get_by_nome(self, nome: str) -> Funcao | None:
        model = self.session.execute(select(FuncaoModel).filter_by(nome=nome)).scalar_one_or_none()
        return FuncaoMapper.to_domain(model)

    def add(self, funcao: Funcao) -> Funcao:
        model = FuncaoMapper.to_model(funcao)
        self.session.add(model)
        self.session.flush()
        return FuncaoMapper.to_domain(model)

    def save(self, funcao: Funcao) -> None:
        model = self.session.get(FuncaoModel, funcao.id)
        if model:
            model.nome = funcao.nome
            model.descricao = funcao.descricao
            model.ativo = funcao.ativo
            self.session.flush()
