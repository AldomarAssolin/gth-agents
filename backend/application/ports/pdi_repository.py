from abc import ABC, abstractmethod
from domain.entities.pdi import PDI


class PDIRepository(ABC):
    @abstractmethod
    def add(self, pdi: PDI) -> PDI:
        pass

    @abstractmethod
    def save(self, pdi: PDI) -> None:
        pass

    @abstractmethod
    def get_by_id(self, pdi_id: int) -> PDI | None:
        pass

    @abstractmethod
    def list_all(self) -> list[PDI]:
        pass

    @abstractmethod
    def list_by_colaborador_id(self, colaborador_id: int) -> list[PDI]:
        pass
