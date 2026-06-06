from infrastructure.database.models.execucao_agente_model import ExecucaoAgenteModel
from domain.entities.execucao_agente import ExecucaoAgente


class ExecucaoAgenteMapper:
    @staticmethod
    def to_domain(model: ExecucaoAgenteModel | None) -> ExecucaoAgente | None:
        if model is None:
            return None
        return ExecucaoAgente(
            id=model.id,
            agente_nome=model.agente_nome,
            entidade_tipo=model.entidade_tipo,
            entidade_id=model.entidade_id,
            entrada=model.entrada,
            saida=model.saida,
            status=model.status,
            erro=model.erro,
            criado_em=model.criado_em,
        )

    @staticmethod
    def to_model(entity: ExecucaoAgente) -> ExecucaoAgenteModel:
        return ExecucaoAgenteModel(
            id=entity.id,
            agente_nome=entity.agente_nome,
            entidade_tipo=entity.entidade_tipo,
            entidade_id=entity.entidade_id,
            entrada=entity.entrada,
            saida=entity.saida,
            status=entity.status,
            erro=entity.erro,
        )
