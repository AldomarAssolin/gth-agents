from flask import Blueprint, jsonify, g

from application.use_cases.dashboard_uc import ConsultarDashboardMVP_UC
from infrastructure.database.session import SessionLocal
from infrastructure.unit_of_work_sqlalchemy import UnitOfWorkSQLAlchemy
from interface.schemas.serializers import serialize
from interface.middlewares.auth_middleware import auth_required, roles_required

dashboard_interface_bp = Blueprint("interface_dashboard", __name__, url_prefix="/dashboard")


@dashboard_interface_bp.get("/mvp")
@auth_required
@roles_required("ADMIN", "RH", "LIDER")
def consultar_dashboard_mvp():
    current_user = g.usuario

    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        uc = ConsultarDashboardMVP_UC(uow)
        resultado = uc.execute(current_user=current_user)

    return jsonify(serialize(resultado)), 200
