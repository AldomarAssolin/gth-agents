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
    BuscarSetorPorIdUC,
    AtualizarSetorUC,
    DesativarSetorUC,
    AtivarSetorUC,
    BuscarFuncaoPorIdUC,
    AtualizarFuncaoUC,
    DesativarFuncaoUC,
    AtivarFuncaoUC,
    BuscarUsuarioPorIdUC,
    AtualizarUsuarioUC,
    DesativarUsuarioUC,
    AtivarUsuarioUC,
    BuscarCompetenciaPorIdUC,
    AtualizarCompetenciaUC,
    DesativarCompetenciaUC,
    AtivarCompetenciaUC,
)
from infrastructure.database.session import SessionLocal
from infrastructure.unit_of_work_sqlalchemy import UnitOfWorkSQLAlchemy
from interface.schemas.cadastro_schema import (
    parse_criar_competencia,
    parse_criar_funcao,
    parse_criar_setor,
    parse_criar_usuario,
    parse_atualizar_setor,
    parse_atualizar_funcao,
    parse_atualizar_usuario,
    parse_atualizar_competencia,
)
from interface.schemas.serializers import serialize
from interface.middlewares.auth_middleware import auth_required, roles_required



cadastros_interface_bp = Blueprint("interface_cadastros", __name__)


# Setores
@cadastros_interface_bp.get("/setores")
@auth_required
def listar_setores():
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        setores = ListarSetoresUC(uow.setores).execute()
    return jsonify(serialize(setores)), 200


@cadastros_interface_bp.post("/setores")
@roles_required("ADMIN", "RH")
def criar_setor():

    dto = parse_criar_setor(request.get_json(silent=True) or {})
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        setor = CriarSetorUC(uow.setores).execute(dto)
    return jsonify(serialize(setor)), 201


@cadastros_interface_bp.get("/setores/<int:id>")
@roles_required("ADMIN", "RH")
def obter_setor(id):
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        setor = BuscarSetorPorIdUC(uow.setores).execute(id)
    return jsonify(serialize(setor)), 200


@cadastros_interface_bp.put("/setores/<int:id>")
@roles_required("ADMIN", "RH")
def atualizar_setor(id):
    dto = parse_atualizar_setor(id, request.get_json(silent=True) or {})
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        setor = AtualizarSetorUC(uow.setores).execute(dto)
    return jsonify(serialize(setor)), 200


@cadastros_interface_bp.patch("/setores/<int:id>/desativar")
@roles_required("ADMIN", "RH")
def desativar_setor(id):
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        setor = DesativarSetorUC(uow.setores).execute(id)
    return jsonify(serialize(setor)), 200


@cadastros_interface_bp.patch("/setores/<int:id>/ativar")
@roles_required("ADMIN", "RH")
def ativar_setor(id):
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        setor = AtivarSetorUC(uow.setores).execute(id)
    return jsonify(serialize(setor)), 200


# Funcoes
@cadastros_interface_bp.get("/funcoes")
@auth_required
def listar_funcoes():
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        funcoes = ListarFuncoesUC(uow.funcoes).execute()
    return jsonify(serialize(funcoes)), 200


@cadastros_interface_bp.post("/funcoes")
@roles_required("ADMIN", "RH")
def criar_funcao():

    dto = parse_criar_funcao(request.get_json(silent=True) or {})
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        funcao = CriarFuncaoUC(uow.funcoes).execute(dto)
    return jsonify(serialize(funcao)), 201

@cadastros_interface_bp.get("/funcoes/<int:id>")
@roles_required("ADMIN", "RH")
def obter_funcao(id):
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        funcao = BuscarFuncaoPorIdUC(uow.funcoes).execute(id)
    return jsonify(serialize(funcao)), 200


@cadastros_interface_bp.put("/funcoes/<int:id>")
@roles_required("ADMIN", "RH")
def atualizar_funcao(id):
    dto = parse_atualizar_funcao(id, request.get_json(silent=True) or {})
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        funcao = AtualizarFuncaoUC(uow.funcoes).execute(dto)
    return jsonify(serialize(funcao)), 200


