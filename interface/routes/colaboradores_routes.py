from flask import Blueprint, jsonify, request, g

from application.use_cases.criar_colaborador_uc import CriarColaboradorUC
from application.use_cases.evolucao_colaborador_uc import VisualizarEvolucaoColaboradorUC
from application.use_cases.listar_metas_uc import ListarMetasColaboradorUC
from application.use_cases.colaborador_use_cases import (
    ListarColaboradoresUC,
    BuscarColaboradorPorIdUC,
    AtualizarColaboradorUC,
    AlterarStatusColaboradorUC,
)
from domain.enums.status_colaborador import StatusColaborador
from infrastructure.database.session import SessionLocal
from infrastructure.unit_of_work_sqlalchemy import UnitOfWorkSQLAlchemy
from interface.schemas.colaborador_schema import parse_criar_colaborador, parse_atualizar_colaborador
from interface.schemas.serializers import serialize
from interface.middlewares.auth_middleware import auth_required
from application.security.access_scope_service import AccessScopeService
from application.errors import NotFoundError, ForbiddenError


colaboradores_interface_bp = Blueprint("interface_colaboradores", __name__, url_prefix="/colaboradores")


@colaboradores_interface_bp.get("")
@auth_required
def listar_colaboradores():
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        uc = ListarColaboradoresUC(uow.colaboradores)
        colaboradores = uc.execute()

        perfil = g.usuario.get("perfil")
        if perfil == "LIDER":
            setor_id = g.usuario.get("setor_id")
            if setor_id is None:
                raise ForbiddenError("Lider nao possui setor vinculado.")
            colaboradores = [c for c in colaboradores if c.setor_id == setor_id]
        elif perfil == "COLABORADOR":
            colaborador_id = g.usuario.get("colaborador_id")
            if colaborador_id is None:
                raise ForbiddenError("Colaborador nao possui id de colaborador vinculado.")
            colaboradores = [c for c in colaboradores if c.id == colaborador_id]

    return jsonify(serialize(colaboradores)), 200


@colaboradores_interface_bp.post("")
@auth_required
def criar_colaborador():
    perfil = g.usuario.get("perfil")
    if perfil not in ("ADMIN", "RH"):
        raise ForbiddenError("Acesso negado.")

    dto = parse_criar_colaborador(request.get_json(silent=True) or {})

    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        uc = CriarColaboradorUC(
            colaboradores_repo=uow.colaboradores,
            setores_repo=uow.setores,
            funcoes_repo=uow.funcoes,
        )
        colaborador = uc.execute(dto)

    return jsonify(serialize(colaborador)), 201


@colaboradores_interface_bp.get("/<int:id>")
@auth_required
def obter_colaborador(id: int):
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        uc = BuscarColaboradorPorIdUC(uow.colaboradores)
        colaborador = uc.execute(id)
        
        AccessScopeService.ensure_can_access_colaborador(g.usuario, colaborador)

    return jsonify(serialize(colaborador)), 200


@colaboradores_interface_bp.put("/<int:id>")
@auth_required
def atualizar_colaborador(id: int):
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        uc_get = BuscarColaboradorPorIdUC(uow.colaboradores)
        colaborador = uc_get.execute(id)

        AccessScopeService.ensure_can_manage_colaborador(g.usuario, colaborador)

        dto = parse_atualizar_colaborador(id, request.get_json(silent=True) or {})

        if g.usuario.get("perfil") == "LIDER":
            if dto.setor_id != g.usuario.get("setor_id"):
                raise ForbiddenError("Lider nao pode alterar o setor do colaborador para fora do seu escopo.")

        uc = RedirectToUpdates = AtualizarColaboradorUC(
            colaboradores_repo=uow.colaboradores,
            setores_repo=uow.setores,
            funcoes_repo=uow.funcoes,
        )
        colaborador = uc.execute(dto)

    return jsonify(serialize(colaborador)), 200


