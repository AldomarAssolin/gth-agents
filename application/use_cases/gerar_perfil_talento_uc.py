from application.errors import NotFoundError
from domain.services.calculadora_competencias import CalculadoraCompetencias
from domain.services.classificador_talento import ClassificadorTalento


class GerarPerfilTalentoUC:
    def __init__(self, colaboradores_repo, competencias_repo, perfis_talento_repo):
        self.colaboradores_repo = colaboradores_repo
        self.competencias_repo = competencias_repo
        self.perfis_talento_repo = perfis_talento_repo
        self.calculadora = CalculadoraCompetencias()
        self.classificador = ClassificadorTalento()

    def execute(self, avaliacao):
        colaborador = self.colaboradores_repo.get_by_id(avaliacao.colaborador_id)
        if not colaborador:
            raise NotFoundError("Colaborador nao encontrado.")

        competencias = {
            item.competencia_id: self.competencias_repo.get_by_id(item.competencia_id)
            for item in avaliacao.itens
        }
        resultado = self.calculadora.calcular(avaliacao, competencias)
        perfil = self.classificador.classificar(avaliacao.colaborador_id, resultado)
        return self.perfis_talento_repo.add(perfil)
