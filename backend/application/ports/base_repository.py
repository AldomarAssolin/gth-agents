from abc import ABC, abstractmethod


class ReadRepository(ABC):
    @abstractmethod
    def get_by_id(self, entity_id: int):
        pass
