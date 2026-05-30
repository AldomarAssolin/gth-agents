from dataclasses import dataclass
from datetime import date


@dataclass(slots=True)
class CriarColaboradorDTO:
    nome: str
    matricula: str
    email: str | None
    data_admissao: date | None
    setor_id: int
    funcao_id: int
