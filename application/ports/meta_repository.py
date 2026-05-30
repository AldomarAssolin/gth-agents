from abc import ABC, abstractmethod


class MetaRepository(ABC):
    @abstractmethod
    def add(self, meta):
        pass
