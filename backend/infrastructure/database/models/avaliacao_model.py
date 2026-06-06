from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.base import Base


class AvaliacaoModel(Base):
    __tablename__ = "avaliacoes"

    id: Mapped[int] = mapped_column(primary_key=True)
    colaborador_id: Mapped[int] = mapped_column(ForeignKey("colaboradores.id"), nullable=False)
    avaliador_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    tipo: Mapped[str] = mapped_column(String(50), nullable=False)
    observacao_geral: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="CONCLUIDA")
    data_avaliacao: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    colaborador = relationship("ColaboradorModel", back_populates="avaliacoes")
    avaliador = relationship("UsuarioModel", back_populates="avaliacoes")
    itens = relationship(
        "ItemAvaliacaoModel",
        back_populates="avaliacao",
        cascade="all, delete-orphan",
    )


class ItemAvaliacaoModel(Base):
    __tablename__ = "itens_avaliacao"

    id: Mapped[int] = mapped_column(primary_key=True)
    avaliacao_id: Mapped[int] = mapped_column(
        ForeignKey("avaliacoes.id", ondelete="CASCADE"),
        nullable=False,
    )
    competencia_id: Mapped[int] = mapped_column(ForeignKey("competencias.id"), nullable=False)
    nota: Mapped[int] = mapped_column(Integer, nullable=False)
    comentario: Mapped[str | None] = mapped_column(Text)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    avaliacao = relationship("AvaliacaoModel", back_populates="itens")
    competencia = relationship("CompetenciaModel", back_populates="itens_avaliacao")
