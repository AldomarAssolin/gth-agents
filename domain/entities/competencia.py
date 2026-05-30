from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from domain.enums.tipo_competencia import TipoCompetencia


@dataclass(slots=True)
class Competencia:
    nome: str
    tipo: TipoCompetencia
    descricao: str | None = None
    peso: Decimal = Decimal("1.00")
    ativo: bool = True
    id: int | None = None
    criado_em: datetime | None = None

    def ativar(self) -> None:
        self.ativo = True

    def desativar(self) -> None:
        self.ativo = False

    def esta_ativa(self) -> bool:
        return self.ativo

    def eh_tecnica(self) -> bool:
        return self.tipo == TipoCompetencia.TECNICA

    def eh_comportamental(self) -> bool:
        return self.tipo == TipoCompetencia.COMPORTAMENTAL

    def eh_lideranca(self) -> bool:
        return self.tipo == TipoCompetencia.LIDERANCA
