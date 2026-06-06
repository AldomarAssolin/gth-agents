from application.errors import NotFoundError
from application.ports.colaborador_repository import ColaboradorRepository
from application.ports.meta_repository import MetaRepository
from domain.entities.meta import Meta


class ListarMetasColaboradorUC:
    def __init__(
        self,
        colaboradores_repo: ColaboradorRepository,
        metas_repo: MetaRepository,
    ):
        self.colaboradores_repo = colaboradores_repo
        self.metas_repo = metas_repo

    def execute(self, colaborador_id: int) -> list[Meta]:
        colaborador = self.colaboradores_repo.get_by_id(colaborador_id)
        if not colaborador:
            raise NotFoundError("Colaborador nao encontrado.")
        return self.metas_repo.list_by_colaborador(colaborador_id)
