from flask import Blueprint, jsonify, request

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



colaboradores_interface_bp = Blueprint("interface_colaboradores", __name__, url_prefix="/colaboradores")


@colaboradores_interface_bp.get("")
def listar_colaboradores():
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        uc = ListarColaboradoresUC(uow.colaboradores)
        colaboradores = uc.execute()
    return jsonify(serialize(colaboradores)), 200


@colaboradores_interface_bp.post("")
@auth_required
def criar_colaborador():
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
def obter_colaborador(id: int):
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        uc = BuscarColaboradorPorIdUC(uow.colaboradores)
        colaborador = uc.execute(id)
    return jsonify(serialize(colaborador)), 200


@colaboradores_interface_bp.put("/<int:id>")
def atualizar_colaborador(id: int):
    dto = parse_atualizar_colaborador(id, request.get_json(silent=True) or {})
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        uc = AtualizarColaboradorUC(
            colaboradores_repo=uow.colaboradores,
            setores_repo=uow.setores,
            funcoes_repo=uow.funcoes,
        )
        colaborador = uc.execute(dto)
    return jsonify(serialize(colaborador)), 200


@colaboradores_interface_bp.patch("/<int:id>/ativar")
def ativar_colaborador(id: int):
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        uc = AlterarStatusColaboradorUC(uow.colaboradores)
        colaborador = uc.execute(id, StatusColaborador.ATIVO)
    return jsonify(serialize(colaborador)), 200


@colaboradores_interface_bp.patch("/<int:id>/inativar")
def inativar_colaborador(id: int):
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        uc = AlterarStatusColaboradorUC(uow.colaboradores)
        colaborador = uc.execute(id, StatusColaborador.INATIVO)
    return jsonify(serialize(colaborador)), 200


@colaboradores_interface_bp.patch("/<int:id>/afastar")
def afastar_colaborador(id: int):
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        uc = AlterarStatusColaboradorUC(uow.colaboradores)
        colaborador = uc.execute(id, StatusColaborador.AFASTADO)
    return jsonify(serialize(colaborador)), 200


@colaboradores_interface_bp.patch("/<int:id>/desligar")
def desligar_colaborador(id: int):
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        uc = AlterarStatusColaboradorUC(uow.colaboradores)
        colaborador = uc.execute(id, StatusColaborador.DESLIGADO)
    return jsonify(serialize(colaborador)), 200


@colaboradores_interface_bp.get("/<int:colaborador_id>/perfil")
@auth_required
def buscar_perfil_colaborador(colaborador_id: int):
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        perfil = uow.perfis_talento.get_ultimo_by_colaborador_id(colaborador_id)

    if not perfil:
        return jsonify({"message": "Colaborador ainda nao possui perfil de talento."}), 404

    return jsonify(serialize(perfil)), 200


@colaboradores_interface_bp.get("/<int:id>/evolucao")
def obter_evolucao_colaborador(id: int):
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
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
def listar_metas_colaborador(id: int):
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        uc = ListarMetasColaboradorUC(
            colaboradores_repo=uow.colaboradores,
            metas_repo=uow.metas,
        )
        metas = uc.execute(id)
    return jsonify(serialize(metas)), 200
