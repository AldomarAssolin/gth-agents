from infrastructure.database.models.funcao_model import FuncaoModel
from domain.entities.funcao import Funcao


class FuncaoMapper:
    @staticmethod
    def to_domain(model: FuncaoModel | None) -> Funcao | None:
        if model is None:
            return None
        return Funcao(
            id=model.id,
            nome=model.nome,
            descricao=model.descricao,
            ativo=model.ativo,
            criado_em=model.criado_em,
        )

    @staticmethod
    def to_model(entity: Funcao) -> FuncaoModel:
        return FuncaoModel(
            id=entity.id,
            nome=entity.nome,
            descricao=entity.descricao,
            ativo=entity.ativo,
        )
