from abc import abstractmethod
from typing import List

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
    def list(self) -> List[Colaborador]:
        pass

    @abstractmethod
    def list_by_setor_id(self, setor_id: int) -> List[Colaborador]:
        pass

    @abstractmethod
    def save(self, colaborador: Colaborador) -> None:
        pass
