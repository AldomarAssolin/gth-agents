from abc import ABC, abstractmethod
from domain.entities.execucao_agente import ExecucaoAgente


class ExecucaoAgenteRepository(ABC):
    @abstractmethod
    def add(self, execucao: ExecucaoAgente) -> ExecucaoAgente:
        pass
