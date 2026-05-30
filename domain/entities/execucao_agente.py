from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class ExecucaoAgente:
    agente_nome: str
    entidade_tipo: str
    entidade_id: int
    entrada: dict | None = None
    saida: dict | None = None
    status: str = "SUCESSO"
    erro: str | None = None
    id: int | None = None
    criado_em: datetime | None = None