@cadastros_interface_bp.patch("/funcoes/<int:id>/desativar")
@roles_required("ADMIN", "RH")
def desativar_funcao(id):
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        funcao = DesativarFuncaoUC(uow.funcoes).execute(id)
    return jsonify(serialize(funcao)), 200


@cadastros_interface_bp.patch("/funcoes/<int:id>/ativar")
@roles_required("ADMIN", "RH")
def ativar_funcao(id):
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        funcao = AtivarFuncaoUC(uow.funcoes).execute(id)
    return jsonify(serialize(funcao)), 200


# Usuarios
@cadastros_interface_bp.get("/usuarios")
@roles_required("ADMIN", "RH")
def listar_usuarios():
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        usuarios = ListarUsuariosUC(uow.usuarios).execute()
    return jsonify(serialize(usuarios)), 200


@cadastros_interface_bp.post("/usuarios")
@roles_required("ADMIN", "RH")
def criar_usuario():

    dto = parse_criar_usuario(request.get_json(silent=True) or {})
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        usuario = CriarUsuarioUC(uow.usuarios).execute(dto)
    return jsonify(serialize(usuario)), 201

@cadastros_interface_bp.get("/usuarios/<int:id>")
@roles_required("ADMIN", "RH")
def obter_usuario(id):
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        usuario = BuscarUsuarioPorIdUC(uow.usuarios).execute(id)
    return jsonify(serialize(usuario)), 200


@cadastros_interface_bp.put("/usuarios/<int:id>")
@roles_required("ADMIN", "RH")
def atualizar_usuario(id):
    dto = parse_atualizar_usuario(id, request.get_json(silent=True) or {})
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        usuario = AtualizarUsuarioUC(uow.usuarios).execute(dto)
    return jsonify(serialize(usuario)), 200


@cadastros_interface_bp.patch("/usuarios/<int:id>/desativar")
@roles_required("ADMIN", "RH")
def desativar_usuario(id):
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        usuario = DesativarUsuarioUC(uow.usuarios).execute(id)
    return jsonify(serialize(usuario)), 200


@cadastros_interface_bp.patch("/usuarios/<int:id>/ativar")
@roles_required("ADMIN", "RH")
def ativar_usuario(id):
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        usuario = AtivarUsuarioUC(uow.usuarios).execute(id)
    return jsonify(serialize(usuario)), 200


# Competencias
@cadastros_interface_bp.get("/competencias")
@auth_required
def listar_competencias():
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        competencias = ListarCompetenciasUC(uow.competencias).execute()
    return jsonify(serialize(competencias)), 200


@cadastros_interface_bp.post("/competencias")
@roles_required("ADMIN", "RH")
def criar_competencia():

    dto = parse_criar_competencia(request.get_json(silent=True) or {})
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        competencia = CriarCompetenciaUC(uow.competencias).execute(dto)
    return jsonify(serialize(competencia)), 201

@cadastros_interface_bp.get("/competencias/<int:id>")
@roles_required("ADMIN", "RH")
def obter_competencia(id):
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        competencia = BuscarCompetenciaPorIdUC(uow.competencias).execute(id)
    return jsonify(serialize(competencia)), 200
    

@cadastros_interface_bp.put("/competencias/<int:id>")
@roles_required("ADMIN", "RH")
def atualizar_competencia(id):
    dto = parse_atualizar_competencia(id, request.get_json(silent=True) or {})
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        competencia = AtualizarCompetenciaUC(uow.competencias).execute(dto)
    return jsonify(serialize(competencia)), 200


@cadastros_interface_bp.patch("/competencias/<int:id>/desativar")
@roles_required("ADMIN", "RH")
def desativar_competencia(id):
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        competencia = DesativarCompetenciaUC(uow.competencias).execute(id)
    return jsonify(serialize(competencia)), 200


@cadastros_interface_bp.patch("/competencias/<int:id>/ativar")
@roles_required("ADMIN", "RH")
def ativar_competencia(id):
    with UnitOfWorkSQLAlchemy(SessionLocal) as uow:
        competencia = AtivarCompetenciaUC(uow.competencias).execute(id)
    return jsonify(serialize(competencia)), 200
