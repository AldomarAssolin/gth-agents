from datetime import datetime, timezone

from sqlalchemy.dialects.postgresql import JSONB

from app.extensions import db
from app.models.mixins import SerializerMixin


class ExecucaoAgente(db.Model, SerializerMixin):
    __tablename__ = "execucoes_agente"

    id = db.Column(db.Integer, primary_key=True)
    agente_nome = db.Column(db.String(100), nullable=False)
    entidade_tipo = db.Column(db.String(100), nullable=False)
    entidade_id = db.Column(db.Integer, nullable=False)
    entrada = db.Column(JSONB)
    saida = db.Column(JSONB)
    status = db.Column(db.String(30), nullable=False, default="SUCESSO")
    erro = db.Column(db.Text)
    criado_em = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
