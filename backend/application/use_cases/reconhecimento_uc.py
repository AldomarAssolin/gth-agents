from datetime import datetime, timezone
from domain.entities.reconhecimento import Reconhecimento
from domain.enums.tipo_reconhecimento import TipoReconhecimento
from application.dtos.reconhecimento_dto import (
    CriarReconhecimentoDTO,
    CancelarReconhecimentoDTO,
)
from application.errors import NotFoundError, ValidationError, ForbiddenError
from application.security.access_scope_service import AccessScopeService


class CriarReconhecimentoUC:
    def __init__(self, uow):
        self.uow = uow

    def execute(self, dto: CriarReconhecimentoDTO, current_user: dict) -> Reconhecimento:
        perfil = current_user.get("perfil")
        if perfil == "COLABORADOR":
            raise ForbiddenError("Colaboradores nao podem registrar reconhecimentos.")

        colaborador = self.uow.colaboradores.get_by_id(dto.colaborador_id)
        if not colaborador:
            raise NotFoundError("Colaborador nao encontrado.")

        registrador = self.uow.usuarios.get_by_id(dto.registrado_por_id)
        if not registrador:
            raise NotFoundError("Usuario registrador nao encontrado.")

        AccessScopeService.ensure_can_manage_colaborador(current_user, colaborador)

        try:
            tipo = TipoReconhecimento(dto.tipo)
        except ValueError:
            raise ValidationError("Tipo de reconhecimento invalido.")

        reconhecimento = Reconhecimento(
            colaborador_id=dto.colaborador_id,
            tipo=tipo,
            descricao=dto.descricao,
            evidencia=dto.evidencia,
            registrado_por_id=dto.registrado_por_id,
            data_reconhecimento=datetime.now(timezone.utc),
            ativo=True,
            criado_em=datetime.now(timezone.utc),
        )

        try:
            reconhecimento.validar()
        except ValueError as exc:
            raise ValidationError(str(exc))

        return self.uow.reconhecimentos.add(reconhecimento)


class ListarReconhecimentosUC:
    def __init__(self, uow):
        self.uow = uow

    def execute(self, current_user: dict) -> list[Reconhecimento]:
        perfil = current_user.get("perfil")

        if perfil in ("ADMIN", "RH"):
            return self.uow.reconhecimentos.list_all()

        if perfil == "LIDER":
            setor_id = current_user.get("setor_id")
            if setor_id is None:
                raise ForbiddenError("Lider nao possui setor vinculado.")
            colaboradores = self.uow.colaboradores.list_by_setor_id(setor_id)
            colab_ids = [c.id for c in colaboradores]
            return self.uow.reconhecimentos.list_by_colaboradores_ids(colab_ids)

        if perfil == "COLABORADOR":
            colaborador_id = current_user.get("colaborador_id")
            if colaborador_id is None:
                raise ForbiddenError("Colaborador nao possui id de colaborador vinculado.")
            return self.uow.reconhecimentos.list_by_colaborador_id(colaborador_id)

        raise ForbiddenError("Perfil desconhecido.")


class BuscarReconhecimentoUC:
    def __init__(self, uow):
        self.uow = uow

    def execute(self, reconhecimento_id: int, current_user: dict) -> Reconhecimento:
        reconhecimento = self.uow.reconhecimentos.get_by_id(reconhecimento_id)
        if not reconhecimento:
            raise NotFoundError("Reconhecimento nao encontrado.")

        colaborador = self.uow.colaboradores.get_by_id(reconhecimento.colaborador_id)
        if not colaborador:
            raise NotFoundError("Colaborador nao encontrado.")

        AccessScopeService.ensure_can_access_colaborador(current_user, colaborador)

        return reconhecimento


class ListarReconhecimentosPorColaboradorUC:
    def __init__(self, uow):
        self.uow = uow

    def execute(self, colaborador_id: int, current_user: dict) -> list[Reconhecimento]:
        colaborador = self.uow.colaboradores.get_by_id(colaborador_id)
        if not colaborador:
            raise NotFoundError("Colaborador nao encontrado.")

        AccessScopeService.ensure_can_access_colaborador(current_user, colaborador)

        return self.uow.reconhecimentos.list_by_colaborador_id(colaborador_id)


class CancelarReconhecimentoUC:
    def __init__(self, uow):
        self.uow = uow

    def execute(self, dto: CancelarReconhecimentoDTO, current_user: dict) -> Reconhecimento:
        perfil = current_user.get("perfil")
        if perfil == "COLABORADOR":
            raise ForbiddenError("Colaboradores nao podem cancelar reconhecimentos.")

        reconhecimento = self.uow.reconhecimentos.get_by_id(dto.reconhecimento_id)
        if not reconhecimento:
            raise NotFoundError("Reconhecimento nao encontrado.")

        colaborador = self.uow.colaboradores.get_by_id(reconhecimento.colaborador_id)
        if not colaborador:
            raise NotFoundError("Colaborador nao encontrado.")

        AccessScopeService.ensure_can_manage_colaborador(current_user, colaborador)

        cancelador = self.uow.usuarios.get_by_id(dto.cancelado_por_id)
        if not cancelador:
            raise NotFoundError("Usuario cancelador nao encontrado.")

        try:
            reconhecimento.cancelar(dto.cancelado_por_id, dto.motivo_cancelamento)
        except ValueError as exc:
            raise ValidationError(str(exc))

        return self.uow.reconhecimentos.save(reconhecimento)
