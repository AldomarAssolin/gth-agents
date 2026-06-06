from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.base import Base


class FeedbackModel(Base):
    __tablename__ = "feedbacks"

    id: Mapped[int] = mapped_column(primary_key=True)
    colaborador_id: Mapped[int] = mapped_column(ForeignKey("colaboradores.id"), nullable=False)
    autor_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    contexto: Mapped[str | None] = mapped_column(Text)
    ponto_positivo: Mapped[str] = mapped_column(Text, nullable=False)
    ponto_melhoria: Mapped[str | None] = mapped_column(Text)
    acao_recomendada: Mapped[str] = mapped_column(Text, nullable=False)
    origem: Mapped[str] = mapped_column(String(50), nullable=False, default="MANUAL")
    data_feedback: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    colaborador = relationship("ColaboradorModel", back_populates="feedbacks")
    autor = relationship("UsuarioModel", back_populates="feedbacks")
