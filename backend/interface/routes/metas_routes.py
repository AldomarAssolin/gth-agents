from flask import Blueprint, jsonify, request, g

from application.use_cases.criar_meta_uc import CriarMetaUC
from infrastructure.database.session import SessionLocal
from infrastructure.unit_of_work_sqlalchemy import UnitOfWorkSQLAlchemy
from interface.schemas.meta_schema import parse_criar_meta
from interface.schemas.serializers import serialize
from interface.middlewares.auth_middleware import roles_required
from application.security.access_scope_service import AccessScopeService
from application.errors import NotFoundError


metas_interface_bp = Blueprint("interface_metas", __name__, url_prefix="/metas")


@metas_interface_bp.post("")
@roles_required("ADMIN", "RH", "LIDER")
def criar_meta():
    dto = parse_criar_meta(request.get_json(silent=True) or {}, criado_por_id=g.usuario["id"])

    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        colaborador = uow.colaboradores.get_by_id(dto.colaborador_id)
        if not colaborador:
            raise NotFoundError("Colaborador nao encontrado.")

        AccessScopeService.ensure_can_manage_colaborador(g.usuario, colaborador)

        uc = CriarMetaUC(
            colaboradores_repo=uow.colaboradores,
            usuarios_repo=uow.usuarios,
            metas_repo=uow.metas,
        )
        meta = uc.execute(dto)

    return jsonify(serialize(meta)), 201
