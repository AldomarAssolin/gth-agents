from dataclasses import dataclass


@dataclass(slots=True)
class RegistrarFeedbackDTO:
    colaborador_id: int
    autor_id: int
    ponto_positivo: str
    acao_recomendada: str
    contexto: str | None = None
    ponto_melhoria: str | None = None
