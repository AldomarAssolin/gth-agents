from dataclasses import dataclass


@dataclass(slots=True)
class RegistrarExecucaoAgenteDTO:
    agente_nome: str
    entidade_tipo: str
    entidade_id: int
    entrada: dict | None = None
    saida: dict | None = None
    status: str = "SUCESSO"
    erro: str | None = None