@colaboradores_interface_bp.patch("/<int:id>/ativar")
@auth_required
def ativar_colaborador(id: int):
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        colaborador = uow.colaboradores.get_by_id(id)
        if not colaborador:
            raise NotFoundError("Colaborador nao encontrado.")

        AccessScopeService.ensure_can_manage_colaborador(g.usuario, colaborador)

        uc = AlterarStatusColaboradorUC(uow.colaboradores)
        colaborador = uc.execute(id, StatusColaborador.ATIVO)

    return jsonify(serialize(colaborador)), 200


@colaboradores_interface_bp.patch("/<int:id>/inativar")
@auth_required
def inativar_colaborador(id: int):
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        colaborador = uow.colaboradores.get_by_id(id)
        if not colaborador:
            raise NotFoundError("Colaborador nao encontrado.")

        AccessScopeService.ensure_can_manage_colaborador(g.usuario, colaborador)

        uc = AlterarStatusColaboradorUC(uow.colaboradores)
        colaborador = uc.execute(id, StatusColaborador.INATIVO)

    return jsonify(serialize(colaborador)), 200


@colaboradores_interface_bp.patch("/<int:id>/afastar")
@auth_required
def afastar_colaborador(id: int):
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        colaborador = uow.colaboradores.get_by_id(id)
        if not colaborador:
            raise NotFoundError("Colaborador nao encontrado.")

        AccessScopeService.ensure_can_manage_colaborador(g.usuario, colaborador)

        uc = AlterarStatusColaboradorUC(uow.colaboradores)
        colaborador = uc.execute(id, StatusColaborador.AFASTADO)

    return jsonify(serialize(colaborador)), 200


@colaboradores_interface_bp.patch("/<int:id>/desligar")
@auth_required
def desligar_colaborador(id: int):
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        colaborador = uow.colaboradores.get_by_id(id)
        if not colaborador:
            raise NotFoundError("Colaborador nao encontrado.")

        AccessScopeService.ensure_can_manage_colaborador(g.usuario, colaborador)

        uc = AlterarStatusColaboradorUC(uow.colaboradores)
        colaborador = uc.execute(id, StatusColaborador.DESLIGADO)

    return jsonify(serialize(colaborador)), 200


@colaboradores_interface_bp.get("/<int:colaborador_id>/perfil")
@auth_required
def buscar_perfil_colaborador(colaborador_id: int):
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        AccessScopeService.ensure_can_access_recurso_do_colaborador(g.usuario, colaborador_id, uow.colaboradores)
        perfil = uow.perfis_talento.get_ultimo_by_colaborador_id(colaborador_id)

    if not perfil:
        return jsonify({"message": "Colaborador ainda nao possui perfil de talento."}), 404

    return jsonify(serialize(perfil)), 200


@colaboradores_interface_bp.get("/<int:id>/evolucao")
@auth_required
def obter_evolucao_colaborador(id: int):
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        AccessScopeService.ensure_can_access_recurso_do_colaborador(g.usuario, id, uow.colaboradores)

        uc = VisualizarEvolucaoColaboradorUC(
            colaboradores_repo=uow.colaboradores,
            avaliacoes_repo=uow.avaliacoes,
            metas_repo=uow.metas,
            feedbacks_repo=uow.feedbacks,
            perfis_repo=uow.perfis_talento,
            competencias_repo=uow.competencias,
        )
        resultado = uc.execute(id)

    return jsonify(serialize(resultado)), 200


@colaboradores_interface_bp.get("/<int:id>/metas")
@auth_required
def listar_metas_colaborador(id: int):
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        AccessScopeService.ensure_can_access_recurso_do_colaborador(g.usuario, id, uow.colaboradores)

        uc = ListarMetasColaboradorUC(
            colaboradores_repo=uow.colaboradores,
            metas_repo=uow.metas,
        )
        metas = uc.execute(id)

    return jsonify(serialize(metas)), 200
