from dataclasses import dataclass
from decimal import Decimal

from domain.enums.perfil_usuario import PerfilUsuario
from domain.enums.tipo_competencia import TipoCompetencia


@dataclass(slots=True)
class CriarSetorDTO:
    nome: str
    descricao: str | None = None


@dataclass(slots=True)
class CriarFuncaoDTO:
    nome: str
    descricao: str | None = None


@dataclass(slots=True)
class CriarUsuarioDTO:
    nome: str
    email: str
    senha: str
    perfil: PerfilUsuario


@dataclass(slots=True)
class CriarCompetenciaDTO:
    nome: str
    tipo: TipoCompetencia
    descricao: str | None = None
    peso: Decimal = Decimal("1.00")
