from decimal import Decimal

from application.dtos.cadastro_dto import (
    CriarCompetenciaDTO,
    CriarFuncaoDTO,
    CriarSetorDTO,
    CriarUsuarioDTO,
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
