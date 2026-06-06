from dataclasses import dataclass
from datetime import date, datetime
from domain.enums.pdi_enums import StatusAcaoPDI, TipoAcaoPDI


@dataclass(slots=True)
class AcaoPDI:
    tipo: TipoAcaoPDI
    descricao: str
    prazo: date
    pdi_id: int | None = None
    status: StatusAcaoPDI = StatusAcaoPDI.PENDENTE
    id: int | None = None
    criado_em: datetime | None = None
    atualizado_em: datetime | None = None

    def concluir(self) -> None:
        if self.status == StatusAcaoPDI.CANCELADA:
            raise ValueError("Acao cancelada nao pode ser concluida.")
        self.status = StatusAcaoPDI.CONCLUIDA

    def cancelar(self) -> None:
        self.status = StatusAcaoPDI.CANCELADA

    def iniciar(self) -> None:
        if self.status == StatusAcaoPDI.CANCELADA:
            raise ValueError("Acao cancelada nao pode ser iniciada.")
        if self.status == StatusAcaoPDI.CONCLUIDA:
            raise ValueError("Acao concluida nao pode ser iniciada.")
        self.status = StatusAcaoPDI.EM_ANDAMENTO
