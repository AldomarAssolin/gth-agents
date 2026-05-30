from datetime import datetime, timezone

from app.extensions import db
from app.models.mixins import SerializerMixin


class Competencia(db.Model, SerializerMixin):
    __tablename__ = "competencias"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False, index=True)
    tipo = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.Text)
    peso = db.Column(db.Numeric(5, 2), nullable=False, default=1.00)
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    criado_em = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    itens_avaliacao = db.relationship("ItemAvaliacao", back_populates="competencia")
