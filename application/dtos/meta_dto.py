from dataclasses import dataclass
from datetime import date

from domain.enums.prioridade_meta import PrioridadeMeta


@dataclass(slots=True)
class CriarMetaDTO:
    colaborador_id: int
    criado_por_id: int
    titulo: str
    descricao: str
    prazo: date
    indicador: str | None = None
    prioridade: PrioridadeMeta = PrioridadeMeta.MEDIA
