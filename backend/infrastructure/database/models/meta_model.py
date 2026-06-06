from datetime import date, datetime, timezone

from sqlalchemy import Date, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.base import Base


class MetaModel(Base):
    __tablename__ = "metas"

    id: Mapped[int] = mapped_column(primary_key=True)
    colaborador_id: Mapped[int] = mapped_column(ForeignKey("colaboradores.id"), nullable=False)
    criado_por_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    titulo: Mapped[str] = mapped_column(String(150), nullable=False)
    descricao: Mapped[str] = mapped_column(Text, nullable=False)
    indicador: Mapped[str | None] = mapped_column(String(150))
    prazo: Mapped[date] = mapped_column(Date, nullable=False)
    prioridade: Mapped[str] = mapped_column(String(30), nullable=False, default="MEDIA")
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="PENDENTE")
    origem: Mapped[str] = mapped_column(String(50), nullable=False, default="MANUAL")
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

    colaborador = relationship("ColaboradorModel", back_populates="metas")
    criado_por = relationship("UsuarioModel", back_populates="metas_criadas")
