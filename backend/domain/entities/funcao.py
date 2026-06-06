from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Funcao:
    nome: str
    descricao: str | None = None
    ativo: bool = True
    id: int | None = None
    criado_em: datetime | None = None

    def ativar(self) -> None:
        self.ativo = True

    def desativar(self) -> None:
        self.ativo = False

    def esta_ativa(self) -> bool:
        return self.ativo
