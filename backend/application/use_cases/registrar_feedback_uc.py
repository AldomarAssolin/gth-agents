from application.dtos.feedback_dto import RegistrarFeedbackDTO
from application.errors import NotFoundError, ValidationError
from application.ports.colaborador_repository import ColaboradorRepository
from application.ports.feedback_repository import FeedbackRepository
from application.ports.usuario_repository import UsuarioRepository
from domain.entities.feedback import Feedback


class RegistrarFeedbackUC:
    def __init__(
        self,
        colaboradores_repo: ColaboradorRepository,
        usuarios_repo: UsuarioRepository,
        feedbacks_repo: FeedbackRepository,
    ):
        self.colaboradores_repo = colaboradores_repo
        self.usuarios_repo = usuarios_repo
        self.feedbacks_repo = feedbacks_repo

    def execute(self, dto: RegistrarFeedbackDTO) -> Feedback:
        colaborador = self.colaboradores_repo.get_by_id(dto.colaborador_id)
        if not colaborador:
            raise NotFoundError("Colaborador nao encontrado.")

        autor = self.usuarios_repo.get_by_id(dto.autor_id)
        if not autor:
            raise NotFoundError("Autor do feedback nao encontrado.")

        if not dto.ponto_positivo:
            raise ValidationError("Ponto positivo e obrigatorio.")
        if not dto.acao_recomendada:
            raise ValidationError("Acao recomendada e obrigatoria.")

        feedback = Feedback(
            colaborador_id=dto.colaborador_id,
            autor_id=dto.autor_id,
            contexto=dto.contexto,
            ponto_positivo=dto.ponto_positivo,
            ponto_melhoria=dto.ponto_melhoria,
            acao_recomendada=dto.acao_recomendada,
            origem="MANUAL",
        )
        try:
            feedback.validar()
        except ValueError as exc:
            raise ValidationError(str(exc)) from exc

        return self.feedbacks_repo.add(feedback)
