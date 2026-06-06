from datetime import date
from application.dtos.pdi_dto import (
    CriarPDIDTO,
    AcaoPDIInputDTO,
    CriarAcaoPDIDTO,
    AtualizarPDIDTO,
    AtualizarAcaoPDIDTO,
)
from application.errors import ValidationError


def parse_date(date_str: str | None) -> date | None:
    if not date_str:
        return None
    try:
        return date.fromisoformat(date_str)
    except ValueError:
        raise ValidationError(f"Data '{date_str}' invalida. Deve estar no formato YYYY-MM-DD.")


def parse_criar_pdi(data: dict, criado_por_id: int) -> CriarPDIDTO:
    data_inicio = parse_date(data.get("data_inicio"))
    data_fim = parse_date(data.get("data_fim"))

    acoes_dto = []
    if "acoes" in data and data["acoes"] is not None:
        for acao_data in data["acoes"]:
            prazo = parse_date(acao_data.get("prazo"))
            if not prazo:
                raise ValidationError("Prazo da acao e obrigatorio.")
            acoes_dto.append(
                AcaoPDIInputDTO(
                    tipo=acao_data.get("tipo"),
                    descricao=acao_data.get("descricao"),
                    prazo=prazo,
                )
            )

    return CriarPDIDTO(
        colaborador_id=data.get("colaborador_id"),
        titulo=data.get("titulo"),
        descricao=data.get("descricao"),
        criado_por_id=criado_por_id,
        origem=data.get("origem", "MANUAL"),
        status=data.get("status", "ATIVO"),
        data_inicio=data_inicio,
        data_fim=data_fim,
        acoes=acoes_dto,
    )


def parse_atualizar_pdi(pdi_id: int, data: dict) -> AtualizarPDIDTO:
    data_inicio = parse_date(data.get("data_inicio"))
    data_fim = parse_date(data.get("data_fim"))
    return AtualizarPDIDTO(
        id=pdi_id,
        titulo=data.get("titulo"),
        descricao=data.get("descricao"),
        data_inicio=data_inicio,
        data_fim=data_fim,
    )


def parse_criar_acao_pdi(pdi_id: int, data: dict) -> CriarAcaoPDIDTO:
    prazo = parse_date(data.get("prazo"))
    if not prazo:
        raise ValidationError("Prazo da acao e obrigatorio.")
    return CriarAcaoPDIDTO(
        pdi_id=pdi_id,
        tipo=data.get("tipo"),
        descricao=data.get("descricao"),
        prazo=prazo,
    )


def parse_atualizar_acao_pdi(acao_id: int, data: dict) -> AtualizarAcaoPDIDTO:
    prazo = parse_date(data.get("prazo"))
    if not prazo:
        raise ValidationError("Prazo da acao e obrigatorio.")
    return AtualizarAcaoPDIDTO(
        id=acao_id,
        tipo=data.get("tipo"),
        descricao=data.get("descricao"),
        prazo=prazo,
    )
