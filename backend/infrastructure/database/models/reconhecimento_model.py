from datetime import datetime, timezone
from sqlalchemy import DateTime, ForeignKey, String, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from infrastructure.database.base import Base


class ReconhecimentoModel(Base):
    __tablename__ = "reconhecimentos"

    id: Mapped[int] = mapped_column(primary_key=True)
    colaborador_id: Mapped[int] = mapped_column(ForeignKey("colaboradores.id"), nullable=False)
    tipo: Mapped[str] = mapped_column(String(50), nullable=False)
    descricao: Mapped[str] = mapped_column(Text, nullable=False)
    evidencia: Mapped[str] = mapped_column(Text, nullable=False)
    registrado_por_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    data_reconhecimento: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    ativo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    cancelado_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    cancelado_por_id: Mapped[int | None] = mapped_column(ForeignKey("usuarios.id"), nullable=True)
    motivo_cancelamento: Mapped[str | None] = mapped_column(Text, nullable=True)

    colaborador = relationship("ColaboradorModel")
    registrado_por = relationship("UsuarioModel", foreign_keys=[registrado_por_id])
    cancelado_por = relationship("UsuarioModel", foreign_keys=[cancelado_por_id])
