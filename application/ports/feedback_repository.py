from abc import ABC, abstractmethod


class FeedbackRepository(ABC):
    @abstractmethod
    def add(self, feedback):
        pass
