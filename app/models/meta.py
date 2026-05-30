from datetime import datetime, timezone

from app.extensions import db
from app.models.mixins import SerializerMixin
from domain.enums.status_meta import StatusMeta


class Meta(db.Model, SerializerMixin):
    __tablename__ = "metas"

    id = db.Column(db.Integer, primary_key=True)
    colaborador_id = db.Column(db.Integer, db.ForeignKey("colaboradores.id"), nullable=False)
    criado_por_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    indicador = db.Column(db.String(150))
    prazo = db.Column(db.Date, nullable=False)
    prioridade = db.Column(db.String(30), nullable=False, default="MEDIA")
    status = db.Column(db.String(30), nullable=False, default=StatusMeta.PENDENTE.value)
    origem = db.Column(db.String(50), nullable=False, default="MANUAL")
    criado_em = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    atualizado_em = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    colaborador = db.relationship("Colaborador", back_populates="metas")
    criado_por = db.relationship("Usuario")
