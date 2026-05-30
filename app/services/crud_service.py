from app.services.date_utils import parse_date
from domain.enums.perfil_usuario import PerfilUsuario
from domain.enums.status_colaborador import StatusColaborador
from domain.enums.tipo_competencia import TipoCompetencia


class CrudService:
    def __init__(self, repository, required_fields: tuple[str, ...] = ()):
        self.repository = repository
        self.required_fields = required_fields

    def list(self):
        return self.repository.list()

    def get(self, entity_id: int):
        entity = self.repository.get(entity_id)
        if not entity:
            raise ValueError("record not found")
        return entity

    def create(self, data: dict):
        self._validate_required(data)
        return self.repository.create(**data)

    def _validate_required(self, data: dict):
        for field in self.required_fields:
            if data.get(field) in (None, ""):
                raise ValueError(f"{field} is required")


class ColaboradorService(CrudService):
    def create(self, data: dict):
        self._validate_required(data)
        data = data.copy()
        data["data_admissao"] = parse_date(data.get("data_admissao"), "data_admissao")
        status = (data.get("status") or StatusColaborador.ATIVO.value).upper()
        if status not in StatusColaborador._value2member_map_:
            raise ValueError("status is invalid")
        data["status"] = status

        if self.repository.get_by_matricula(data["matricula"]):
            raise ValueError("matricula already exists")

        if data.get("email") and self.repository.get_by_email(data["email"]):
            raise ValueError("email already exists")

        return self.repository.create(**data)


class UsuarioService(CrudService):
    def create(self, data: dict):
        self._validate_required(data)
        data = data.copy()
        perfil = data["perfil"].upper()
        if perfil not in PerfilUsuario._value2member_map_:
            raise ValueError("perfil is invalid")
        data["perfil"] = perfil
        data["ativo"] = data.get("ativo", True)

        if self.repository.get_by_email(data["email"]):
            raise ValueError("email already exists")

        return self.repository.create(**data)


class CompetenciaService(CrudService):
    def create(self, data: dict):
        self._validate_required(data)
        data = data.copy()
        tipo = data["tipo"].upper()
        if tipo not in TipoCompetencia._value2member_map_:
            raise ValueError("tipo is invalid")
        data["tipo"] = tipo
        data["peso"] = data.get("peso", 1.0)
        data["ativo"] = data.get("ativo", True)
        return self.repository.create(**data)
