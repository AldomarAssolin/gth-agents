from application.dtos.reconhecimento_dto import (
    CriarReconhecimentoDTO,
    CancelarReconhecimentoDTO,
)
from application.errors import ValidationError
from domain.enums.tipo_reconhecimento import TipoReconhecimento


def parse_criar_reconhecimento(data: dict, registrado_por_id: int) -> CriarReconhecimentoDTO:
    colaborador_id = data.get("colaborador_id")
    tipo = data.get("tipo")
    descricao = data.get("descricao")
    evidencia = data.get("evidencia")

    if not colaborador_id:
        raise ValidationError("Colaborador e obrigatorio.")

    if not tipo:
        raise ValidationError("Tipo de reconhecimento e obrigatorio.")

    try:
        tipo_enum = TipoReconhecimento(tipo)
    except ValueError:
        raise ValidationError("Tipo de reconhecimento invalido.")

    if not descricao or not descricao.strip():
        raise ValidationError("Descricao do reconhecimento e obrigatoria.")

    if not evidencia or not evidencia.strip():
        raise ValidationError("Evidencia do reconhecimento e obrigatoria.")

    return CriarReconhecimentoDTO(
        colaborador_id=colaborador_id,
        tipo=tipo_enum,
        descricao=descricao,
        evidencia=evidencia,
        registrado_por_id=registrado_por_id,
    )


def parse_cancelar_reconhecimento(
    reconhecimento_id: int, data: dict, cancelado_por_id: int
) -> CancelarReconhecimentoDTO:
    motivo = data.get("motivo_cancelamento")

    if not motivo or not motivo.strip():
        raise ValidationError("Motivo do cancelamento e obrigatorio.")

    return CancelarReconhecimentoDTO(
        reconhecimento_id=reconhecimento_id,
        cancelado_por_id=cancelado_por_id,
        motivo_cancelamento=motivo,
    )
