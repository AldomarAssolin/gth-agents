from application.ports.base_repository import ReadRepository
from abc import abstractmethod


class CompetenciaRepository(ReadRepository):
    @abstractmethod
    def list(self):
        pass

    @abstractmethod
    def add(self, competencia):
        pass

    @abstractmethod
    def save(self, competencia) -> None:
        pass
