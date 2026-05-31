from flask import Blueprint, jsonify, request, g
from application.dtos.reconhecimento_dto import (
    CriarReconhecimentoDTO,
    CancelarReconhecimentoDTO,
)
from application.use_cases.reconhecimento_uc import (
    CriarReconhecimentoUC,
    ListarReconhecimentosUC,
    BuscarReconhecimentoUC,
    ListarReconhecimentosPorColaboradorUC,
    CancelarReconhecimentoUC,
)
from infrastructure.database.session import SessionLocal
from infrastructure.unit_of_work_sqlalchemy import UnitOfWorkSQLAlchemy
from interface.middlewares.auth_middleware import auth_required, roles_required
from interface.schemas.reconhecimento_schema import (
    parse_criar_reconhecimento,
    parse_cancelar_reconhecimento,
)
from interface.schemas.serializers import serialize


reconhecimentos_interface_bp = Blueprint("interface_reconhecimentos", __name__)


@reconhecimentos_interface_bp.post("/reconhecimentos")
@roles_required("ADMIN", "RH", "LIDER")
def criar_reconhecimento():
    dto = parse_criar_reconhecimento(
        request.get_json(silent=True) or {},
        g.usuario.get("id"),
    )

    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        uc = CriarReconhecimentoUC(uow)
        reconhecimento = uc.execute(dto, g.usuario)

    return jsonify(serialize(reconhecimento)), 201


@reconhecimentos_interface_bp.get("/reconhecimentos")
@auth_required
def listar_reconhecimentos():
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        uc = ListarReconhecimentosUC(uow)
        reconhecimentos = uc.execute(g.usuario)

    return jsonify(serialize(reconhecimentos)), 200


@reconhecimentos_interface_bp.get("/reconhecimentos/<int:reconhecimento_id>")
@auth_required
def buscar_reconhecimento(reconhecimento_id: int):
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        uc = BuscarReconhecimentoUC(uow)
        reconhecimento = uc.execute(reconhecimento_id, g.usuario)

    return jsonify(serialize(reconhecimento)), 200


@reconhecimentos_interface_bp.patch("/reconhecimentos/<int:reconhecimento_id>/cancelar")
@roles_required("ADMIN", "RH", "LIDER")
def cancelar_reconhecimento(reconhecimento_id: int):
    dto = parse_cancelar_reconhecimento(
        reconhecimento_id,
        request.get_json(silent=True) or {},
        g.usuario.get("id"),
    )

    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        uc = CancelarReconhecimentoUC(uow)
        reconhecimento = uc.execute(dto, g.usuario)

    return jsonify(serialize(reconhecimento)), 200


@reconhecimentos_interface_bp.get("/colaboradores/<int:colaborador_id>/reconhecimentos")
@auth_required
def listar_reconhecimentos_do_colaborador(colaborador_id: int):
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        uc = ListarReconhecimentosPorColaboradorUC(uow)
        reconhecimentos = uc.execute(colaborador_id, g.usuario)

    return jsonify(serialize(reconhecimentos)), 200
