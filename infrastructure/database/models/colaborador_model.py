from datetime import date, datetime, timezone

from sqlalchemy import Date, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.base import Base


class ColaboradorModel(Base):
    __tablename__ = "colaboradores"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    matricula: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    email: Mapped[str | None] = mapped_column(String(150), unique=True, index=True)
    data_admissao: Mapped[date | None] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="ATIVO")
    setor_id: Mapped[int] = mapped_column(ForeignKey("setores.id"), nullable=False)
    funcao_id: Mapped[int] = mapped_column(ForeignKey("funcoes.id"), nullable=False)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    setor = relationship("SetorModel", back_populates="colaboradores")
    funcao = relationship("FuncaoModel", back_populates="colaboradores")
    avaliacoes = relationship("AvaliacaoModel", back_populates="colaborador")
    perfis_talento = relationship("PerfilTalentoModel", back_populates="colaborador")
    metas = relationship("MetaModel", back_populates="colaborador")
    feedbacks = relationship("FeedbackModel", back_populates="colaborador")
