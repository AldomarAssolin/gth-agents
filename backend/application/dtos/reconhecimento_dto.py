from dataclasses import dataclass
from domain.enums.tipo_reconhecimento import TipoReconhecimento


@dataclass(slots=True)
class CriarReconhecimentoDTO:
    colaborador_id: int
    tipo: TipoReconhecimento
    descricao: str
    evidencia: str
    registrado_por_id: int


@dataclass(slots=True)
class CancelarReconhecimentoDTO:
    reconhecimento_id: int
    cancelado_por_id: int
    motivo_cancelamento: str
