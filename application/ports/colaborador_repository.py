from abc import abstractmethod

from application.ports.base_repository import ReadRepository
from domain.entities.colaborador import Colaborador


class ColaboradorRepository(ReadRepository):
    @abstractmethod
    def get_by_matricula(self, matricula: str) -> Colaborador | None:
        pass

    @abstractmethod
    def add(self, colaborador: Colaborador) -> Colaborador:
        pass

    @abstractmethod
    def list(self) -> list[Colaborador]:
        pass

    @abstractmethod
    def save(self, colaborador: Colaborador) -> None:
        pass
