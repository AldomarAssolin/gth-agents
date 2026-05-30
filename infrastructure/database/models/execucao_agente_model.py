from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.base import Base


class ExecucaoAgenteModel(Base):
    __tablename__ = "execucoes_agente"

    id: Mapped[int] = mapped_column(primary_key=True)
    agente_nome: Mapped[str] = mapped_column(String(100), nullable=False)
    entidade_tipo: Mapped[str] = mapped_column(String(100), nullable=False)
    entidade_id: Mapped[int] = mapped_column(Integer, nullable=False)
    entrada: Mapped[dict | None] = mapped_column(JSON)
    saida: Mapped[dict | None] = mapped_column(JSON)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="SUCESSO")
    erro: Mapped[str | None] = mapped_column(Text)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
