from app.models import (
    Avaliacao,
    Colaborador,
    Competencia,
    ExecucaoAgente,
    Feedback,
    Funcao,
    Meta,
    PerfilTalento,
    Setor,
    Usuario,
)
from app.repositories.base_repository import BaseRepository


class UsuarioRepository(BaseRepository):
    model = Usuario

    def get_by_email(self, email: str):
        return Usuario.query.filter_by(email=email).first()


class SetorRepository(BaseRepository):
    model = Setor


class FuncaoRepository(BaseRepository):
    model = Funcao


class ColaboradorRepository(BaseRepository):
    model = Colaborador

    def get_by_matricula(self, matricula: str):
        return Colaborador.query.filter_by(matricula=matricula).first()

    def get_by_email(self, email: str):
        return Colaborador.query.filter_by(email=email).first()


class CompetenciaRepository(BaseRepository):
    model = Competencia


class AvaliacaoRepository(BaseRepository):
    model = Avaliacao

    def list_by_colaborador(self, colaborador_id: int):
        return (
            Avaliacao.query.filter_by(colaborador_id=colaborador_id)
            .order_by(Avaliacao.data_avaliacao.desc())
            .all()
        )


class PerfilTalentoRepository(BaseRepository):
    model = PerfilTalento

    def get_atual_by_colaborador(self, colaborador_id: int):
        return (
            PerfilTalento.query.filter_by(colaborador_id=colaborador_id)
            .order_by(PerfilTalento.criado_em.desc())
            .first()
        )


class MetaRepository(BaseRepository):
    model = Meta

    def list_by_colaborador(self, colaborador_id: int):
        return Meta.query.filter_by(colaborador_id=colaborador_id).order_by(Meta.prazo.asc()).all()


class FeedbackRepository(BaseRepository):
    model = Feedback

    def list_by_colaborador(self, colaborador_id: int):
        return (
            Feedback.query.filter_by(colaborador_id=colaborador_id)
            .order_by(Feedback.data_feedback.desc())
            .all()
        )


class ExecucaoAgenteRepository(BaseRepository):
    model = ExecucaoAgente
