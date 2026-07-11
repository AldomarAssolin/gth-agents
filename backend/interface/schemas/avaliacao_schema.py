from application.dtos.avaliacao_dto import ItemAvaliacaoDTO, RegistrarAvaliacaoDTO
from domain.enums.tipo_avaliacao import TipoAvaliacao


def parse_registrar_avaliacao(data: dict, avaliador_id: int) -> RegistrarAvaliacaoDTO:
    itens = [
        ItemAvaliacaoDTO(
            competencia_id=item.get("competencia_id"),
            nota=item.get("nota"),
            comentario=item.get("comentario"),
        )
        for item in data.get("itens", [])
    ]
    return RegistrarAvaliacaoDTO(
        colaborador_id=data.get("colaborador_id"),
        avaliador_id=avaliador_id,
        tipo=TipoAvaliacao((data.get("tipo") or TipoAvaliacao.AVALIACAO_LIDER.value).upper()),
        observacao_geral=data.get("observacao_geral"),
        itens=itens,
    )
