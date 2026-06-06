from abc import ABC, abstractmethod
from domain.entities.acao_pdi import AcaoPDI


class AcaoPDIRepository(ABC):
    @abstractmethod
    def add(self, acao: AcaoPDI) -> AcaoPDI:
        pass

    @abstractmethod
    def save(self, acao: AcaoPDI) -> None:
        pass

    @abstractmethod
    def get_by_id(self, acao_id: int) -> AcaoPDI | None:
        pass

    @abstractmethod
    def list_by_pdi_id(self, pdi_id: int) -> list[AcaoPDI]:
        pass
