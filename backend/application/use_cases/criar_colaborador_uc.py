from application.dtos.colaborador_dto import CriarColaboradorDTO
from application.errors import ConflictError, NotFoundError, ValidationError
from application.ports.colaborador_repository import ColaboradorRepository
from application.ports.funcao_repository import FuncaoRepository
from application.ports.setor_repository import SetorRepository
from domain.entities.colaborador import Colaborador
from domain.enums.status_colaborador import StatusColaborador


class CriarColaboradorUC:
    def __init__(
        self,
        colaboradores_repo: ColaboradorRepository,
        setores_repo: SetorRepository,
        funcoes_repo: FuncaoRepository,
    ):
        self.colaboradores_repo = colaboradores_repo
        self.setores_repo = setores_repo
        self.funcoes_repo = funcoes_repo

    def execute(self, dto: CriarColaboradorDTO) -> Colaborador:
        if not dto.nome:
            raise ValidationError("Nome do colaborador e obrigatorio.")
        if not dto.matricula:
            raise ValidationError("Matricula do colaborador e obrigatoria.")

        existente = self.colaboradores_repo.get_by_matricula(dto.matricula)
        if existente:
            raise ConflictError("Ja existe colaborador com esta matricula.")

        setor = self.setores_repo.get_by_id(dto.setor_id)
        if not setor:
            raise NotFoundError("Setor nao encontrado.")

        funcao = self.funcoes_repo.get_by_id(dto.funcao_id)
        if not funcao:
            raise NotFoundError("Funcao nao encontrada.")

        colaborador = Colaborador(
            nome=dto.nome,
            matricula=dto.matricula,
            email=dto.email,
            data_admissao=dto.data_admissao,
            setor_id=dto.setor_id,
            funcao_id=dto.funcao_id,
            status=StatusColaborador.ATIVO,
        )
        return self.colaboradores_repo.add(colaborador)
