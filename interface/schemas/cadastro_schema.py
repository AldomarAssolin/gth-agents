from decimal import Decimal

from application.dtos.cadastro_dto import (
    CriarCompetenciaDTO,
    CriarFuncaoDTO,
    CriarSetorDTO,
    CriarUsuarioDTO,
    AtualizarCompetenciaDTO,
    AtualizarFuncaoDTO,
    AtualizarSetorDTO,
    AtualizarUsuarioDTO,
)
from domain.enums.perfil_usuario import PerfilUsuario
from domain.enums.tipo_competencia import TipoCompetencia


def parse_criar_setor(data: dict) -> CriarSetorDTO:
    return CriarSetorDTO(nome=data.get("nome"), descricao=data.get("descricao"))


def parse_criar_funcao(data: dict) -> CriarFuncaoDTO:
    return CriarFuncaoDTO(nome=data.get("nome"), descricao=data.get("descricao"))


def parse_criar_usuario(data: dict) -> CriarUsuarioDTO:
    return CriarUsuarioDTO(
        nome=data.get("nome"),
        email=data.get("email"),
        senha=data.get("senha"),
        perfil=PerfilUsuario((data.get("perfil") or "").upper()),
    )


def parse_criar_competencia(data: dict) -> CriarCompetenciaDTO:
    return CriarCompetenciaDTO(
        nome=data.get("nome"),
        tipo=TipoCompetencia((data.get("tipo") or "").upper()),
        descricao=data.get("descricao"),
        peso=Decimal(str(data.get("peso", "1.00"))),
    )


def parse_atualizar_setor(entity_id: int, data: dict) -> AtualizarSetorDTO:
    return AtualizarSetorDTO(
        id=entity_id,
        nome=data.get("nome"),
        descricao=data.get("descricao")
    )


def parse_atualizar_funcao(entity_id: int, data: dict) -> AtualizarFuncaoDTO:
    return AtualizarFuncaoDTO(
        id=entity_id,
        nome=data.get("nome"),
        descricao=data.get("descricao")
    )


def parse_atualizar_usuario(entity_id: int, data: dict) -> AtualizarUsuarioDTO:
    perfil_val = data.get("perfil")
    perfil = PerfilUsuario(perfil_val.upper()) if perfil_val else None
    return AtualizarUsuarioDTO(
        id=entity_id,
        nome=data.get("nome"),
        email=data.get("email"),
        perfil=perfil,
        senha=data.get("senha")
    )


def parse_atualizar_competencia(entity_id: int, data: dict) -> AtualizarCompetenciaDTO:
    tipo_val = data.get("tipo")
    tipo = TipoCompetencia(tipo_val.upper()) if tipo_val else None
    peso_val = data.get("peso")
    peso = Decimal(str(peso_val)) if peso_val is not None else Decimal("1.00")
    return AtualizarCompetenciaDTO(
        id=entity_id,
        nome=data.get("nome"),
        tipo=tipo,
        descricao=data.get("descricao"),
        peso=peso
    )
