from flask import Blueprint, jsonify, request, g
from application.use_cases.pdi_uc import (
    CriarPDIUC,
    ListarPDIsUC,
    BuscarPDIUC,
    ListarPDIsPorColaboradorUC,
    AtualizarPDIUC,
    ConcluirPDIUC,
    CancelarPDIUC,
    CriarAcaoPDIUC,
    AtualizarAcaoPDIUC,
    ConcluirAcaoPDIUC,
    CancelarAcaoPDIUC,
)
from infrastructure.database.session import SessionLocal
from infrastructure.unit_of_work_sqlalchemy import UnitOfWorkSQLAlchemy
from interface.schemas.pdi_schema import (
    parse_criar_pdi,
    parse_atualizar_pdi,
    parse_criar_acao_pdi,
    parse_atualizar_acao_pdi,
)
from interface.schemas.serializers import serialize
from interface.middlewares.auth_middleware import auth_required, roles_required
from application.security.access_scope_service import AccessScopeService
from application.errors import NotFoundError, ForbiddenError, ValidationError

pdis_interface_bp = Blueprint("interface_pdis", __name__)


@pdis_interface_bp.post("/pdis")
@roles_required("ADMIN", "RH", "LIDER")
def criar_pdi():
    dto = parse_criar_pdi(request.get_json(silent=True) or {}, g.usuario.get("id"))

    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        colaborador = uow.colaboradores.get_by_id(dto.colaborador_id)
        if not colaborador:
            raise NotFoundError("Colaborador nao encontrado.")

        AccessScopeService.ensure_can_manage_colaborador(g.usuario, colaborador)

        uc = CriarPDIUC(
            colaboradores_repo=uow.colaboradores,
            usuarios_repo=uow.usuarios,
            pdis_repo=uow.pdis,
        )
        pdi = uc.execute(dto)

    return jsonify(serialize(pdi)), 201


@pdis_interface_bp.get("/pdis")
@auth_required
def listar_pdis():
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        uc = ListarPDIsUC(uow.pdis)
        pdis = uc.execute()

        perfil = g.usuario.get("perfil")
        if perfil == "LIDER":
            setor_id = g.usuario.get("setor_id")
            if setor_id is None:
                raise ForbiddenError("Lider nao possui setor vinculado.")
            # Filter in-memory to only include collaborators from leader's sector
            filtrados = []
            for p in pdis:
                colab = uow.colaboradores.get_by_id(p.colaborador_id)
                if colab and colab.setor_id == setor_id:
                    filtrados.append(p)
            pdis = filtrados
        elif perfil == "COLABORADOR":
            colaborador_id = g.usuario.get("colaborador_id")
            if colaborador_id is None:
                raise ForbiddenError("Colaborador nao possui id de colaborador vinculado.")
            pdis = [p for p in pdis if p.colaborador_id == colaborador_id]

    return jsonify(serialize(pdis)), 200


@pdis_interface_bp.get("/pdis/<int:pdi_id>")
@auth_required
def buscar_pdi(pdi_id: int):
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        uc = BuscarPDIUC(uow.pdis)
        pdi = uc.execute(pdi_id)

        colaborador = uow.colaboradores.get_by_id(pdi.colaborador_id)
        if not colaborador:

            raise NotFoundError("Colaborador nao encontrado.")

        AccessScopeService.ensure_can_access_colaborador(g.usuario, colaborador)


    return jsonify(serialize(pdi)), 200


@pdis_interface_bp.patch("/pdis/<int:pdi_id>")
@roles_required("ADMIN", "RH", "LIDER")
def atualizar_pdi(pdi_id: int):
    dto = parse_atualizar_pdi(pdi_id, request.get_json(silent=True) or {})

    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        pdi = uow.pdis.get_by_id(pdi_id)
        if not pdi:
            raise NotFoundError("PDI nao encontrado.")

        colaborador = uow.colaboradores.get_by_id(pdi.colaborador_id)
        if not colaborador:
            raise NotFoundError("Colaborador nao encontrado.")

        AccessScopeService.ensure_can_manage_colaborador(g.usuario, colaborador)

        uc = AtualizarPDIUC(uow.pdis)
        pdi_atualizado = uc.execute(dto)

    return jsonify(serialize(pdi_atualizado)), 200


@pdis_interface_bp.patch("/pdis/<int:pdi_id>/concluir")
@roles_required("ADMIN", "RH", "LIDER")
def concluir_pdi(pdi_id: int):
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        pdi = uow.pdis.get_by_id(pdi_id)
        if not pdi:
            raise NotFoundError("PDI nao encontrado.")

        colaborador = uow.colaboradores.get_by_id(pdi.colaborador_id)
        if not colaborador:
            raise NotFoundError("Colaborador nao encontrado.")

        AccessScopeService.ensure_can_manage_colaborador(g.usuario, colaborador)

        uc = ConcluirPDIUC(uow.pdis)
        pdi_concluido = uc.execute(pdi_id)

    return jsonify(serialize(pdi_concluido)), 200


@pdis_interface_bp.patch("/pdis/<int:pdi_id>/cancelar")
@roles_required("ADMIN", "RH", "LIDER")
def cancelar_pdi(pdi_id: int):
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        pdi = uow.pdis.get_by_id(pdi_id)
        if not pdi:
            raise NotFoundError("PDI nao encontrado.")

        colaborador = uow.colaboradores.get_by_id(pdi.colaborador_id)
        if not colaborador:
            raise NotFoundError("Colaborador nao encontrado.")

        AccessScopeService.ensure_can_manage_colaborador(g.usuario, colaborador)

        uc = CancelarPDIUC(uow.pdis)
        pdi_cancelado = uc.execute(pdi_id)

    return jsonify(serialize(pdi_cancelado)), 200


