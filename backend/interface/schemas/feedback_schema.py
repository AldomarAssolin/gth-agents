from application.dtos.feedback_dto import RegistrarFeedbackDTO, EstruturarFeedbackDTO


def parse_registrar_feedback(data: dict) -> RegistrarFeedbackDTO:
    return RegistrarFeedbackDTO(
        colaborador_id=data.get("colaborador_id"),
        autor_id=data.get("autor_id"),
        contexto=data.get("contexto"),
        ponto_positivo=data.get("ponto_positivo"),
        ponto_melhoria=data.get("ponto_melhoria"),
        acao_recomendada=data.get("acao_recomendada"),
    )


def parse_estruturar_feedback(data: dict) -> EstruturarFeedbackDTO:
    return EstruturarFeedbackDTO(
        observacao=data.get("observacao"),
    )
