from flask import Blueprint, jsonify, request

from application.use_cases.registrar_feedback_uc import RegistrarFeedbackUC
from application.use_cases.estruturar_feedback_uc import EstruturarFeedbackUC
from infrastructure.database.session import SessionLocal
from infrastructure.unit_of_work_sqlalchemy import UnitOfWorkSQLAlchemy
from interface.schemas.feedback_schema import parse_registrar_feedback, parse_estruturar_feedback
from interface.schemas.serializers import serialize


feedbacks_interface_bp = Blueprint("interface_feedbacks", __name__, url_prefix="/feedbacks")


@feedbacks_interface_bp.post("")
def registrar_feedback():
    dto = parse_registrar_feedback(request.get_json(silent=True) or {})

    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        uc = RegistrarFeedbackUC(
            colaboradores_repo=uow.colaboradores,
            usuarios_repo=uow.usuarios,
            feedbacks_repo=uow.feedbacks,
        )
        feedback = uc.execute(dto)

    return jsonify(serialize(feedback)), 201


@feedbacks_interface_bp.post("/estruturar")
def estruturar_feedback():
    dto = parse_estruturar_feedback(request.get_json(silent=True) or {})
    uc = EstruturarFeedbackUC()
    resultado = uc.execute(dto)
    return jsonify(serialize(resultado)), 200
