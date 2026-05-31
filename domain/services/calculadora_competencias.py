from dataclasses import dataclass

from domain.entities.avaliacao import Avaliacao
from domain.entities.competencia import Competencia
from domain.enums.tipo_competencia import TipoCompetencia


@dataclass(slots=True)
class ResultadoCompetencias:
    media_tecnica: float
    media_comportamental: float
    media_lideranca: float
    media_organizacional: float
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
        organizacional = []
        todas = []

        for item in avaliacao.itens:
            competencia = competencias.get(item.competencia_id)
            if competencia is None:
                raise ValueError(f"competencia {item.competencia_id} not found")

            # Peso nulo ou <= 0 assume 1.0
            peso = float(competencia.peso) if (competencia.peso is not None and competencia.peso > 0) else 1.0
            nota = float(item.nota)
            
            par = (nota, peso)
            todas.append(par)

            tipo_str = (
                competencia.tipo.value
                if isinstance(competencia.tipo, TipoCompetencia)
                else str(competencia.tipo)
            ).upper()

            if tipo_str == "TECNICA":
                tecnicas.append(par)
            elif tipo_str == "COMPORTAMENTAL":
                comportamentais.append(par)
            elif tipo_str == "LIDERANCA":
                lideranca.append(par)
            elif tipo_str == "ORGANIZACIONAL":
                organizacional.append(par)

        return ResultadoCompetencias(
            media_tecnica=self._media_ponderada(tecnicas),
            media_comportamental=self._media_ponderada(comportamentais),
            media_lideranca=self._media_ponderada(lideranca),
            media_organizacional=self._media_ponderada(organizacional),
            media_geral=self._media_ponderada(todas),
        )

    def _media_ponderada(self, itens: list[tuple[float, float]]) -> float:
        if not itens:
            return 0.0
        soma_ponderada = sum(nota * peso for nota, peso in itens)
        soma_pesos = sum(peso for _, peso in itens)
        if soma_pesos <= 0:
            return 0.0
        return round(soma_ponderada / soma_pesos, 2)
