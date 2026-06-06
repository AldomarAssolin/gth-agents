from abc import ABC, abstractmethod
from domain.entities.reconhecimento import Reconhecimento


class ReconhecimentoRepository(ABC):
    @abstractmethod
    def add(self, reconhecimento: Reconhecimento) -> Reconhecimento:
        pass

    @abstractmethod
    def save(self, reconhecimento: Reconhecimento) -> Reconhecimento:
        pass

    @abstractmethod
    def get_by_id(self, reconhecimento_id: int) -> Reconhecimento | None:
        pass

    @abstractmethod
    def list_all(self) -> list[Reconhecimento]:
        pass

    @abstractmethod
    def list_by_colaborador_id(self, colaborador_id: int) -> list[Reconhecimento]:
        pass

    @abstractmethod
    def list_by_colaboradores_ids(self, colaboradores_ids: list[int]) -> list[Reconhecimento]:
        pass
