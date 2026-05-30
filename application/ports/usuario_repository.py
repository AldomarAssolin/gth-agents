from abc import abstractmethod

from application.ports.base_repository import ReadRepository


class UsuarioRepository(ReadRepository):
    @abstractmethod
    def list(self):
        pass

    @abstractmethod
    def add(self, usuario):
        pass

    @abstractmethod
    def get_by_email(self, email: str):
        pass

    @abstractmethod
    def save(self, usuario) -> None:
        pass
