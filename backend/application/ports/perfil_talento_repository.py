from abc import ABC, abstractmethod


class PerfilTalentoRepository(ABC):
    @abstractmethod
    def add(self, perfil_talento):
        pass

    @abstractmethod
    def get_ultimo_by_colaborador_id(self, colaborador_id: int):
        pass
