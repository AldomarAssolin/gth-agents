from application.dtos.auth_dto import LoginDTO
from application.errors import UnauthorizedError, ForbiddenError
from application.ports.usuario_repository import UsuarioRepository
from infrastructure.security.jwt_service import JWTService


class LoginUsuarioUC:
    def __init__(self, usuarios_repo: UsuarioRepository):
        self.usuarios_repo = usuarios_repo

    def execute(self, dto: LoginDTO) -> dict:
        usuario = self.usuarios_repo.get_by_email(dto.email)
        if not usuario:
            raise UnauthorizedError("Credenciais invalidas.")

        if not usuario.check_password_hash(dto.senha):
            raise UnauthorizedError("Credenciais invalidas.")

        if not usuario.ativo:
            raise ForbiddenError("Usuario inativo.")

        token = JWTService.gerar_token(usuario.id, usuario.email, usuario.perfil.value)

        return {
            "access_token": token,
            "token_type": "Bearer",
            "usuario": usuario,
        }
