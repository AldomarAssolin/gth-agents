from domain.entities.perfil_talento import PerfilTalento
from domain.enums.classificacao_talento import ClassificacaoTalento
from domain.services.calculadora_competencias import ResultadoCompetencias


class ClassificadorTalento:
    def classificar(
        self,
        colaborador_id: int,
        resultado: ResultadoCompetencias,
    ) -> PerfilTalento:
        classificacao = self._definir_classificacao(resultado)
        return PerfilTalento(
            colaborador_id=colaborador_id,
            classificacao=classificacao,
            resumo=self._gerar_resumo(classificacao, resultado),
            nivel_tecnico=self._nivel(resultado.media_tecnica),
            nivel_comportamental=self._nivel(resultado.media_comportamental),
            potencial_lideranca=self._nivel(resultado.media_lideranca),
            pontos_fortes=self._identificar_pontos_fortes(resultado),
            pontos_melhoria=self._identificar_pontos_melhoria(resultado),
            recomendacoes=self.recomendacoes(classificacao),
            origem="REGRA_DOMINIO",
        )

    def _definir_classificacao(self, resultado: ResultadoCompetencias) -> ClassificacaoTalento:
        tecnico = resultado.media_tecnica
        comportamental = resultado.media_comportamental
        lideranca = resultado.media_lideranca
        geral = resultado.media_geral

        if tecnico >= 4.0 and comportamental >= 4.0 and (lideranca >= 4.0 or lideranca == 0.0):
            return ClassificacaoTalento.ALTA_PERFORMANCE

        if (tecnico >= 3.0 and comportamental >= 4.0 and lideranca >= 4.0) or (tecnico >= 4.0 and lideranca >= 4.0):
            return ClassificacaoTalento.POTENCIAL_LIDER

        if (tecnico >= 4.0 and comportamental < 4.0) or (tecnico >= 4.0 and lideranca < 4.0):
            return ClassificacaoTalento.ESPECIALISTA_TECNICO

        if geral >= 3.0 and (tecnico >= 3.0 or comportamental >= 3.0):
            return ClassificacaoTalento.TALENTO_EM_DESENVOLVIMENTO

        return ClassificacaoTalento.NECESSITA_DESENVOLVIMENTO

    def _nivel(self, media: float) -> str:
        if media >= 4.0:
            return "ALTO"
        if media >= 3.0:
            return "MEDIO"
        if media > 0.0:
            return "BAIXO"
        return "NAO_AVALIADO"

    def _gerar_resumo(
        self,
        classificacao: ClassificacaoTalento,
        resultado: ResultadoCompetencias,
    ) -> str:
        return (
            f"Perfil classificado como {classificacao.value}. "
            f"Media tecnica: {resultado.media_tecnica}, "
            f"media comportamental: {resultado.media_comportamental}, "
            f"media de lideranca: {resultado.media_lideranca}."
        )

    def _identificar_pontos_fortes(self, resultado: ResultadoCompetencias) -> list[str]:
        pontos = []
        if resultado.media_tecnica >= 4.0:
            pontos.append("Boa competência técnica.")
        if resultado.media_comportamental >= 4.0:
            pontos.append("Bom comportamento organizacional.")
        if resultado.media_lideranca >= 4.0:
            pontos.append("Boa capacidade de liderança.")
        if resultado.media_organizacional >= 4.0:
            pontos.append("Boa aderência aos valores e práticas organizacionais.")
        return pontos

    def _identificar_pontos_melhoria(self, resultado: ResultadoCompetencias) -> list[str]:
        pontos = []
        if 0.0 < resultado.media_tecnica < 3.0:
            pontos.append("Desenvolver competências técnicas.")
        if 0.0 < resultado.media_comportamental < 3.0:
            pontos.append("Desenvolver competências comportamentais.")
        if 0.0 < resultado.media_lideranca < 3.0:
            pontos.append("Desenvolver competências de liderança.")
        if 0.0 < resultado.media_organizacional < 3.0:
            pontos.append("Desenvolver aderência organizacional.")
        return pontos

    def recomendacoes(self, classificacao: ClassificacaoTalento) -> list[str]:
        recomendacoes = {
            ClassificacaoTalento.ALTA_PERFORMANCE: [
                "Manter acompanhamento e oferecer desafios maiores.",
                "Considerar para projetos estratégicos ou mentoria.",
            ],
            ClassificacaoTalento.ESPECIALISTA_TECNICO: [
                "Utilizar como referência técnica.",
                "Desenvolver comunicação, influência e apoio a colegas.",
            ],
            ClassificacaoTalento.POTENCIAL_LIDER: [
                "Incluir em atividades de apoio à liderança.",
                "Oferecer mentoria com liderança experiente.",
            ],
            ClassificacaoTalento.TALENTO_EM_DESENVOLVIMENTO: [
                "Criar plano de desenvolvimento individual.",
                "Acompanhar evolução por metas e feedbacks periódicos.",
            ],
            ClassificacaoTalento.NECESSITA_DESENVOLVIMENTO: [
                "Priorizar treinamento e acompanhamento próximo.",
                "Definir metas de curto prazo para evolução.",
            ],
        }
        return recomendacoes[classificacao]
