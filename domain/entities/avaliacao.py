from dataclasses import dataclass, field
from datetime import datetime

from domain.entities.item_avaliacao import ItemAvaliacao
from domain.enums.tipo_avaliacao import TipoAvaliacao


@dataclass(slots=True)
class Avaliacao:
    colaborador_id: int
    avaliador_id: int
    tipo: TipoAvaliacao
    itens: list[ItemAvaliacao] = field(default_factory=list)
    observacao_geral: str | None = None
    status: str = "CONCLUIDA"
    id: int | None = None
    data_avaliacao: datetime | None = None
    criado_em: datetime | None = None

    def validar(self) -> None:
        if self.colaborador_id is None:
            raise ValueError("avaliacao must be linked to a colaborador")
        if self.avaliador_id is None:
            raise ValueError("avaliacao must have an avaliador")
        if not self.itens:
            raise ValueError("avaliacao must contain at least one item")

        competencias_avaliadas = set()
        for item in self.itens:
            item.validar()
            if item.competencia_id in competencias_avaliadas:
                raise ValueError("competencia cannot be evaluated twice")
            competencias_avaliadas.add(item.competencia_id)

    def adicionar_item(self, item: ItemAvaliacao) -> None:
        item.validar()
        if any(atual.competencia_id == item.competencia_id for atual in self.itens):
            raise ValueError("competencia cannot be evaluated twice")
        self.itens.append(item)

    def media_notas(self) -> float:
        if not self.itens:
            return 0.0
        return round(sum(item.nota for item in self.itens) / len(self.itens), 2)

    def esta_concluida(self) -> bool:
        return self.status == "CONCLUIDA"
