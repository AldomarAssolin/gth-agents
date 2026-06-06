from dataclasses import dataclass
from datetime import datetime

from werkzeug.security import check_password_hash

from domain.enums.perfil_usuario import PerfilUsuario


@dataclass(slots=True)
class Usuario:
    nome: str
    email: str
    senha_hash: str
    perfil: PerfilUsuario
    ativo: bool = True
    id: int | None = None
    colaborador_id: int | None = None
    setor_id: int | None = None
    criado_em: datetime | None = None


    def ativar(self) -> None:
        self.ativo = True

    def desativar(self) -> None:
        self.ativo = False

    def pode_avaliar(self) -> bool:
        return self.ativo and self.perfil in {
            PerfilUsuario.ADMIN,
            PerfilUsuario.RH,
            PerfilUsuario.LIDER,
            PerfilUsuario.COLABORADOR,
        }

    def eh_admin(self) -> bool:
        return self.perfil == PerfilUsuario.ADMIN

    def check_password_hash(self, senha: str) -> bool:
        return check_password_hash(self.senha_hash, senha)
