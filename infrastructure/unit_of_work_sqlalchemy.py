from infrastructure.repositories.avaliacao_repository_sqlalchemy import AvaliacaoRepositorySQLAlchemy
from infrastructure.repositories.colaborador_repository_sqlalchemy import ColaboradorRepositorySQLAlchemy
from infrastructure.repositories.competencia_repository_sqlalchemy import CompetenciaRepositorySQLAlchemy
from infrastructure.repositories.feedback_repository_sqlalchemy import FeedbackRepositorySQLAlchemy
from infrastructure.repositories.funcao_repository_sqlalchemy import FuncaoRepositorySQLAlchemy
from infrastructure.repositories.meta_repository_sqlalchemy import MetaRepositorySQLAlchemy
from infrastructure.repositories.perfil_talento_repository_sqlalchemy import PerfilTalentoRepositorySQLAlchemy
from infrastructure.repositories.setor_repository_sqlalchemy import SetorRepositorySQLAlchemy
from infrastructure.repositories.usuario_repository_sqlalchemy import UsuarioRepositorySQLAlchemy
from infrastructure.repositories.execucao_agente_repository_sqlalchemy import ExecucaoAgenteRepositorySQLAlchemy


class UnitOfWorkSQLAlchemy:
    def __init__(self, session_factory):
        self.session_factory = session_factory
        self.session = None

    def __enter__(self):
        self.session = self.session_factory()
        self.colaboradores = ColaboradorRepositorySQLAlchemy(self.session)
        self.usuarios = UsuarioRepositorySQLAlchemy(self.session)
        self.setores = SetorRepositorySQLAlchemy(self.session)
        self.funcoes = FuncaoRepositorySQLAlchemy(self.session)
        self.competencias = CompetenciaRepositorySQLAlchemy(self.session)
        self.avaliacoes = AvaliacaoRepositorySQLAlchemy(self.session)
        self.perfis_talento = PerfilTalentoRepositorySQLAlchemy(self.session)
        self.metas = MetaRepositorySQLAlchemy(self.session)
        self.feedbacks = FeedbackRepositorySQLAlchemy(self.session)
        self.execucoes_agente = ExecucaoAgenteRepositorySQLAlchemy(self.session)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            if exc_type:
                self.rollback()
            else:
                self.commit()
        finally:
            self.close()

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()

    def close(self) -> None:
        self.session.close()
