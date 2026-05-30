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


@dataclass(slots=True)
class AtualizarSetorDTO:
    id: int
    nome: str
    descricao: str | None = None


@dataclass(slots=True)
class AtualizarFuncaoDTO:
    id: int
    nome: str
    descricao: str | None = None


@dataclass(slots=True)
class AtualizarUsuarioDTO:
    id: int
    nome: str
    email: str
    perfil: PerfilUsuario
    senha: str | None = None


@dataclass(slots=True)
class AtualizarCompetenciaDTO:
    id: int
    nome: str
    tipo: TipoCompetencia
    descricao: str | None = None
    peso: Decimal = Decimal("1.00")
