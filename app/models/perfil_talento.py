from datetime import datetime, timezone

from sqlalchemy.dialects.postgresql import JSONB

from app.extensions import db
from app.models.mixins import SerializerMixin


class PerfilTalento(db.Model, SerializerMixin):
    __tablename__ = "perfis_talento"

    id = db.Column(db.Integer, primary_key=True)
    colaborador_id = db.Column(db.Integer, db.ForeignKey("colaboradores.id"), nullable=False)
    classificacao = db.Column(db.String(80), nullable=False)
    resumo = db.Column(db.Text)
    nivel_tecnico = db.Column(db.String(30))
    nivel_comportamental = db.Column(db.String(30))
    potencial_lideranca = db.Column(db.String(30))
    pontos_fortes = db.Column(JSONB)
    pontos_melhoria = db.Column(JSONB)
    recomendacoes = db.Column(JSONB)
    origem = db.Column(db.String(50), nullable=False, default="AGENTE_IA")
    criado_em = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    colaborador = db.relationship("Colaborador", back_populates="perfis_talento")
