from sqlalchemy.orm import Session
from application.ports.execucao_agente_repository import ExecucaoAgenteRepository
from domain.entities.execucao_agente import ExecucaoAgente
from infrastructure.database.models.execucao_agente_model import ExecucaoAgenteModel
from infrastructure.mappers.execucao_agente_mapper import ExecucaoAgenteMapper


class ExecucaoAgenteRepositorySQLAlchemy(ExecucaoAgenteRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, execucao: ExecucaoAgente) -> ExecucaoAgente:
        model = ExecucaoAgenteMapper.to_model(execucao)
        self.session.add(model)
        self.session.flush()
        return ExecucaoAgenteMapper.to_domain(model)
