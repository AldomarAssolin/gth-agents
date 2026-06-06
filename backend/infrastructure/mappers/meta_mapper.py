from infrastructure.database.models.meta_model import MetaModel
from domain.entities.meta import Meta
from domain.enums.prioridade_meta import PrioridadeMeta
from domain.enums.status_meta import StatusMeta


class MetaMapper:
    @staticmethod
    def to_domain(model: MetaModel | None) -> Meta | None:
        if model is None:
            return None
        return Meta(
            id=model.id,
            colaborador_id=model.colaborador_id,
            criado_por_id=model.criado_por_id,
            titulo=model.titulo,
            descricao=model.descricao,
            indicador=model.indicador,
            prazo=model.prazo,
            prioridade=PrioridadeMeta(model.prioridade),
            status=StatusMeta(model.status),
            origem=model.origem,
            criado_em=model.criado_em,
            atualizado_em=model.atualizado_em,
        )

    @staticmethod
    def to_model(entity: Meta) -> MetaModel:
        return MetaModel(
            id=entity.id,
            colaborador_id=entity.colaborador_id,
            criado_por_id=entity.criado_por_id,
            titulo=entity.titulo,
            descricao=entity.descricao,
            indicador=entity.indicador,
            prazo=entity.prazo,
            prioridade=entity.prioridade.value,
            status=entity.status.value,
            origem=entity.origem,
        )
