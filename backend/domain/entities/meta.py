from dataclasses import dataclass
from datetime import date, datetime

from domain.enums.status_meta import StatusMeta
from domain.enums.prioridade_meta import PrioridadeMeta


@dataclass(slots=True)
class Meta:
    colaborador_id: int
    criado_por_id: int
    titulo: str
    descricao: str
    prazo: date
    indicador: str | None = None
    prioridade: PrioridadeMeta = PrioridadeMeta.MEDIA
    status: StatusMeta = StatusMeta.PENDENTE
    origem: str = "MANUAL"
    id: int | None = None
    criado_em: datetime | None = None
    atualizado_em: datetime | None = None

    def iniciar(self) -> None:
        self.status = StatusMeta.EM_ANDAMENTO

    def concluir(self) -> None:
        self.status = StatusMeta.CONCLUIDA

    def atrasar(self) -> None:
        self.status = StatusMeta.ATRASADA

    def cancelar(self) -> None:
        self.status = StatusMeta.CANCELADA

    def esta_aberta(self) -> bool:
        return self.status in {StatusMeta.PENDENTE, StatusMeta.EM_ANDAMENTO, StatusMeta.ATRASADA}

    def eh_critica(self) -> bool:
        return self.prioridade == PrioridadeMeta.CRITICA
