from application.dtos.meta_dto import CriarMetaDTO
from application.errors import NotFoundError, ValidationError
from application.ports.colaborador_repository import ColaboradorRepository
from application.ports.meta_repository import MetaRepository
from application.ports.usuario_repository import UsuarioRepository
from domain.entities.meta import Meta
from domain.enums.status_meta import StatusMeta


class CriarMetaUC:
    def __init__(
        self,
        colaboradores_repo: ColaboradorRepository,
        usuarios_repo: UsuarioRepository,
        metas_repo: MetaRepository,
    ):
        self.colaboradores_repo = colaboradores_repo
        self.usuarios_repo = usuarios_repo
        self.metas_repo = metas_repo

    def execute(self, dto: CriarMetaDTO) -> Meta:
        colaborador = self.colaboradores_repo.get_by_id(dto.colaborador_id)
        if not colaborador:
            raise NotFoundError("Colaborador nao encontrado.")

        criador = self.usuarios_repo.get_by_id(dto.criado_por_id)
        if not criador:
            raise NotFoundError("Usuario criador nao encontrado.")

        if not dto.titulo:
            raise ValidationError("Titulo da meta e obrigatorio.")
        if not dto.descricao:
            raise ValidationError("Descricao da meta e obrigatoria.")
        if not dto.prazo:
            raise ValidationError("Prazo da meta e obrigatorio.")

        meta = Meta(
            colaborador_id=dto.colaborador_id,
            criado_por_id=dto.criado_por_id,
            titulo=dto.titulo,
            descricao=dto.descricao,
            prazo=dto.prazo,
            indicador=dto.indicador,
            prioridade=dto.prioridade,
            status=StatusMeta.PENDENTE,
            origem="MANUAL",
        )
        return self.metas_repo.add(meta)
