from datetime import date, timedelta
from decimal import Decimal

from domain.entities.avaliacao import Avaliacao
from domain.entities.competencia import Competencia
from domain.entities.item_avaliacao import ItemAvaliacao
from domain.enums.tipo_avaliacao import TipoAvaliacao
from domain.enums.tipo_competencia import TipoCompetencia
from domain.services.calculadora_competencias import CalculadoraCompetencias
from domain.services.classificador_talento import ClassificadorTalento


class AgenteAvaliador:
    nome = "Agente Avaliador"

    def __init__(self, calculadora: CalculadoraCompetencias | None = None):
        self.calculadora = calculadora or CalculadoraCompetencias()

    def analisar(self, colaborador, avaliacao) -> dict:
        avaliacao_dominio, competencias = self._to_domain(avaliacao)
        resultado = self.calculadora.calcular(avaliacao_dominio, competencias)
        pontos_fortes, pontos_melhoria = self._pontos(avaliacao.itens)

        return {
            "colaborador_id": colaborador.id,
            "colaborador": colaborador.nome,
            "nivel_tecnico": self._nivel(resultado.media_tecnica),
            "nivel_comportamental": self._nivel(resultado.media_comportamental),
            "media_tecnica": resultado.media_tecnica,
            "media_comportamental": resultado.media_comportamental,
            "media_lideranca": resultado.media_lideranca,
            "media_geral": resultado.media_geral,
            "pontos_fortes": pontos_fortes or ["Entrega consistente"],
            "pontos_melhoria": pontos_melhoria or ["Manter evolucao continua"],
            "resumo": (
                f"{colaborador.nome} apresenta nivel tecnico {self._nivel(resultado.media_tecnica).lower()} "
                f"e nivel comportamental {self._nivel(resultado.media_comportamental).lower()}."
            ),
        }

    def _to_domain(self, avaliacao) -> tuple[Avaliacao, dict[int, Competencia]]:
        avaliacao_dominio = Avaliacao(
            colaborador_id=avaliacao.colaborador_id,
            avaliador_id=avaliacao.avaliador_id,
            tipo=TipoAvaliacao(avaliacao.tipo),
            observacao_geral=avaliacao.observacao_geral,
            itens=[
                ItemAvaliacao(
                    competencia_id=item.competencia_id,
                    nota=item.nota,
                    comentario=item.comentario,
                    id=item.id,
                )
                for item in avaliacao.itens
            ],
        )
        competencias = {
            item.competencia_id: Competencia(
                id=item.competencia.id,
                nome=item.competencia.nome,
                tipo=TipoCompetencia(item.competencia.tipo),
                descricao=item.competencia.descricao,
                peso=Decimal(item.competencia.peso),
                ativo=item.competencia.ativo,
                criado_em=item.competencia.criado_em,
            )
            for item in avaliacao.itens
        }
        return avaliacao_dominio, competencias

    def _pontos(self, itens) -> tuple[list[str], list[str]]:
        pontos_fortes = []
        pontos_melhoria = []

        for item in itens:
            if item.nota >= 4:
                pontos_fortes.append(item.competencia.nome)
            elif item.nota <= 2:
                pontos_melhoria.append(item.competencia.nome)

        return puntos_fortes, pontos_melhoria

    def _nivel(self, media: float) -> str:
        if media >= 4:
            return "ALTO"
        if media >= 3:
            return "MEDIO"
        if media > 0:
            return "BAIXO"
        return "NAO_AVALIADO"


class AgentePerfilador:
    nome = "Agente Perfilador"

    def __init__(self, classificador: ClassificadorTalento | None = None):
        self.classificador = classificador or ClassificadorTalento()

    def classificar(self, analise: dict) -> dict:
        from domain.services.calculadora_competencias import ResultadoCompetencias

        perfil = self.classificador.classificar(
            colaborador_id=analise["colaborador_id"],
            resultado=ResultadoCompetencias(
                media_tecnica=analise["media_tecnica"],
                media_comportamental=analise["media_comportamental"],
                media_lideranca=analise["media_lideranca"],
                media_geral=analise["media_geral"],
            ),
        )

        return {
            "classificacao": perfil.classificacao.value,
            "potencial_lideranca": perfil.potencial_lideranca,
            "resumo": perfil.resumo,
            "nivel_tecnico": perfil.nivel_tecnico,
            "nivel_comportamental": perfil.nivel_comportamental,
            "pontos_fortes": perfil.pontos_fortes or analise["pontos_fortes"],
            "pontos_melhoria": perfil.pontos_melhoria or analise["pontos_melhoria"],
            "recomendacoes": perfil.recomendacoes,
        }


class AgenteGeradorMetas:
    nome = "Agente Gerador de Metas"

    def sugerir(self, perfil: dict) -> list[dict]:
        metas = []
        prazo_base = date.today()

        for index, ponto in enumerate(perfil["pontos_melhoria"][:2], start=1):
            metas.append(
                {
                    "titulo": f"Desenvolver {ponto.lower()}",
                    "descricao": f"Executar acoes praticas para evoluir em {ponto.lower()}.",
                    "indicador": "Evidencias registradas semanalmente",
                    "prazo": prazo_base + timedelta(days=60 + (index - 1) * 30),
                    "prioridade": "ALTA" if index == 1 else "MEDIA",
                    "status": "PENDENTE",
                    "origem": "AGENTE_IA",
                }
            )

        return metas


class AgenteFeedback:
    nome = "Agente Feedback"

    def estruturar(self, observacao: str) -> dict:
        observacao = observacao.strip()
        if not observacao:
            raise ValueError("observacao is required")

        return {
            "contexto": observacao,
            "ponto_positivo": "Ha aspectos positivos observados na atuacao do colaborador.",
            "ponto_melhoria": "Identificar e comunicar risks ou dificuldades com antecedencia.",
            "acao_recomendada": (
                "Registrar a situacao observada, alinhar expectativa com o lider "
                "e acompanhar a evolucao no proximo ciclo."
            ),
            "tom": "CONSTRUTIVO",
        }
