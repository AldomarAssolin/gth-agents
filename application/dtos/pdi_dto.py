from dataclasses import dataclass
from datetime import date


@dataclass(slots=True)
class AcaoPDIInputDTO:
    tipo: str
    descricao: str
    prazo: date


@dataclass(slots=True)
class CriarPDIDTO:
    colaborador_id: int
    titulo: str
    descricao: str
    criado_por_id: int
    origem: str = "MANUAL"
    status: str = "ATIVO"
    data_inicio: date | None = None
    data_fim: date | None = None
    acoes: list[AcaoPDIInputDTO] | None = None



@dataclass(slots=True)
class AtualizarPDIDTO:
    id: int
    titulo: str
    descricao: str
    data_inicio: date | None = None
    data_fim: date | None = None


@dataclass(slots=True)
class CriarAcaoPDIDTO:
    pdi_id: int
    tipo: str
    descricao: str
    prazo: date


@dataclass(slots=True)
class AtualizarAcaoPDIDTO:
    id: int
    tipo: str
    descricao: str
    prazo: date
