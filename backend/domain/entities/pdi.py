from dataclasses import dataclass, field
from datetime import date, datetime
from domain.enums.pdi_enums import StatusPDI, OrigemPDI, StatusAcaoPDI
from domain.entities.acao_pdi import AcaoPDI


@dataclass(slots=True)
class PDI:
    colaborador_id: int
    titulo: str
    descricao: str
    criado_por_id: int
    origem: OrigemPDI = OrigemPDI.MANUAL
    status: StatusPDI = StatusPDI.RASCUNHO
    data_inicio: date | None = None
    data_fim: date | None = None
    acoes: list[AcaoPDI] = field(default_factory=list)
    id: int | None = None
    criado_em: datetime | None = None
    atualizado_em: datetime | None = None

    def concluir(self) -> None:
        if self.status == StatusPDI.CANCELADO:
            raise ValueError("PDI cancelado nao pode ser concluido.")
        for acao in self.acoes:
            if acao.status not in (StatusAcaoPDI.CONCLUIDA, StatusAcaoPDI.CANCELADA):
                raise ValueError("PDI possui acoes pendentes.")
        self.status = StatusPDI.CONCLUIDO

    def cancelar(self) -> None:
        if self.status == StatusPDI.CONCLUIDO:
            raise ValueError("PDI concluido nao pode ser cancelado.")
        self.status = StatusPDI.CANCELADO

    def ativar(self) -> None:
        if self.status == StatusPDI.CONCLUIDO:
            raise ValueError("PDI concluido nao pode ser ativado.")
        if self.status == StatusPDI.CANCELADO:
            raise ValueError("PDI cancelado nao pode ser ativado.")
        self.status = StatusPDI.ATIVO

    def validar(self) -> None:
        if not self.titulo:
            raise ValueError("Titulo do PDI e obrigatorio.")
        if not self.descricao:
            raise ValueError("Descricao do PDI e obrigatorio.")
        if not self.colaborador_id:
            raise ValueError("Colaborador do PDI e obrigatorio.")
        if not self.criado_por_id:
            raise ValueError("Criador do PDI e obrigatorio.")
