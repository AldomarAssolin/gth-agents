from infrastructure.database.models.perfil_talento_model import PerfilTalentoModel
from domain.entities.perfil_talento import PerfilTalento
from domain.enums.classificacao_talento import ClassificacaoTalento


class PerfilTalentoMapper:
    @staticmethod
    def to_domain(model: PerfilTalentoModel | None) -> PerfilTalento | None:
        if model is None:
            return None
        return PerfilTalento(
            id=model.id,
            colaborador_id=model.colaborador_id,
            classificacao=ClassificacaoTalento(model.classificacao),
            resumo=model.resumo,
            nivel_tecnico=model.nivel_tecnico,
            nivel_comportamental=model.nivel_comportamental,
            potencial_lideranca=model.potencial_lideranca,
            pontos_fortes=model.pontos_fortes or [],
            pontos_melhoria=model.pontos_melhoria or [],
            recomendacoes=model.recomendacoes or [],
            origem=model.origem,
            criado_em=model.criado_em,
        )

    @staticmethod
    def to_model(entity: PerfilTalento) -> PerfilTalentoModel:
        return PerfilTalentoModel(
            id=entity.id,
            colaborador_id=entity.colaborador_id,
            classificacao=entity.classificacao.value,
            resumo=entity.resumo,
            nivel_tecnico=entity.nivel_tecnico,
            nivel_comportamental=entity.nivel_comportamental,
            potencial_lideranca=entity.potencial_lideranca,
            pontos_fortes=entity.pontos_fortes,
            pontos_melhoria=entity.pontos_melhoria,
            recomendacoes=entity.recomendacoes,
            origem=entity.origem,
        )
