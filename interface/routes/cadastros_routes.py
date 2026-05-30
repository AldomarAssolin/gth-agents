from flask import Blueprint, jsonify, request

from application.use_cases.cadastros_basicos_uc import (
    CriarCompetenciaUC,
    CriarFuncaoUC,
    CriarSetorUC,
    CriarUsuarioUC,
    ListarCompetenciasUC,
    ListarFuncoesUC,
    ListarSetoresUC,
    ListarUsuariosUC,
)
from infrastructure.database.session import SessionLocal
from infrastructure.unit_of_work_sqlalchemy import UnitOfWorkSQLAlchemy
from interface.schemas.cadastro_schema import (
    parse_criar_competencia,
    parse_criar_funcao,
    parse_criar_setor,
    parse_criar_usuario,
)
from interface.schemas.serializers import serialize


cadastros_interface_bp = Blueprint("interface_cadastros", __name__)


@cadastros_interface_bp.get("/setores")
def listar_setores():
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        setores = ListarSetoresUC(uow.setores).execute()
    return jsonify(serialize(setores)), 200


@cadastros_interface_bp.post("/setores")
def criar_setor():
    dto = parse_criar_setor(request.get_json(silent=True) or {})
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        setor = CriarSetorUC(uow.setores).execute(dto)
    return jsonify(serialize(setor)), 201


@cadastros_interface_bp.get("/funcoes")
def listar_funcoes():
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        funcoes = ListarFuncoesUC(uow.funcoes).execute()
    return jsonify(serialize(funcoes)), 200


@cadastros_interface_bp.post("/funcoes")
def criar_funcao():
    dto = parse_criar_funcao(request.get_json(silent=True) or {})
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        funcao = CriarFuncaoUC(uow.funcoes).execute(dto)
    return jsonify(serialize(funcao)), 201


@cadastros_interface_bp.get("/usuarios")
def listar_usuarios():
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        usuarios = ListarUsuariosUC(uow.usuarios).execute()
    return jsonify(serialize(usuarios)), 200


@cadastros_interface_bp.post("/usuarios")
def criar_usuario():
    dto = parse_criar_usuario(request.get_json(silent=True) or {})
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        usuario = CriarUsuarioUC(uow.usuarios).execute(dto)
    return jsonify(serialize(usuario)), 201


@cadastros_interface_bp.get("/competencias")
def listar_competencias():
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        competencias = ListarCompetenciasUC(uow.competencias).execute()
    return jsonify(serialize(competencias)), 200


@cadastros_interface_bp.post("/competencias")
def criar_competencia():
    dto = parse_criar_competencia(request.get_json(silent=True) or {})
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        competencia = CriarCompetenciaUC(uow.competencias).execute(dto)
    return jsonify(serialize(competencia)), 201
