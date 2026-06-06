from datetime import date, datetime
from typing import List

from application.errors import NotFoundError
from application.ports.avaliacao_repository import AvaliacaoRepository
from application.ports.colaborador_repository import ColaboradorRepository
from application.ports.competencia_repository import CompetenciaRepository
from application.ports.feedback_repository import FeedbackRepository
from application.ports.meta_repository import MetaRepository
from application.ports.perfil_talento_repository import PerfilTalentoRepository
from domain.enums.status_meta import StatusMeta
from domain.enums.tipo_competencia import TipoCompetencia
from application.security.access_scope_service import AccessScopeService


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

    def _media(self, notas: List[int]) -> float:
        if not notas:
            return 0.0
        return round(sum(notas) / len(notas), 2)


class ConsultarEvolucaoColaboradorUC:
    def __init__(self, uow):
        self.uow = uow

    def execute(self, colaborador_id: int, current_user: dict) -> dict:
        colaborador = self.uow.colaboradores.get_by_id(colaborador_id)
        if not colaborador:
            raise NotFoundError("Colaborador nao encontrado.")

        # Realizar validação de escopo conforme exigido
        AccessScopeService.ensure_can_access_colaborador(current_user, colaborador)

        # 1. Perfil de Talento mais recente
        perfil_atual = self.uow.perfis_talento.get_ultimo_by_colaborador_id(colaborador_id)

        # 2. Avaliações
        avaliacoes = self.uow.avaliacoes.list_by_colaborador(colaborador_id)

        # 3. Metas
        metas = self.uow.metas.list_by_colaborador(colaborador_id)

        # 4. Feedbacks
        feedbacks = self.uow.feedbacks.list_by_colaborador(colaborador_id)

        # 5. PDIs
        pdis = self.uow.pdis.list_by_colaborador_id(colaborador_id)

        # 6. Reconhecimentos
        reconhecimentos = self.uow.reconhecimentos.list_by_colaborador_id(colaborador_id)

        # Calcular notas de competências (mesma lógica herdada do VisualizarEvolucaoColaboradorUC)
        competencias = {c.id: c for c in self.uow.competencias.list()}
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

        # Pre-populate competencia nos itens de avaliacao
        for avaliacao in avaliacoes:
            for item in avaliacao.itens:
                if not item.competencia:
                    item.competencia = competencias.get(item.competencia_id)

        # Helper para obter o valor string de enums
        def _get_val(enum_attr):
            return enum_attr.value if hasattr(enum_attr, "value") else str(enum_attr)

        # Filtrar reconhecimentos ativos
        reconhecimentos_ativos = [r for r in reconhecimentos if r.ativo]

        return {
            "colaborador": colaborador,
            "perfil_atual": perfil_atual,
            "indicadores": {
                "total_avaliacoes": len(avaliacoes),
                "total_metas": len(metas),
                "metas_concluidas": len([m for m in metas if _get_val(m.status) == "CONCLUIDA"]),
                "metas_atrasadas": len([m for m in metas if _get_val(m.status) == "ATRASADA"]),
                "total_feedbacks": len(feedbacks),
                "pdis_ativos": len([p for p in pdis if _get_val(p.status) == "ATIVO"]),
                "reconhecimentos": len(reconhecimentos_ativos),
                # Chaves legadas para compatibilidade
                "media_tecnica": self._media(notas_tecnicas),
                "media_comportamental": self._media(notas_comportamentais),
                "perfil_atual": perfil_atual,
            },
            "ultimas_avaliacoes": [
                {
                    "id": a.id,
                    "tipo": a.tipo,
                    "data_avaliacao": a.data_avaliacao or a.criado_em,
                    "observacao_geral": a.observacao_geral
                }
                for a in sorted(avaliacoes, key=lambda x: x.data_avaliacao or x.criado_em or datetime.min, reverse=True)[:5]
            ],
            "metas": [
                {
                    "id": m.id,
                    "titulo": m.titulo,
                    "status": m.status,
                    "prioridade": m.prioridade,
                    "prazo": m.prazo
                }
                for m in sorted(metas, key=lambda x: x.prazo or date.min)
            ],
            "feedbacks": [
                {
                    "id": f.id,
                    "contexto": f.contexto,
                    "ponto_positivo": f.ponto_positivo,
                    "ponto_melhoria": f.ponto_melhoria,
                    "acao_recomendada": f.acao_recomendada,
                    "data_feedback": f.data_feedback or f.criado_em
                }
                for f in sorted(feedbacks, key=lambda x: x.data_feedback or x.criado_em or datetime.min, reverse=True)[:5]
            ],
            "pdis": [
                {
                    "id": p.id,
                    "titulo": p.titulo,
                    "status": p.status,
                    "origem": p.origem,
                    "data_inicio": p.data_inicio,
                    "data_fim": p.data_fim
                }
                for p in sorted(pdis, key=lambda x: x.criado_em or datetime.min, reverse=True)
            ],
            "reconhecimentos": [
                {
                    "id": r.id,
                    "tipo": r.tipo,
                    "descricao": r.descricao,
                    "evidencia": r.evidencia,
                    "data_reconhecimento": r.data_reconhecimento or r.criado_em,
                    "ativo": r.ativo
                }
                for r in sorted(reconhecimentos_ativos, key=lambda x: x.data_reconhecimento or x.criado_em or datetime.min, reverse=True)[:5]
            ],
            # Chaves legadas para compatibilidade
            "avaliacoes": avaliacoes,
        }

    def _media(self, notas: List[int]) -> float:
        if not notas:
            return 0.0
        return round(sum(notas) / len(notas), 2)
