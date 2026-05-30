from application.dtos.cadastro_dto import (
    CriarCompetenciaDTO,
    CriarFuncaoDTO,
    CriarSetorDTO,
    CriarUsuarioDTO,
)
from application.errors import ConflictError, ValidationError
from application.ports.competencia_repository import CompetenciaRepository
from application.ports.funcao_repository import FuncaoRepository
from application.ports.setor_repository import SetorRepository
from application.ports.usuario_repository import UsuarioRepository
from domain.entities.competencia import Competencia
from domain.entities.funcao import Funcao
from domain.entities.setor import Setor
from domain.entities.usuario import Usuario
from werkzeug.security import generate_password_hash


class ListarSetoresUC:
    def __init__(self, setores_repo: SetorRepository):
        self.setores_repo = setores_repo

    def execute(self) -> list[Setor]:
        return self.setores_repo.list()


class CriarSetorUC:
    def __init__(self, setores_repo: SetorRepository):
        self.setores_repo = setores_repo

    def execute(self, dto: CriarSetorDTO) -> Setor:
        if not dto.nome:
            raise ValidationError("Nome do setor e obrigatorio.")
        if self.setores_repo.get_by_nome(dto.nome):
            raise ConflictError("Ja existe setor com este nome.")
        return self.setores_repo.add(Setor(nome=dto.nome, descricao=dto.descricao))


class ListarFuncoesUC:
    def __init__(self, funcoes_repo: FuncaoRepository):
        self.funcoes_repo = funcoes_repo

    def execute(self) -> list[Funcao]:
        return self.funcoes_repo.list()


class CriarFuncaoUC:
    def __init__(self, funcoes_repo: FuncaoRepository):
        self.funcoes_repo = funcoes_repo

    def execute(self, dto: CriarFuncaoDTO) -> Funcao:
        if not dto.nome:
            raise ValidationError("Nome da funcao e obrigatorio.")
        if self.funcoes_repo.get_by_nome(dto.nome):
            raise ConflictError("Ja existe funcao com este nome.")
        return self.funcoes_repo.add(Funcao(nome=dto.nome, descricao=dto.descricao))


class ListarUsuariosUC:
    def __init__(self, usuarios_repo: UsuarioRepository):
        self.usuarios_repo = usuarios_repo

    def execute(self) -> list[Usuario]:
        return self.usuarios_repo.list()


class CriarUsuarioUC:
    def __init__(self, usuarios_repo: UsuarioRepository):
        self.usuarios_repo = usuarios_repo

    def execute(self, dto: CriarUsuarioDTO) -> Usuario:
        if not dto.nome:
            raise ValidationError("Nome do usuario e obrigatorio.")
        if not dto.email:
            raise ValidationError("Email do usuario e obrigatorio.")
        if not dto.senha:
            raise ValidationError("Senha do usuario e obrigatoria.")
        if self.usuarios_repo.get_by_email(dto.email):
            raise ConflictError("Ja existe usuario com este email.")
        return self.usuarios_repo.add(
            Usuario(
                nome=dto.nome,
                email=dto.email,
                senha_hash=generate_password_hash(dto.senha),
                perfil=dto.perfil,
            )
        )


class ListarCompetenciasUC:
    def __init__(self, competencias_repo: CompetenciaRepository):
        self.competencias_repo = competencias_repo

    def execute(self) -> list[Competencia]:
        return self.competencias_repo.list()


class CriarCompetenciaUC:
    def __init__(self, competencias_repo: CompetenciaRepository):
        self.competencias_repo = competencias_repo

    def execute(self, dto: CriarCompetenciaDTO) -> Competencia:
        if not dto.nome:
            raise ValidationError("Nome da competencia e obrigatorio.")
        return self.competencias_repo.add(
            Competencia(
                nome=dto.nome,
                tipo=dto.tipo,
                descricao=dto.descricao,
                peso=dto.peso,
            )
        )
