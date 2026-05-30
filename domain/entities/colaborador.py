from dataclasses import dataclass
from datetime import date, datetime

from domain.enums.status_colaborador import StatusColaborador


@dataclass(slots=True)
class Colaborador:
    nome: str
    matricula: str
    setor_id: int
    funcao_id: int
    email: str | None = None
    data_admissao: date | None = None
    status: StatusColaborador = StatusColaborador.ATIVO
    id: int | None = None
    criado_em: datetime | None = None
    atualizado_em: datetime | None = None

    def esta_ativo(self) -> bool:
        return self.status == StatusColaborador.ATIVO

    def ativar(self) -> None:
        self.status = StatusColaborador.ATIVO

    def inativar(self) -> None:
        self.status = StatusColaborador.INATIVO

    def afastar(self) -> None:
        self.status = StatusColaborador.AFASTADO

    def desligar(self) -> None:
        self.status = StatusColaborador.DESLIGADO
