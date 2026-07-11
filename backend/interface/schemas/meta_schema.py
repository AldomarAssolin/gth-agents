from datetime import date

from application.dtos.meta_dto import CriarMetaDTO
from domain.enums.prioridade_meta import PrioridadeMeta


def parse_criar_meta(data: dict, criado_por_id: int) -> CriarMetaDTO:
    return CriarMetaDTO(
        colaborador_id=data.get("colaborador_id"),
        criado_por_id=criado_por_id,
        titulo=data.get("titulo"),
        descricao=data.get("descricao"),
        indicador=data.get("indicador"),
        prazo=date.fromisoformat(data["prazo"]) if data.get("prazo") else None,
        prioridade=PrioridadeMeta((data.get("prioridade") or PrioridadeMeta.MEDIA.value).upper()),
    )
