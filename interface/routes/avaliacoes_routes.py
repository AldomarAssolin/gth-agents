from flask import Blueprint, jsonify, request

from application.use_cases.registrar_avaliacao_uc import RegistrarAvaliacaoUC
from infrastructure.database.session import SessionLocal
from infrastructure.unit_of_work_sqlalchemy import UnitOfWorkSQLAlchemy
from interface.schemas.avaliacao_schema import parse_registrar_avaliacao
from interface.schemas.serializers import serialize


avaliacoes_interface_bp = Blueprint("interface_avaliacoes", __name__, url_prefix="/avaliacoes")


@avaliacoes_interface_bp.post("")
def registrar_avaliacao():
    dto = parse_registrar_avaliacao(request.get_json(silent=True) or {})

    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        uc = RegistrarAvaliacaoUC(
            colaboradores_repo=uow.colaboradores,
            usuarios_repo=uow.usuarios,
            competencias_repo=uow.competencias,
            avaliacoes_repo=uow.avaliacoes,
            perfis_talento_repo=uow.perfis_talento,
        )
        resultado = uc.execute(dto)

    return jsonify(serialize(resultado)), 201
