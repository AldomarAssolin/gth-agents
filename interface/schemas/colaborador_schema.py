from datetime import date

from application.dtos.colaborador_dto import CriarColaboradorDTO, AtualizarColaboradorDTO


def parse_criar_colaborador(data: dict) -> CriarColaboradorDTO:
    return CriarColaboradorDTO(
        nome=data.get("nome"),
        matricula=data.get("matricula"),
        email=data.get("email"),
        data_admissao=date.fromisoformat(data["data_admissao"])
        if data.get("data_admissao")
        else None,
        setor_id=data.get("setor_id"),
        funcao_id=data.get("funcao_id"),
    )


def parse_atualizar_colaborador(entity_id: int, data: dict) -> AtualizarColaboradorDTO:
    return AtualizarColaboradorDTO(
        id=entity_id,
        nome=data.get("nome"),
        matricula=data.get("matricula"),
        email=data.get("email"),
        data_admissao=date.fromisoformat(data["data_admissao"])
        if data.get("data_admissao")
        else None,
        setor_id=data.get("setor_id"),
        funcao_id=data.get("funcao_id"),
    )
