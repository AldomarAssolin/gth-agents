from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Feedback:
    colaborador_id: int
    autor_id: int
    ponto_positivo: str
    acao_recomendada: str
    contexto: str | None = None
    ponto_melhoria: str | None = None
    origem: str = "MANUAL"
    id: int | None = None
    data_feedback: datetime | None = None
    criado_em: datetime | None = None

    def validar(self) -> None:
        if self.colaborador_id is None:
            raise ValueError("feedback must be linked to a colaborador")
        if self.autor_id is None:
            raise ValueError("feedback must have an autor")
        if not self.ponto_positivo:
            raise ValueError("ponto_positivo is required")
        if not self.acao_recomendada:
            raise ValueError("acao_recomendada is required")

    def possui_ponto_melhoria(self) -> bool:
        return bool(self.ponto_melhoria)
