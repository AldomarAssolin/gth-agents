import os
from datetime import datetime, timedelta, timezone
import jwt


class JWTService:
    @staticmethod
    def gerar_token(usuario_id: int, email: str, perfil: str) -> str:
        secret = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret-change-me")
        algorithm = os.getenv("JWT_ALGORITHM", "HS256")
        expires_minutes = int(os.getenv("JWT_EXPIRES_MINUTES", "60"))

        now = datetime.now(timezone.utc)
        payload = {
            "id": usuario_id,
            "email": email,
            "perfil": perfil,
            "iat": now,
            "exp": now + timedelta(minutes=expires_minutes),
        }
        return jwt.encode(payload, secret, algorithm=algorithm)

    @staticmethod
    def decodificar_token(token: str) -> dict:
        secret = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret-change-me")
        algorithm = os.getenv("JWT_ALGORITHM", "HS256")
        return jwt.decode(token, secret, algorithms=[algorithm])
