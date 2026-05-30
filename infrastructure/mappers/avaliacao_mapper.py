from infrastructure.database.models.avaliacao_model import AvaliacaoModel, ItemAvaliacaoModel
from domain.entities.avaliacao import Avaliacao
from domain.entities.item_avaliacao import ItemAvaliacao
from domain.enums.tipo_avaliacao import TipoAvaliacao


class AvaliacaoMapper:
    @staticmethod
    def to_domain(model: AvaliacaoModel | None) -> Avaliacao | None:
        if model is None:
            return None
        return Avaliacao(
            id=model.id,
            colaborador_id=model.colaborador_id,
            avaliador_id=model.avaliador_id,
            tipo=TipoAvaliacao(model.tipo),
            observacao_geral=model.observacao_geral,
            status=model.status,
            data_avaliacao=model.data_avaliacao,
            criado_em=model.criado_em,
            itens=[
                ItemAvaliacao(
                    id=item.id,
                    competencia_id=item.competencia_id,
                    nota=item.nota,
                    comentario=item.comentario,
                )
                for item in model.itens
            ],
        )

    @staticmethod
    def to_model(entity: Avaliacao) -> AvaliacaoModel:
        return AvaliacaoModel(
            id=entity.id,
            colaborador_id=entity.colaborador_id,
            avaliador_id=entity.avaliador_id,
            tipo=entity.tipo.value,
            observacao_geral=entity.observacao_geral,
            status=entity.status,
            itens=[
                ItemAvaliacaoModel(
                    competencia_id=item.competencia_id,
                    nota=item.nota,
                    comentario=item.comentario,
                )
                for item in entity.itens
            ],
        )
