from dataclasses import dataclass
from datetime import datetime, timezone
from domain.enums.tipo_reconhecimento import TipoReconhecimento


@dataclass(slots=True)
class Reconhecimento:
    colaborador_id: int
    tipo: TipoReconhecimento
    descricao: str
    evidencia: str
    registrado_por_id: int
    data_reconhecimento: datetime | None = None
    ativo: bool = True
    criado_em: datetime | None = None
    cancelado_em: datetime | None = None
    cancelado_por_id: int | None = None
    motivo_cancelamento: str | None = None
    id: int | None = None

    def validar(self) -> None:
        if not self.colaborador_id:
            raise ValueError("Reconhecimento deve estar vinculado a um colaborador.")

        if not self.registrado_por_id:
            raise ValueError("Reconhecimento deve possuir usuario registrador.")

        if not self.descricao or not self.descricao.strip():
            raise ValueError("Descricao do reconhecimento e obrigatoria.")

        if not self.evidencia or not self.evidencia.strip():
            raise ValueError("Evidencia do reconhecimento e obrigatoria.")

    def cancelar(self, cancelado_por_id: int, motivo: str) -> None:
        if not self.ativo:
            raise ValueError("Reconhecimento ja esta cancelado.")

        if not motivo or not motivo.strip():
            raise ValueError("Motivo do cancelamento e obrigatorio.")

        self.ativo = False
        self.cancelado_por_id = cancelado_por_id
        self.motivo_cancelamento = motivo
        self.cancelado_em = datetime.now(timezone.utc)
