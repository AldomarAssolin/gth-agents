from flask import Blueprint, jsonify, request
from application.dtos.auth_dto import LoginDTO
from application.use_cases.login_usuario_uc import LoginUsuarioUC
from infrastructure.database.session import SessionLocal
from infrastructure.unit_of_work_sqlalchemy import UnitOfWorkSQLAlchemy
from interface.schemas.serializers import serialize

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/auth/login")
def login():
    data = request.get_json(silent=True) or {}
    dto = LoginDTO(email=data.get("email"), senha=data.get("senha"))

    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        uc = LoginUsuarioUC(uow.usuarios)
        resultado = uc.execute(dto)

    return jsonify(serialize(resultado)), 200
