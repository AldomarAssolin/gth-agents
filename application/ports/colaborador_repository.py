from abc import abstractmethod

from application.ports.base_repository import ReadRepository


class ColaboradorRepository(ReadRepository):
    @abstractmethod
    def get_by_matricula(self, matricula: str):
        pass

    @abstractmethod
    def add(self, colaborador):
        pass
