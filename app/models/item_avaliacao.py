from datetime import datetime, timezone

from app.extensions import db
from app.models.mixins import SerializerMixin


class ItemAvaliacao(db.Model, SerializerMixin):
    __tablename__ = "itens_avaliacao"

    id = db.Column(db.Integer, primary_key=True)
    avaliacao_id = db.Column(
        db.Integer,
        db.ForeignKey("avaliacoes.id", ondelete="CASCADE"),
        nullable=False,
    )
    competencia_id = db.Column(db.Integer, db.ForeignKey("competencias.id"), nullable=False)
    nota = db.Column(db.Integer, nullable=False)
    comentario = db.Column(db.Text)
    criado_em = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    avaliacao = db.relationship("Avaliacao", back_populates="itens")
    competencia = db.relationship("Competencia", back_populates="itens_avaliacao")

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["competencia"] = self.competencia.to_dict() if self.competencia else None
        return data
