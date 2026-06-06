from application.dtos.execucao_agente_dto import RegistrarExecucaoAgenteDTO
from application.ports.execucao_agente_repository import ExecucaoAgenteRepository
from domain.entities.execucao_agente import ExecucaoAgente


class RegistrarExecucaoAgenteUC:
    def __init__(self, repository: ExecucaoAgenteRepository):
        self.repository = repository

    def execute(self, dto: RegistrarExecucaoAgenteDTO) -> ExecucaoAgente:
        execucao = ExecucaoAgente(
            agente_nome=dto.agente_nome,
            entidade_tipo=dto.entidade_tipo,
            entidade_id=dto.entidade_id,
            entrada=dto.entrada,
            saida=dto.saida,
            status=dto.status,
            erro=dto.erro,
        )
        return self.repository.add(execucao)
