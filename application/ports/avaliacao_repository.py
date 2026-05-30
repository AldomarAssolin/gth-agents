from abc import ABC, abstractmethod


class AvaliacaoRepository(ABC):
    @abstractmethod
    def add(self, avaliacao):
        pass

    @abstractmethod
    def get_by_id(self, avaliacao_id: int):
        pass
