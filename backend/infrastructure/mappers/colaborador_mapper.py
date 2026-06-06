from infrastructure.database.models.colaborador_model import ColaboradorModel
from domain.entities.colaborador import Colaborador
from domain.enums.status_colaborador import StatusColaborador


class ColaboradorMapper:
    @staticmethod
    def to_domain(model: ColaboradorModel | None) -> Colaborador | None:
        if model is None:
            return None
        return Colaborador(
            id=model.id,
            nome=model.nome,
            matricula=model.matricula,
            email=model.email,
            data_admissao=model.data_admissao,
            status=StatusColaborador(model.status),
            setor_id=model.setor_id,
            funcao_id=model.funcao_id,
            criado_em=model.criado_em,
            atualizado_em=model.atualizado_em,
        )

    @staticmethod
    def to_model(entity: Colaborador) -> ColaboradorModel:
        return ColaboradorModel(
            id=entity.id,
            nome=entity.nome,
            matricula=entity.matricula,
            email=entity.email,
            data_admissao=entity.data_admissao,
            status=entity.status.value,
            setor_id=entity.setor_id,
            funcao_id=entity.funcao_id,
        )
