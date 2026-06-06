from dataclasses import dataclass

from domain.enums.tipo_avaliacao import TipoAvaliacao


@dataclass(slots=True)
class ItemAvaliacaoDTO:
    competencia_id: int
    nota: int
    comentario: str | None = None


@dataclass(slots=True)
class RegistrarAvaliacaoDTO:
    colaborador_id: int
    avaliador_id: int
    tipo: TipoAvaliacao
    observacao_geral: str | None
    itens: list[ItemAvaliacaoDTO]
