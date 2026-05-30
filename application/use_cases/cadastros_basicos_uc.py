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
from application.errors import ConflictError, ValidationError, NotFoundError
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


class BuscarSetorPorIdUC:
    def __init__(self, setores_repo: SetorRepository):
        self.setores_repo = setores_repo

    def execute(self, setor_id: int) -> Setor:
        setor = self.setores_repo.get_by_id(setor_id)
        if not setor:
            raise NotFoundError("Setor nao encontrado.")
        return setor


class AtualizarSetorUC:
    def __init__(self, setores_repo: SetorRepository):
        self.setores_repo = setores_repo

    def execute(self, dto: AtualizarSetorDTO) -> Setor:
        setor = self.setores_repo.get_by_id(dto.id)
        if not setor:
            raise NotFoundError("Setor nao encontrado.")
        if not dto.nome:
            raise ValidationError("Nome do setor e obrigatorio.")
        existente = self.setores_repo.get_by_nome(dto.nome)
        if existente and existente.id != dto.id:
            raise ConflictError("Ja existe setor com este nome.")
        setor.nome = dto.nome
        setor.descricao = dto.descricao
        self.setores_repo.save(setor)
        return setor


class DesativarSetorUC:
    def __init__(self, setores_repo: SetorRepository):
        self.setores_repo = setores_repo

    def execute(self, setor_id: int) -> Setor:
        setor = self.setores_repo.get_by_id(setor_id)
        if not setor:
            raise NotFoundError("Setor nao encontrado.")
        setor.desativar()
        self.setores_repo.save(setor)
        return setor


class BuscarFuncaoPorIdUC:
    def __init__(self, funcoes_repo: FuncaoRepository):
        self.funcoes_repo = funcoes_repo

    def execute(self, funcao_id: int) -> Funcao:
        funcao = self.funcoes_repo.get_by_id(funcao_id)
        if not funcao:
            raise NotFoundError("Funcao nao encontrada.")
        return funcao


class AtualizarFuncaoUC:
    def __init__(self, funcoes_repo: FuncaoRepository):
        self.funcoes_repo = funcoes_repo

    def execute(self, dto: AtualizarFuncaoDTO) -> Funcao:
        funcao = self.funcoes_repo.get_by_id(dto.id)
        if not funcao:
            raise NotFoundError("Funcao nao encontrada.")
        if not dto.nome:
            raise ValidationError("Nome da funcao e obrigatorio.")
        existente = self.funcoes_repo.get_by_nome(dto.nome)
        if existente and existente.id != dto.id:
            raise ConflictError("Ja existe funcao com este nome.")
        funcao.nome = dto.nome
        funcao.descricao = dto.descricao
        self.funcoes_repo.save(funcao)
        return funcao


class DesativarFuncaoUC:
    def __init__(self, funcoes_repo: FuncaoRepository):
        self.funcoes_repo = funcoes_repo

    def execute(self, funcao_id: int) -> Funcao:
        funcao = self.funcoes_repo.get_by_id(funcao_id)
        if not funcao:
            raise NotFoundError("Funcao nao encontrada.")
        funcao.desativar()
        self.funcoes_repo.save(funcao)
        return funcao


class BuscarUsuarioPorIdUC:
    def __init__(self, usuarios_repo: UsuarioRepository):
        self.usuarios_repo = usuarios_repo

    def execute(self, usuario_id: int) -> Usuario:
        usuario = self.usuarios_repo.get_by_id(usuario_id)
        if not usuario:
            raise NotFoundError("Usuario nao encontrado.")
        return usuario


class AtualizarUsuarioUC:
    def __init__(self, usuarios_repo: UsuarioRepository):
        self.usuarios_repo = usuarios_repo

    def execute(self, dto: AtualizarUsuarioDTO) -> Usuario:
        usuario = self.usuarios_repo.get_by_id(dto.id)
        if not usuario:
            raise NotFoundError("Usuario nao encontrado.")
        if not dto.nome:
            raise ValidationError("Nome do usuario e obrigatorio.")
        if not dto.email:
            raise ValidationError("Email do usuario e obrigatorio.")
        existente = self.usuarios_repo.get_by_email(dto.email)
        if existente and existente.id != dto.id:
            raise ConflictError("Ja existe usuario com este email.")
        usuario.nome = dto.nome
        usuario.email = dto.email
        usuario.perfil = dto.perfil
        if dto.senha:
            usuario.senha_hash = generate_password_hash(dto.senha)
        self.usuarios_repo.save(usuario)
        return usuario


class DesativarUsuarioUC:
    def __init__(self, usuarios_repo: UsuarioRepository):
        self.usuarios_repo = usuarios_repo

    def execute(self, usuario_id: int) -> Usuario:
        usuario = self.usuarios_repo.get_by_id(usuario_id)
        if not usuario:
            raise NotFoundError("Usuario nao encontrado.")
        usuario.desativar()
        self.usuarios_repo.save(usuario)
        return usuario


class BuscarCompetenciaPorIdUC:
    def __init__(self, competencias_repo: CompetenciaRepository):
        self.competencias_repo = competencias_repo

    def execute(self, competencia_id: int) -> Competencia:
        competencia = self.competencias_repo.get_by_id(competencia_id)
        if not competencia:
            raise NotFoundError("Competencia nao encontrada.")
        return competencia


class AtualizarCompetenciaUC:
    def __init__(self, competencias_repo: CompetenciaRepository):
        self.competencias_repo = competencias_repo

    def execute(self, dto: AtualizarCompetenciaDTO) -> Competencia:
        competencia = self.competencias_repo.get_by_id(dto.id)
        if not competencia:
            raise NotFoundError("Competencia nao encontrada.")
        if not dto.nome:
            raise ValidationError("Nome da competencia e obrigatorio.")
        competencia.nome = dto.nome
        competencia.tipo = dto.tipo
        competencia.descricao = dto.descricao
        competencia.peso = dto.peso
        self.competencias_repo.save(competencia)
        return competencia


class DesativarCompetenciaUC:
    def __init__(self, competencias_repo: CompetenciaRepository):
        self.competencias_repo = competencias_repo

    def execute(self, competencia_id: int) -> Competencia:
        competencia = self.competencias_repo.get_by_id(competencia_id)
        if not competencia:
            raise NotFoundError("Competencia nao encontrada.")
        competencia.desativar()
        self.competencias_repo.save(competencia)
        return competencia
