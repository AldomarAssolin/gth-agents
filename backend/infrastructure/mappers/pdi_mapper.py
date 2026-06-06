from domain.entities.pdi import PDI
from domain.entities.acao_pdi import AcaoPDI
from domain.enums.pdi_enums import StatusPDI, OrigemPDI, TipoAcaoPDI, StatusAcaoPDI
from infrastructure.database.models.pdi_model import PDIModel
from infrastructure.database.models.acao_pdi_model import AcaoPDIModel


class AcaoPDIMapper:
    @staticmethod
    def to_domain(model: AcaoPDIModel | None) -> AcaoPDI | None:
        if model is None:
            return None
        return AcaoPDI(
            id=model.id,
            pdi_id=model.pdi_id,
            tipo=TipoAcaoPDI(model.tipo),
            descricao=model.descricao,
            prazo=model.prazo,
            status=StatusAcaoPDI(model.status),
            criado_em=model.criado_em,
            atualizado_em=model.atualizado_em,
        )

    @staticmethod
    def to_model(entity: AcaoPDI) -> AcaoPDIModel:
        return AcaoPDIModel(
            id=entity.id,
            pdi_id=entity.pdi_id,
            tipo=entity.tipo.value if hasattr(entity.tipo, "value") else entity.tipo,
            descricao=entity.descricao,
            prazo=entity.prazo,
            status=entity.status.value if hasattr(entity.status, "value") else entity.status,
        )


class PDIMapper:
    @staticmethod
    def to_domain(model: PDIModel | None) -> PDI | None:
        if model is None:
            return None
        acoes_domain = []
        if model.acoes:
            acoes_domain = [AcaoPDIMapper.to_domain(acao) for acao in model.acoes]
        return PDI(
            id=model.id,
            colaborador_id=model.colaborador_id,
            titulo=model.titulo,
            descricao=model.descricao,
            origem=OrigemPDI(model.origem),
            status=StatusPDI(model.status),
            data_inicio=model.data_inicio,
            data_fim=model.data_fim,
            criado_por_id=model.criado_por_id,
            acoes=acoes_domain,
            criado_em=model.criado_em,
            atualizado_em=model.atualizado_em,
        )

    @staticmethod
    def to_model(entity: PDI) -> PDIModel:
        acoes_models = []
        if entity.acoes:
            acoes_models = [AcaoPDIMapper.to_model(acao) for acao in entity.acoes]
        return PDIModel(
            id=entity.id,
            colaborador_id=entity.colaborador_id,
            titulo=entity.titulo,
            descricao=entity.descricao,
            origem=entity.origem.value if hasattr(entity.origem, "value") else entity.origem,
            status=entity.status.value if hasattr(entity.status, "value") else entity.status,
            data_inicio=entity.data_inicio,
            data_fim=entity.data_fim,
            criado_por_id=entity.criado_por_id,
            acoes=acoes_models,
        )
