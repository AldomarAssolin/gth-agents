from infrastructure.database.models.setor_model import SetorModel
from domain.entities.setor import Setor


class SetorMapper:
    @staticmethod
    def to_domain(model: SetorModel | None) -> Setor | None:
        if model is None:
            return None
        return Setor(
            id=model.id,
            nome=model.nome,
            descricao=model.descricao,
            ativo=model.ativo,
            criado_em=model.criado_em,
        )

    @staticmethod
    def to_model(entity: Setor) -> SetorModel:
        return SetorModel(
            id=entity.id,
            nome=entity.nome,
            descricao=entity.descricao,
            ativo=entity.ativo,
        )
