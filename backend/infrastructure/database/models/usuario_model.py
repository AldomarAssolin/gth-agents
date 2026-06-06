from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.base import Base


class UsuarioModel(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True, index=True)
    senha_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    perfil: Mapped[str] = mapped_column(String(50), nullable=False)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    colaborador_id: Mapped[int | None] = mapped_column(ForeignKey("colaboradores.id"), nullable=True)
    setor_id: Mapped[int | None] = mapped_column(ForeignKey("setores.id"), nullable=True)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )


    avaliacoes = relationship("AvaliacaoModel", back_populates="avaliador")
    metas_criadas = relationship("MetaModel", back_populates="criado_por")
    feedbacks = relationship("FeedbackModel", back_populates="autor")
