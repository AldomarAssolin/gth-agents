from application.errors import ForbiddenError, NotFoundError


class AccessScopeService:
    @staticmethod
    def can_access_colaborador(usuario: dict | object, colaborador: object) -> bool:
        def get_attr(obj, name):
            if isinstance(obj, dict):
                return obj.get(name)
            return getattr(obj, name, None)

        perfil_val = get_attr(usuario, "perfil")
        perfil = perfil_val.value if hasattr(perfil_val, "value") else str(perfil_val)

        if perfil in ("ADMIN", "RH"):
            return True

        if perfil == "LIDER":
            setor_id = get_attr(usuario, "setor_id")
            if setor_id is None:
                return False
            colab_setor_id = get_attr(colaborador, "setor_id")
            return setor_id == colab_setor_id

        if perfil == "COLABORADOR":
            colaborador_id = get_attr(usuario, "colaborador_id")
            if colaborador_id is None:
                return False
            return colaborador_id == get_attr(colaborador, "id")

        return False

    @classmethod
    def ensure_can_access_colaborador(cls, usuario: dict | object, colaborador: object) -> None:
        if not cls.can_access_colaborador(usuario, colaborador):
            raise ForbiddenError("Acesso negado.")

    @classmethod
    def ensure_can_manage_colaborador(cls, usuario: dict | object, colaborador: object) -> None:
        def get_attr(obj, name):
            if isinstance(obj, dict):
                return obj.get(name)
            return getattr(obj, name, None)

        perfil_val = get_attr(usuario, "perfil")
        perfil = perfil_val.value if hasattr(perfil_val, "value") else str(perfil_val)

        if perfil in ("ADMIN", "RH"):
            return

        if perfil == "LIDER":
            setor_id = get_attr(usuario, "setor_id")
            if setor_id is not None and setor_id == get_attr(colaborador, "setor_id"):
                return
            raise ForbiddenError("Acesso negado.")

        raise ForbiddenError("Acesso negado.")

    @classmethod
    def ensure_can_access_recurso_do_colaborador(cls, usuario: dict | object, colaborador_id: int, colaboradores_repo: object) -> None:
        def get_attr(obj, name):
            if isinstance(obj, dict):
                return obj.get(name)
            return getattr(obj, name, None)

        perfil_val = get_attr(usuario, "perfil")
        perfil = perfil_val.value if hasattr(perfil_val, "value") else str(perfil_val)

        if perfil in ("ADMIN", "RH"):
            return

        colaborador = colaboradores_repo.get_by_id(colaborador_id)
        if not colaborador:
            raise NotFoundError("Colaborador nao encontrado.")

        cls.ensure_can_access_colaborador(usuario, colaborador)
