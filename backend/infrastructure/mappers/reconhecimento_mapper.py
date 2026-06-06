from domain.entities.reconhecimento import Reconhecimento
from domain.enums.tipo_reconhecimento import TipoReconhecimento
from infrastructure.database.models.reconhecimento_model import ReconhecimentoModel


class ReconhecimentoMapper:
    @staticmethod
    def to_domain(model: ReconhecimentoModel | None) -> Reconhecimento | None:
        if model is None:
            return None
        return Reconhecimento(
            id=model.id,
            colaborador_id=model.colaborador_id,
            tipo=TipoReconhecimento(model.tipo),
            descricao=model.descricao,
            evidencia=model.evidencia,
            registrado_por_id=model.registrado_por_id,
            data_reconhecimento=model.data_reconhecimento,
            ativo=model.ativo,
            criado_em=model.criado_em,
            cancelado_em=model.cancelado_em,
            cancelado_por_id=model.cancelado_por_id,
            motivo_cancelamento=model.motivo_cancelamento,
        )

    @staticmethod
    def to_model(entity: Reconhecimento) -> ReconhecimentoModel:
        return ReconhecimentoModel(
            id=entity.id,
            colaborador_id=entity.colaborador_id,
            tipo=entity.tipo.value if hasattr(entity.tipo, "value") else entity.tipo,
            descricao=entity.descricao,
            evidencia=entity.evidencia,
            registrado_por_id=entity.registrado_por_id,
            data_reconhecimento=entity.data_reconhecimento,
            ativo=entity.ativo,
            criado_em=entity.criado_em,
            cancelado_em=entity.cancelado_em,
            cancelado_por_id=entity.cancelado_por_id,
            motivo_cancelamento=entity.motivo_cancelamento,
        )
