from datetime import datetime, timezone

from app.extensions import db
from app.models.mixins import SerializerMixin
from domain.enums.status_colaborador import StatusColaborador


class Colaborador(db.Model, SerializerMixin):
    __tablename__ = "colaboradores"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    matricula = db.Column(db.String(50), nullable=False, unique=True, index=True)
    email = db.Column(db.String(150), unique=True, index=True)
    data_admissao = db.Column(db.Date)
    status = db.Column(db.String(30), nullable=False, default=StatusColaborador.ATIVO.value)
    setor_id = db.Column(db.Integer, db.ForeignKey("setores.id"), nullable=False)
    funcao_id = db.Column(db.Integer, db.ForeignKey("funcoes.id"), nullable=False)
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

    setor = db.relationship("Setor", back_populates="colaboradores")
    funcao = db.relationship("Funcao", back_populates="colaboradores")
    avaliacoes = db.relationship("Avaliacao", back_populates="colaborador")
    perfis_talento = db.relationship("PerfilTalento", back_populates="colaborador")
    metas = db.relationship("Meta", back_populates="colaborador")
    feedbacks = db.relationship("Feedback", back_populates="colaborador")

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["setor"] = self.setor.to_dict() if self.setor else None
        data["funcao"] = self.funcao.to_dict() if self.funcao else None
        return data
