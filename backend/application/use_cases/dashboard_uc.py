from datetime import date, datetime
from typing import List

from application.errors import ForbiddenError
from domain.enums.status_meta import StatusMeta
from domain.enums.pdi_enums import StatusPDI


def _get_attr(obj, name):
    if isinstance(obj, dict):
        return obj.get(name)
    return getattr(obj, name, None)


class ConsultarDashboardMVP_UC:
    def __init__(self, uow):
        self.uow = uow

    def execute(self, current_user: dict | object) -> dict:
        perfil_val = _get_attr(current_user, "perfil")
        perfil = perfil_val.value if hasattr(perfil_val, "value") else str(perfil_val)
        perfil = perfil.upper()

        if perfil not in ("ADMIN", "RH", "LIDER"):
            raise ForbiddenError("Acesso negado.")

        if perfil == "LIDER":
            setor_id = _get_attr(current_user, "setor_id")
            if setor_id is None:
                raise ForbiddenError("Lider deve estar vinculado a um setor.")
            colaboradores = self.uow.colaboradores.list_by_setor_id(setor_id)
        else:
            colaboradores = self.uow.colaboradores.list()

        # Listas agregadas
        all_avaliacoes = []
        all_metas = []
        all_feedbacks = []
        all_pdis = []
        all_reconhecimentos = []
        perfis_talento_dict = {}

        # Mapeamento para evitar N+1 desnecessário se pudéssemos, mas para respeitar a estrutura de repositórios atual
        # fazemos a busca por colaborador.
        for colab in colaboradores:
            # 1. Avaliações
            all_avaliacoes.extend(self.uow.avaliacoes.list_by_colaborador(colab.id))

            # 2. Metas
            all_metas.extend(self.uow.metas.list_by_colaborador(colab.id))

            # 3. Feedbacks
            all_feedbacks.extend(self.uow.feedbacks.list_by_colaborador(colab.id))

            # 4. PDIs
            all_pdis.extend(self.uow.pdis.list_by_colaborador_id(colab.id))

            # 5. Reconhecimentos
            all_reconhecimentos.extend(self.uow.reconhecimentos.list_by_colaborador_id(colab.id))

            # 6. Perfil de Talento mais recente
            perfis_talento_dict[colab.id] = self.uow.perfis_talento.get_ultimo_by_colaborador_id(colab.id)

        # Helpers para ler valores de enums
        def _get_val(enum_attr):
            if enum_attr is None:
                return None
            return enum_attr.value if hasattr(enum_attr, "value") else str(enum_attr)

        # Contagens de Colaboradores
        ativos_count = 0
        inativos_count = 0
        afastados_count = 0
        desligados_count = 0

        for colab in colaboradores:
            status_str = _get_val(colab.status)
            if status_str == "ATIVO":
                ativos_count += 1
            elif status_str == "INATIVO":
                inativos_count += 1
            elif status_str == "AFASTADO":
                afastados_count += 1
            elif status_str == "DESLIGADO":
                desligados_count += 1

        # Contagens de Metas
        metas_pendentes = 0
        metas_em_andamento = 0
        metas_concluidas = 0
        metas_atrasadas = 0
        metas_canceladas = 0

        for meta in all_metas:
            status_str = _get_val(meta.status)
            if status_str == "PENDENTE":
                metas_pendentes += 1
            elif status_str == "EM_ANDAMENTO":
                metas_em_andamento += 1
            elif status_str == "CONCLUIDA":
                metas_concluidas += 1
            elif status_str == "ATRASADA":
                metas_atrasadas += 1
            elif status_str == "CANCELADA":
                metas_canceladas += 1

        # Contagens de PDIs
        pdi_rascunho = 0
        pdi_ativos = 0
        pdi_concluidos = 0
        pdi_cancelados = 0

        for pdi in all_pdis:
            status_str = _get_val(pdi.status)
            if status_str == "RASCUNHO":
                pdi_rascunho += 1
            elif status_str == "ATIVO":
                pdi_ativos += 1
            elif status_str == "CONCLUIDO":
                pdi_concluidos += 1
            elif status_str == "CANCELADO":
                pdi_cancelados += 1

        # Contagens de Reconhecimentos
        recs_ativos = [r for r in all_reconhecimentos if r.ativo]
        recs_cancelados = [r for r in all_reconhecimentos if not r.ativo]

        # Contagens de Perfis de Talento
        perfis_dist = {
            "ALTA_PERFORMANCE": 0,
            "POTENCIAL_LIDER": 0,
            "ESPECIALISTA_TECNICO": 0,
            "TALENTO_EM_DESENVOLVIMENTO": 0,
            "NECESSITA_DESENVOLVIMENTO": 0,
            "SEM_PERFIL": 0,
        }

        colabs_com_avaliacao_ids = {av.colaborador_id for av in all_avaliacoes}
        colaboradores_sem_avaliacao_count = 0
        colaboradores_sem_perfil_count = 0

        for colab in colaboradores:
            # Verificar avaliação
            if colab.id not in colabs_com_avaliacao_ids:
                colaboradores_sem_avaliacao_count += 1

            # Verificar perfil de talento
            perf = perfis_talento_dict.get(colab.id)
            if perf is None:
                colaboradores_sem_perfil_count += 1
                perfis_dist["SEM_PERFIL"] += 1
            else:
                classif = _get_val(perf.classificacao)
                if classif in perfis_dist:
                    perfis_dist[classif] += 1
                else:
                    # Fallback caso classificação não case perfeitamente com as sugeridas
                    perfis_dist["SEM_PERFIL"] += 1

        # Montagem dos últimos registros (máximo 5 itens)
        ultimas_avaliacoes = [
            {
                "id": av.id,
                "colaborador_id": av.colaborador_id,
                "tipo": av.tipo,
                "data_avaliacao": av.data_avaliacao or av.criado_em,
            }
            for av in sorted(all_avaliacoes, key=lambda x: x.data_avaliacao or x.criado_em or datetime.min, reverse=True)[:5]
        ]

        ultimos_feedbacks = [
            {
                "id": fb.id,
                "colaborador_id": fb.colaborador_id,
                "contexto": fb.contexto,
                "data_feedback": fb.data_feedback or fb.criado_em,
            }
            for fb in sorted(all_feedbacks, key=lambda x: x.data_feedback or x.criado_em or datetime.min, reverse=True)[:5]
        ]

        ultimos_reconhecimentos = [
            {
                "id": rec.id,
                "colaborador_id": rec.colaborador_id,
                "tipo": rec.tipo,
                "data_reconhecimento": rec.data_reconhecimento or rec.criado_em,
            }
            for rec in sorted(recs_ativos, key=lambda x: x.data_reconhecimento or x.criado_em or datetime.min, reverse=True)[:5]
        ]

        return {
            "resumo_geral": {
                "total_colaboradores": len(colaboradores),
                "colaboradores_ativos": ativos_count,
                "colaboradores_inativos": inativos_count,
                "total_avaliacoes": len(all_avaliacoes),
                "total_metas": len(all_metas),
                "total_feedbacks": len(all_feedbacks),
                "total_pdis": len(all_pdis),
                "total_reconhecimentos": len(all_reconhecimentos),
            },
            "colaboradores": {
                "ativos": ativos_count,
                "inativos": inativos_count,
                "afastados": afastados_count,
                "desligados": desligados_count,
            },
            "avaliacoes": {
                "total": len(all_avaliacoes),
                "ultimas": ultimas_avaliacoes,
            },
            "metas": {
                "total": len(all_metas),
                "pendentes": metas_pendentes,
                "em_andamento": metas_em_andamento,
                "concluidas": metas_concluidas,
                "atrasadas": metas_atrasadas,
                "canceladas": metas_canceladas,
            },
            "pdis": {
                "total": len(all_pdis),
                "rascunho": pdi_rascunho,
                "ativos": pdi_ativos,
                "concluidos": pdi_concluidos,
                "cancelados": pdi_cancelados,
            },
            "feedbacks": {
                "total": len(all_feedbacks),
                "ultimos": ultimos_feedbacks,
            },
            "reconhecimentos": {
                "total": len(all_reconhecimentos),
                "ativos": len(recs_ativos),
                "cancelados": len(recs_cancelados),
                "ultimos": ultimos_reconhecimentos,
            },
            "perfis_talento": perfis_dist,
            "alertas": {
                "metas_atrasadas": metas_atrasadas,
                "pdis_ativos": pdi_ativos,
                "colaboradores_sem_avaliacao": colaboradores_sem_avaliacao_count,
                "colaboradores_sem_perfil": colaboradores_sem_perfil_count,
            },
        }
