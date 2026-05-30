from dataclasses import dataclass


@dataclass(slots=True)
class ItemAvaliacao:
    competencia_id: int
    nota: int
    comentario: str | None = None
    id: int | None = None

    def validar(self) -> None:
        if self.competencia_id is None:
            raise ValueError("item avaliacao must have a competencia")
        if self.nota < 1 or self.nota > 5:
            raise ValueError("nota must be between 1 and 5")

    def esta_acima_do_esperado(self) -> bool:
        return self.nota >= 4

    def necessita_desenvolvimento(self) -> bool:
        return self.nota <= 2
