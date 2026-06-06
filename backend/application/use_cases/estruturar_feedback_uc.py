from application.dtos.feedback_dto import EstruturarFeedbackDTO
from application.errors import ValidationError
from application.services.agents import AgenteFeedback


class EstruturarFeedbackUC:
    def __init__(self):
        self.agente_feedback = AgenteFeedback()

    def execute(self, dto: EstruturarFeedbackDTO) -> dict:
        if not dto.observacao or not dto.observacao.strip():
            raise ValidationError("observacao is required")
        try:
            return self.agente_feedback.estruturar(dto.observacao)
        except ValueError as exc:
            raise ValidationError(str(exc)) from exc
