from flask import Blueprint, jsonify, request

from application.use_cases.criar_meta_uc import CriarMetaUC
from infrastructure.database.session import SessionLocal
from infrastructure.unit_of_work_sqlalchemy import UnitOfWorkSQLAlchemy
from interface.schemas.meta_schema import parse_criar_meta
from interface.schemas.serializers import serialize


metas_interface_bp = Blueprint("interface_metas", __name__, url_prefix="/metas")


@metas_interface_bp.post("")
def criar_meta():
    dto = parse_criar_meta(request.get_json(silent=True) or {})

    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        uc = CriarMetaUC(
            colaboradores_repo=uow.colaboradores,
            usuarios_repo=uow.usuarios,
            metas_repo=uow.metas,
        )
        meta = uc.execute(dto)

    return jsonify(serialize(meta)), 201
