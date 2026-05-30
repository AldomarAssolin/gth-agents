from application.errors import NotFoundError
from application.ports.avaliacao_repository import AvaliacaoRepository
from application.ports.colaborador_repository import ColaboradorRepository
from application.ports.competencia_repository import CompetenciaRepository
from application.ports.feedback_repository import FeedbackRepository
from application.ports.meta_repository import MetaRepository
from application.ports.perfil_talento_repository import PerfilTalentoRepository
from domain.enums.status_meta import StatusMeta
from domain.enums.tipo_competencia import TipoCompetencia


class VisualizarEvolucaoColaboradorUC:
    def __init__(
        self,
        colaboradores_repo: ColaboradorRepository,
        avaliacoes_repo: AvaliacaoRepository,
        metas_repo: MetaRepository,
        feedbacks_repo: FeedbackRepository,
        perfis_repo: PerfilTalentoRepository,
        competencias_repo: CompetenciaRepository,
    ):
        self.colaboradores_repo = colaboradores_repo
        self.avaliacoes_repo = avaliacoes_repo
        self.metas_repo = metas_repo
        self.feedbacks_repo = feedbacks_repo
        self.perfis_repo = perfis_repo
        self.competencias_repo = competencias_repo

    def execute(self, colaborador_id: int) -> dict:
        colaborador = self.colaboradores_repo.get_by_id(colaborador_id)
        if not colaborador:
            raise NotFoundError("Colaborador nao encontrado.")

        avaliacoes = self.avaliacoes_repo.list_by_colaborador(colaborador_id)
        metas = self.metas_repo.list_by_colaborador(colaborador_id)
        feedbacks = self.feedbacks_repo.list_by_colaborador(colaborador_id)
        perfil_atual = self.perfis_repo.get_ultimo_by_colaborador_id(colaborador_id)

        # Load all competencies to have a reliable mapping
        competencias = {c.id: c for c in self.competencias_repo.list()}

        notas_tecnicas = []
        notas_comportamentais = []

        for avaliacao in avaliacoes:
            for item in avaliacao.itens:
                comp = item.competencia or competencias.get(item.competencia_id)
                if comp:
                    tipo = comp.tipo.value if isinstance(comp.tipo, TipoCompetencia) else str(comp.tipo)
                    tipo = tipo.upper()
                    if tipo == "TECNICA":
                        notas_tecnicas.append(item.nota)
                    elif tipo in ("COMPORTAMENTAL", "LIDERANCA"):
                        notas_comportamentais.append(item.nota)

        # Pre-populate competencia on items for serializing
        for avaliacao in avaliacoes:
            for item in avaliacao.itens:
                if not item.competencia:
                    item.competencia = competencias.get(item.competencia_id)

        return {
            "colaborador": colaborador,
            "indicadores": {
                "media_tecnica": self._media(notas_tecnicas),
                "media_comportamental": self._media(notas_comportamentais),
                "metas_concluidas": len([m for m in metas if m.status == StatusMeta.CONCLUIDA]),
                "metas_atrasadas": len([m for m in metas if m.status == StatusMeta.ATRASADA]),
                "feedbacks_recebidos": len(feedbacks),
                "perfil_atual": perfil_atual,
            },
            "avaliacoes": avaliacoes,
            "metas": metas,
            "feedbacks": feedbacks,
        }

    def _media(self, notas: list[int]) -> float:
        if not notas:
            return 0.0
        return round(sum(notas) / len(notas), 2)
