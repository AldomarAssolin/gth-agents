from app.models import Colaborador
from app.repositories.domain_repositories import (
    AvaliacaoRepository,
    FeedbackRepository,
    MetaRepository,
    PerfilTalentoRepository,
)


class EvolucaoService:
    def __init__(self):
        self.avaliacoes = AvaliacaoRepository()
        self.feedbacks = FeedbackRepository()
        self.metas = MetaRepository()
        self.perfis = PerfilTalentoRepository()

    def get_colaborador_evolucao(self, colaborador: Colaborador) -> dict:
        avaliacoes = self.avaliacoes.list_by_colaborador(colaborador.id)
        metas = self.metas.list_by_colaborador(colaborador.id)
        feedbacks = self.feedbacks.list_by_colaborador(colaborador.id)
        perfil_atual = self.perfis.get_atual_by_colaborador(colaborador.id)

        notas_tecnicas = []
        notas_comportamentais = []

        for avaliacao in avaliacoes:
            for item in avaliacao.itens:
                tipo = item.competencia.tipo.upper()
                if tipo == "TECNICA":
                    notas_tecnicas.append(item.nota)
                elif tipo in ("COMPORTAMENTAL", "LIDERANCA"):
                    notas_comportamentais.append(item.nota)

        return {
            "colaborador": colaborador.to_dict(),
            "indicadores": {
                "media_tecnica": self._media(notas_tecnicas),
                "media_comportamental": self._media(notas_comportamentais),
                "metas_concluidas": len([meta for meta in metas if meta.status == "CONCLUIDA"]),
                "metas_atrasadas": len([meta for meta in metas if meta.status == "ATRASADA"]),
                "feedbacks_recebidos": len(feedbacks),
                "perfil_atual": perfil_atual.to_dict() if perfil_atual else None,
            },
            "avaliacoes": [avaliacao.to_dict() for avaliacao in avaliacoes],
            "metas": [meta.to_dict() for meta in metas],
            "feedbacks": [feedback.to_dict() for feedback in feedbacks],
        }

    def _media(self, notas: list[int]) -> float:
        if not notas:
            return 0.0
        return round(sum(notas) / len(notas), 2)
