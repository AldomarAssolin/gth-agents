from datetime import datetime, timezone

from app.extensions import db
from app.models.mixins import SerializerMixin


class Feedback(db.Model, SerializerMixin):
    __tablename__ = "feedbacks"

    id = db.Column(db.Integer, primary_key=True)
    colaborador_id = db.Column(db.Integer, db.ForeignKey("colaboradores.id"), nullable=False)
    autor_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    contexto = db.Column(db.Text)
    ponto_positivo = db.Column(db.Text, nullable=False)
    ponto_melhoria = db.Column(db.Text)
    acao_recomendada = db.Column(db.Text, nullable=False)
    origem = db.Column(db.String(50), nullable=False, default="MANUAL")
    data_feedback = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    criado_em = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    colaborador = db.relationship("Colaborador", back_populates="feedbacks")
    autor = db.relationship("Usuario")
