from flask import Blueprint, jsonify, request

from application.use_cases.criar_colaborador_uc import CriarColaboradorUC
from infrastructure.database.session import SessionLocal
from infrastructure.unit_of_work_sqlalchemy import UnitOfWorkSQLAlchemy
from interface.schemas.colaborador_schema import parse_criar_colaborador
from interface.schemas.serializers import serialize


colaboradores_interface_bp = Blueprint("interface_colaboradores", __name__, url_prefix="/colaboradores")


@colaboradores_interface_bp.post("")
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


@colaboradores_interface_bp.get("/<int:colaborador_id>/perfil")
def buscar_perfil_colaborador(colaborador_id: int):
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        perfil = uow.perfis_talento.get_ultimo_by_colaborador_id(colaborador_id)

    if not perfil:
        return jsonify({"message": "Colaborador ainda nao possui perfil de talento."}), 404

    return jsonify(serialize(perfil)), 200
