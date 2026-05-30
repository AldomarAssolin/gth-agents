from dataclasses import dataclass

from domain.entities.avaliacao import Avaliacao
from domain.entities.competencia import Competencia
from domain.enums.tipo_competencia import TipoCompetencia


@dataclass(slots=True)
class ResultadoCompetencias:
    media_tecnica: float
    media_comportamental: float
    media_lideranca: float
    media_geral: float


class CalculadoraCompetencias:
    def calcular(
        self,
        avaliacao: Avaliacao,
        competencias: dict[int, Competencia],
    ) -> ResultadoCompetencias:
        avaliacao.validar()

        tecnicas = []
        comportamentais = []
        lideranca = []
        todas = []

        for item in avaliacao.itens:
            competencia = competencias.get(item.competencia_id)
            if competencia is None:
                raise ValueError(f"competencia {item.competencia_id} not found")

            nota_ponderada = float(item.nota) * float(competencia.peso)
            todas.append(nota_ponderada)

            if competencia.tipo == TipoCompetencia.TECNICA:
                tecnicas.append(nota_ponderada)
            elif competencia.tipo == TipoCompetencia.COMPORTAMENTAL:
                comportamentais.append(nota_ponderada)
            elif competencia.tipo == TipoCompetencia.LIDERANCA:
                lideranca.append(nota_ponderada)

        return ResultadoCompetencias(
            media_tecnica=self._media(tecnicas),
            media_comportamental=self._media(comportamentais),
            media_lideranca=self._media(lideranca),
            media_geral=self._media(todas),
        )

    def _media(self, notas: list[int]) -> float:
        if not notas:
            return 0.0
        return round(sum(notas) / len(notas), 2)
