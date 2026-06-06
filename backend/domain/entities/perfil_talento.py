from dataclasses import dataclass, field
from datetime import datetime

from domain.enums.classificacao_talento import ClassificacaoTalento


@dataclass(slots=True)
class PerfilTalento:
    colaborador_id: int
    classificacao: ClassificacaoTalento
    resumo: str | None = None
    nivel_tecnico: str | None = None
    nivel_comportamental: str | None = None
    potencial_lideranca: str | None = None
    pontos_fortes: list[str] = field(default_factory=list)
    pontos_melhoria: list[str] = field(default_factory=list)
    recomendacoes: list[str] = field(default_factory=list)
    origem: str = "AGENTE_IA"
    id: int | None = None
    criado_em: datetime | None = None

    def eh_potencial_lider(self) -> bool:
        return self.classificacao == ClassificacaoTalento.POTENCIAL_LIDER

    def eh_alta_performance(self) -> bool:
        return self.classificacao == ClassificacaoTalento.ALTA_PERFORMANCE

    def necessita_desenvolvimento(self) -> bool:
        return self.classificacao == ClassificacaoTalento.NECESSITA_DESENVOLVIMENTO

    def adicionar_recomendacao(self, recomendacao: str) -> None:
        if recomendacao:
            self.recomendacoes.append(recomendacao)
