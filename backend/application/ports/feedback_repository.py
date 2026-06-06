from abc import ABC, abstractmethod


class FeedbackRepository(ABC):
    @abstractmethod
    def add(self, feedback):
        pass

    @abstractmethod
    def list_by_colaborador(self, colaborador_id: int):
        pass
