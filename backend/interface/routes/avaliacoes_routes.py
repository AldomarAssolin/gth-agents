from flask import Blueprint, jsonify, request, g

from application.use_cases.registrar_avaliacao_uc import RegistrarAvaliacaoUC
from infrastructure.database.session import SessionLocal
from infrastructure.unit_of_work_sqlalchemy import UnitOfWorkSQLAlchemy
from interface.schemas.avaliacao_schema import parse_registrar_avaliacao
from interface.schemas.serializers import serialize
from interface.middlewares.auth_middleware import roles_required
from application.security.access_scope_service import AccessScopeService
from application.errors import NotFoundError


avaliacoes_interface_bp = Blueprint("interface_avaliacoes", __name__, url_prefix="/avaliacoes")


@avaliacoes_interface_bp.post("")
@roles_required("ADMIN", "RH", "LIDER")
def registrar_avaliacao():
    dto = parse_registrar_avaliacao(request.get_json(silent=True) or {}, avaliador_id=g.usuario["id"])

    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        colaborador = uow.colaboradores.get_by_id(dto.colaborador_id)
        if not colaborador:
            raise NotFoundError("Colaborador nao encontrado.")

        AccessScopeService.ensure_can_manage_colaborador(g.usuario, colaborador)

        uc = RegistrarAvaliacaoUC(
            colaboradores_repo=uow.colaboradores,
            usuarios_repo=uow.usuarios,
            competencias_repo=uow.competencias,
            avaliacoes_repo=uow.avaliacoes,
            perfis_talento_repo=uow.perfis_talento,
            execucoes_agente_repo=uow.execucoes_agente,
        )
        resultado = uc.execute(dto)

    return jsonify(serialize(resultado)), 201
