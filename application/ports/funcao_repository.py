from application.ports.base_repository import ReadRepository
from abc import abstractmethod


class FuncaoRepository(ReadRepository):
    @abstractmethod
    def list(self):
        pass

    @abstractmethod
    def get_by_nome(self, nome: str):
        pass

    @abstractmethod
    def add(self, funcao):
        pass

    @abstractmethod
    def save(self, funcao) -> None:
        pass
