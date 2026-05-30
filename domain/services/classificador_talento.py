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

        if tecnico >= 4 and comportamental >= 4 and lideranca >= 4:
            return ClassificacaoTalento.ALTA_PERFORMANCE
        if tecnico >= 4 and lideranca >= 3:
            return ClassificacaoTalento.POTENCIAL_LIDER
        if tecnico >= 4 and comportamental < 4:
            return ClassificacaoTalento.ESPECIALISTA_TECNICO
        if tecnico >= 3 and comportamental >= 3:
            return ClassificacaoTalento.TALENTO_EM_DESENVOLVIMENTO
        return ClassificacaoTalento.NECESSITA_DESENVOLVIMENTO

    def _nivel(self, media: float) -> str:
        if media >= 4:
            return "ALTO"
        if media >= 3:
            return "MEDIO"
        if media > 0:
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
        if resultado.media_tecnica >= 4:
            pontos.append("Boa competencia tecnica.")
        if resultado.media_comportamental >= 4:
            pontos.append("Bom comportamento organizacional.")
        if resultado.media_lideranca >= 4:
            pontos.append("Boa capacidade de lideranca.")
        return pontos

    def _identificar_pontos_melhoria(self, resultado: ResultadoCompetencias) -> list[str]:
        pontos = []
        if resultado.media_tecnica < 3:
            pontos.append("Desenvolver competencias tecnicas.")
        if resultado.media_comportamental < 3:
            pontos.append("Desenvolver competencias comportamentais.")
        if resultado.media_lideranca < 3:
            pontos.append("Desenvolver competencias de lideranca.")
        return pontos

    def recomendacoes(self, classificacao: ClassificacaoTalento) -> list[str]:
        recomendacoes = {
            ClassificacaoTalento.ALTA_PERFORMANCE: [
                "Criar desafios maiores",
                "Avaliar trilha de lideranca",
            ],
            ClassificacaoTalento.ESPECIALISTA_TECNICO: [
                "Atuar como referencia tecnica",
                "Mentorar colaboradores juniores",
            ],
            ClassificacaoTalento.POTENCIAL_LIDER: [
                "Participar de apoio a lideranca",
                "Conduzir pequenas iniciativas",
            ],
            ClassificacaoTalento.TALENTO_EM_DESENVOLVIMENTO: [
                "Definir metas de evolucao",
                "Acompanhar feedbacks periodicos",
            ],
            ClassificacaoTalento.NECESSITA_DESENVOLVIMENTO: [
                "Criar plano de acao imediato",
                "Aumentar acompanhamento do lider",
            ],
        }
        return recomendacoes[classificacao]