@pdis_interface_bp.get("/colaboradores/<int:colaborador_id>/pdis")
@auth_required
def listar_pdis_do_colaborador(colaborador_id: int):
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        colaborador = uow.colaboradores.get_by_id(colaborador_id)
        if not colaborador:
            raise NotFoundError("Colaborador nao encontrado.")

        AccessScopeService.ensure_can_access_colaborador(g.usuario, colaborador)

        uc = ListarPDIsPorColaboradorUC(uow.pdis)
        pdis = uc.execute(colaborador_id)

    return jsonify(serialize(pdis)), 200


@pdis_interface_bp.post("/pdis/<int:pdi_id>/acoes")
@roles_required("ADMIN", "RH", "LIDER")
def criar_acao_pdi(pdi_id: int):
    dto = parse_criar_acao_pdi(pdi_id, request.get_json(silent=True) or {})

    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        pdi = uow.pdis.get_by_id(pdi_id)
        if not pdi:
            raise NotFoundError("PDI nao encontrado.")

        colaborador = uow.colaboradores.get_by_id(pdi.colaborador_id)
        if not colaborador:
            raise NotFoundError("Colaborador nao encontrado.")

        AccessScopeService.ensure_can_manage_colaborador(g.usuario, colaborador)

        uc = CriarAcaoPDIUC(uow.pdis, uow.acoes_pdi)
        acao = uc.execute(dto)

    return jsonify(serialize(acao)), 201


@pdis_interface_bp.get("/pdis/<int:pdi_id>/acoes")
@auth_required
def listar_acoes_pdi(pdi_id: int):
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        pdi = uow.pdis.get_by_id(pdi_id)
        if not pdi:
            raise NotFoundError("PDI nao encontrado.")

        colaborador = uow.colaboradores.get_by_id(pdi.colaborador_id)
        if not colaborador:
            raise NotFoundError("Colaborador nao encontrado.")

        AccessScopeService.ensure_can_access_colaborador(g.usuario, colaborador)

        acoes = uow.acoes_pdi.list_by_pdi_id(pdi_id)

    return jsonify(serialize(acoes)), 200


@pdis_interface_bp.patch("/pdis/<int:pdi_id>/acoes/<int:acao_id>")
@roles_required("ADMIN", "RH", "LIDER")
def atualizar_acao_pdi(pdi_id: int, acao_id: int):
    dto = parse_atualizar_acao_pdi(acao_id, request.get_json(silent=True) or {})

    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        acao = uow.acoes_pdi.get_by_id(acao_id)
        if not acao or acao.pdi_id != pdi_id:
            raise NotFoundError("Acao nao encontrada para este PDI.")

        pdi = uow.pdis.get_by_id(pdi_id)
        if not pdi:
            raise NotFoundError("PDI nao encontrado.")

        colaborador = uow.colaboradores.get_by_id(pdi.colaborador_id)
        if not colaborador:
            raise NotFoundError("Colaborador nao encontrado.")

        AccessScopeService.ensure_can_manage_colaborador(g.usuario, colaborador)

        uc = AtualizarAcaoPDIUC(uow.pdis, uow.acoes_pdi)
        acao_atualizada = uc.execute(dto)

    return jsonify(serialize(acao_atualizada)), 200


@pdis_interface_bp.patch("/pdis/<int:pdi_id>/acoes/<int:acao_id>/concluir")
@roles_required("ADMIN", "RH", "LIDER")
def concluir_acao_pdi(pdi_id: int, acao_id: int):
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        acao = uow.acoes_pdi.get_by_id(acao_id)
        if not acao or acao.pdi_id != pdi_id:
            raise NotFoundError("Acao nao encontrada para este PDI.")

        pdi = uow.pdis.get_by_id(pdi_id)
        if not pdi:
            raise NotFoundError("PDI nao encontrado.")

        colaborador = uow.colaboradores.get_by_id(pdi.colaborador_id)
        if not colaborador:
            raise NotFoundError("Colaborador nao encontrado.")

        AccessScopeService.ensure_can_manage_colaborador(g.usuario, colaborador)

        uc = ConcluirAcaoPDIUC(uow.pdis, uow.acoes_pdi)
        acao_concluida = uc.execute(acao_id)

    return jsonify(serialize(acao_concluida)), 200


@pdis_interface_bp.patch("/pdis/<int:pdi_id>/acoes/<int:acao_id>/cancelar")
@roles_required("ADMIN", "RH", "LIDER")
def cancelar_acao_pdi(pdi_id: int, acao_id: int):
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        acao = uow.acoes_pdi.get_by_id(acao_id)
        if not acao or acao.pdi_id != pdi_id:
            raise NotFoundError("Acao nao encontrada para este PDI.")

        pdi = uow.pdis.get_by_id(pdi_id)
        if not pdi:
            raise NotFoundError("PDI nao encontrado.")

        colaborador = uow.colaboradores.get_by_id(pdi.colaborador_id)
        if not colaborador:
            raise NotFoundError("Colaborador nao encontrado.")

        AccessScopeService.ensure_can_manage_colaborador(g.usuario, colaborador)

        uc = CancelarAcaoPDIUC(uow.pdis, uow.acoes_pdi)
        acao_cancelada = uc.execute(acao_id)

    return jsonify(serialize(acao_cancelada)), 200
