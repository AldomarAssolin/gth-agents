from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.base import Base


class PerfilTalentoModel(Base):
    __tablename__ = "perfis_talento"

    id: Mapped[int] = mapped_column(primary_key=True)
    colaborador_id: Mapped[int] = mapped_column(ForeignKey("colaboradores.id"), nullable=False)
    classificacao: Mapped[str] = mapped_column(String(80), nullable=False)
    resumo: Mapped[str | None] = mapped_column(Text)
    nivel_tecnico: Mapped[str | None] = mapped_column(String(30))
    nivel_comportamental: Mapped[str | None] = mapped_column(String(30))
    potencial_lideranca: Mapped[str | None] = mapped_column(String(30))
    pontos_fortes: Mapped[list | None] = mapped_column(JSON)
    pontos_melhoria: Mapped[list | None] = mapped_column(JSON)
    recomendacoes: Mapped[list | None] = mapped_column(JSON)
    origem: Mapped[str] = mapped_column(String(50), nullable=False, default="AGENTE_IA")
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    colaborador = relationship("ColaboradorModel", back_populates="perfis_talento")
