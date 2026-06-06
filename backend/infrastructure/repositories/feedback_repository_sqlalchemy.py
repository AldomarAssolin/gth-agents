from sqlalchemy import select
from sqlalchemy.orm import Session

from application.ports.feedback_repository import FeedbackRepository
from domain.entities.feedback import Feedback
from infrastructure.database.models.feedback_model import FeedbackModel
from infrastructure.mappers.feedback_mapper import FeedbackMapper


class FeedbackRepositorySQLAlchemy(FeedbackRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, feedback: Feedback) -> Feedback:
        model = FeedbackMapper.to_model(feedback)
        self.session.add(model)
        self.session.flush()
        return FeedbackMapper.to_domain(model)

    def list_by_colaborador(self, colaborador_id: int) -> list[Feedback]:
        models = self.session.execute(
            select(FeedbackModel)
            .filter_by(colaborador_id=colaborador_id)
            .order_by(FeedbackModel.criado_em.asc())
        ).scalars().all()
        return [FeedbackMapper.to_domain(model) for model in models]
