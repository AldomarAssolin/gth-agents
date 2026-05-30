from sqlalchemy.orm import Session

from application.ports.feedback_repository import FeedbackRepository
from domain.entities.feedback import Feedback
from infrastructure.mappers.feedback_mapper import FeedbackMapper


class FeedbackRepositorySQLAlchemy(FeedbackRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, feedback: Feedback) -> Feedback:
        model = FeedbackMapper.to_model(feedback)
        self.session.add(model)
        self.session.flush()
        return FeedbackMapper.to_domain(model)
