from dataclasses import dataclass


@dataclass(slots=True)
class RegistrarFeedbackDTO:
    colaborador_id: int
    autor_id: int
    contexto: str
    ponto_positivo: str
    ponto_melhoria: str
    acao_recomendada: str


@dataclass(slots=True)
class EstruturarFeedbackDTO:
    observacao: str
