from infrastructure.database.models.feedback_model import FeedbackModel
from domain.entities.feedback import Feedback


class FeedbackMapper:
    @staticmethod
    def to_domain(model: FeedbackModel | None) -> Feedback | None:
        if model is None:
            return None
        return Feedback(
            id=model.id,
            colaborador_id=model.colaborador_id,
            autor_id=model.autor_id,
            contexto=model.contexto,
            ponto_positivo=model.ponto_positivo,
            ponto_melhoria=model.ponto_melhoria,
            acao_recomendada=model.acao_recomendada,
            origem=model.origem,
            data_feedback=model.data_feedback,
            criado_em=model.criado_em,
        )

    @staticmethod
    def to_model(entity: Feedback) -> FeedbackModel:
        return FeedbackModel(
            id=entity.id,
            colaborador_id=entity.colaborador_id,
            autor_id=entity.autor_id,
            contexto=entity.contexto,
            ponto_positivo=entity.ponto_positivo,
            ponto_melhoria=entity.ponto_melhoria,
            acao_recomendada=entity.acao_recomendada,
            origem=entity.origem,
        )
