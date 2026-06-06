from enum import Enum


class StatusMeta(Enum):
    PENDENTE = "PENDENTE"
    EM_ANDAMENTO = "EM_ANDAMENTO"
    CONCLUIDA = "CONCLUIDA"
    ATRASADA = "ATRASADA"
    CANCELADA = "CANCELADA"
