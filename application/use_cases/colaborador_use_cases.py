from application.dtos.colaborador_dto import AtualizarColaboradorDTO
from application.errors import ConflictError, NotFoundError, ValidationError
from application.ports.colaborador_repository import ColaboradorRepository
from application.ports.funcao_repository import FuncaoRepository
from application.ports.setor_repository import SetorRepository
from domain.entities.colaborador import Colaborador
from domain.enums.status_colaborador import StatusColaborador


class ListarColaboradoresUC:
    def __init__(self, colaboradores_repo: ColaboradorRepository):
        self.colaboradores_repo = colaboradores_repo

    def execute(self) -> list[Colaborador]:
        return self.colaboradores_repo.list()


class BuscarColaboradorPorIdUC:
    def __init__(self, colaboradores_repo: ColaboradorRepository):
        self.colaboradores_repo = colaboradores_repo

    def execute(self, colaborador_id: int) -> Colaborador:
        colaborador = self.colaboradores_repo.get_by_id(colaborador_id)
        if not colaborador:
            raise NotFoundError("Colaborador nao encontrado.")
        return colaborador


class AtualizarColaboradorUC:
    def __init__(
        self,
        colaboradores_repo: ColaboradorRepository,
        setores_repo: SetorRepository,
        funcoes_repo: FuncaoRepository,
    ):
        self.colaboradores_repo = colaboradores_repo
        self.setores_repo = setores_repo
        self.funcoes_repo = funcoes_repo

    def execute(self, dto: AtualizarColaboradorDTO) -> Colaborador:
        colaborador = self.colaboradores_repo.get_by_id(dto.id)
        if not colaborador:
            raise NotFoundError("Colaborador nao encontrado.")

        if not dto.nome:
            raise ValidationError("Nome do colaborador e obrigatorio.")
        if not dto.matricula:
            raise ValidationError("Matricula do colaborador e obrigatoria.")

        existente = self.colaboradores_repo.get_by_matricula(dto.matricula)
        if existente and existente.id != dto.id:
            raise ConflictError("Ja existe colaborador com esta matricula.")

        setor = self.setores_repo.get_by_id(dto.setor_id)
        if not setor:
            raise NotFoundError("Setor nao encontrado.")

        funcao = self.funcoes_repo.get_by_id(dto.funcao_id)
        if not funcao:
            raise NotFoundError("Funcao nao encontrada.")

        colaborador.nome = dto.nome
        colaborador.matricula = dto.matricula
        colaborador.email = dto.email
        colaborador.data_admissao = dto.data_admissao
        colaborador.setor_id = dto.setor_id
        colaborador.funcao_id = dto.funcao_id

        self.colaboradores_repo.save(colaborador)
        return colaborador


class AlterarStatusColaboradorUC:
    def __init__(self, colaboradores_repo: ColaboradorRepository):
        self.colaboradores_repo = colaboradores_repo

    def execute(self, colaborador_id: int, status: StatusColaborador) -> Colaborador:
        colaborador = self.colaboradores_repo.get_by_id(colaborador_id)
        if not colaborador:
            raise NotFoundError("Colaborador nao encontrado.")

        if status == StatusColaborador.ATIVO:
            colaborador.ativar()
        elif status == StatusColaborador.INATIVO:
            colaborador.inativar()
        elif status == StatusColaborador.AFASTADO:
            colaborador.afastar()
        elif status == StatusColaborador.DESLIGADO:
            colaborador.desligar()
        else:
            raise ValidationError("Status invalido.")

        self.colaboradores_repo.save(colaborador)
        return colaborador
