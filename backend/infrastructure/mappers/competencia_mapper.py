from infrastructure.database.models.competencia_model import CompetenciaModel
from domain.entities.competencia import Competencia
from domain.enums.tipo_competencia import TipoCompetencia


class CompetenciaMapper:
    @staticmethod
    def to_domain(model: CompetenciaModel | None) -> Competencia | None:
        if model is None:
            return None
        return Competencia(
            id=model.id,
            nome=model.nome,
            tipo=TipoCompetencia(model.tipo),
            descricao=model.descricao,
            peso=model.peso,
            ativo=model.ativo,
            criado_em=model.criado_em,
        )

    @staticmethod
    def to_model(entity: Competencia) -> CompetenciaModel:
        return CompetenciaModel(
            id=entity.id,
            nome=entity.nome,
            tipo=entity.tipo.value,
            descricao=entity.descricao,
            peso=entity.peso,
            ativo=entity.ativo,
        )
