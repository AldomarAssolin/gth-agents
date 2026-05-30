from application.ports.base_repository import ReadRepository
from abc import abstractmethod


class SetorRepository(ReadRepository):
    @abstractmethod
    def list(self):
        pass

    @abstractmethod
    def get_by_nome(self, nome: str):
        pass

    @abstractmethod
    def add(self, setor):
        pass
