from abc import ABC, abstractmethod


class MetaRepository(ABC):
    @abstractmethod
    def add(self, meta):
        pass

    @abstractmethod
    def list_by_colaborador(self, colaborador_id: int):
        pass
