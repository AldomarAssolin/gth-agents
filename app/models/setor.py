from datetime import datetime, timezone

from app.extensions import db
from app.models.mixins import SerializerMixin


class Setor(db.Model, SerializerMixin):
    __tablename__ = "setores"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True, index=True)
    descricao = db.Column(db.Text)
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    criado_em = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    colaboradores = db.relationship("Colaborador", back_populates="setor")
