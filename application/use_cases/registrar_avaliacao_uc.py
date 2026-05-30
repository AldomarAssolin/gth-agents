from application.dtos.avaliacao_dto import RegistrarAvaliacaoDTO
from application.errors import NotFoundError, ValidationError
from application.ports.avaliacao_repository import AvaliacaoRepository
from application.ports.colaborador_repository import ColaboradorRepository
from application.ports.competencia_repository import CompetenciaRepository
from application.ports.perfil_talento_repository import PerfilTalentoRepository
from application.ports.usuario_repository import UsuarioRepository
from domain.entities.avaliacao import Avaliacao
from domain.entities.item_avaliacao import ItemAvaliacao
from domain.services.calculadora_competencias import CalculadoraCompetencias
from domain.services.classificador_talento import ClassificadorTalento
from domain.services.validador_avaliacao import ValidadorAvaliacao


class RegistrarAvaliacaoUC:
    def __init__(
        self,
        colaboradores_repo: ColaboradorRepository,
        usuarios_repo: UsuarioRepository,
        competencias_repo: CompetenciaRepository,
        avaliacoes_repo: AvaliacaoRepository,
        perfis_talento_repo: PerfilTalentoRepository,
    ):
        self.colaboradores_repo = colaboradores_repo
        self.usuarios_repo = usuarios_repo
        self.competencias_repo = competencias_repo
        self.avaliacoes_repo = avaliacoes_repo
        self.perfis_talento_repo = perfis_talento_repo
        self.validador = ValidadorAvaliacao()
        self.calculadora = CalculadoraCompetencias()
        self.classificador = ClassificadorTalento()

    def execute(self, dto: RegistrarAvaliacaoDTO):
        colaborador = self.colaboradores_repo.get_by_id(dto.colaborador_id)
        if not colaborador:
            raise NotFoundError("Colaborador nao encontrado.")
        if not colaborador.esta_ativo():
            raise ValidationError("Nao e possivel avaliar colaborador inativo.")

        avaliador = self.usuarios_repo.get_by_id(dto.avaliador_id)
        if not avaliador:
            raise NotFoundError("Avaliador nao encontrado.")
        if not avaliador.pode_avaliar():
            raise ValidationError("Usuario nao possui permissao para avaliar.")

        itens = [
            ItemAvaliacao(
                competencia_id=item.competencia_id,
                nota=item.nota,
                comentario=item.comentario,
            )
            for item in dto.itens
        ]
        avaliacao = Avaliacao(
            colaborador_id=dto.colaborador_id,
            avaliador_id=dto.avaliador_id,
            tipo=dto.tipo,
            observacao_geral=dto.observacao_geral,
            itens=itens,
        )

        try:
            self.validador.validar(avaliacao)
        except ValueError as exc:
            raise ValidationError(str(exc)) from exc

        competencias_por_id = {}
        for item in avaliacao.itens:
            competencia = self.competencias_repo.get_by_id(item.competencia_id)
            if not competencia:
                raise NotFoundError(f"Competencia {item.competencia_id} nao encontrada.")
            competencias_por_id[competencia.id] = competencia

        avaliacao_salva = self.avaliacoes_repo.add(avaliacao)
        try:
            resultado = self.calculadora.calcular(
                avaliacao=avaliacao_salva,
                competencias=competencias_por_id,
            )
            perfil = self.classificador.classificar(
                colaborador_id=dto.colaborador_id,
                resultado=resultado,
            )
        except ValueError as exc:
            raise ValidationError(str(exc)) from exc
        perfil_salvo = self.perfis_talento_repo.add(perfil)

        return {
            "avaliacao": avaliacao_salva,
            "perfil_talento": perfil_salvo,
            "resultado_competencias": resultado,
        }
