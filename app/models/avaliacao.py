from datetime import datetime, timezone

from app.extensions import db
from app.models.mixins import SerializerMixin


class Avaliacao(db.Model, SerializerMixin):
    __tablename__ = "avaliacoes"

    id = db.Column(db.Integer, primary_key=True)
    colaborador_id = db.Column(db.Integer, db.ForeignKey("colaboradores.id"), nullable=False)
    avaliador_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    observacao_geral = db.Column(db.Text)
    status = db.Column(db.String(30), nullable=False, default="CONCLUIDA")
    data_avaliacao = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    criado_em = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    colaborador = db.relationship("Colaborador", back_populates="avaliacoes")
    avaliador = db.relationship("Usuario")
    itens = db.relationship(
        "ItemAvaliacao",
        back_populates="avaliacao",
        cascade="all, delete-orphan",
    )

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["itens"] = [item.to_dict() for item in self.itens]
        return data
