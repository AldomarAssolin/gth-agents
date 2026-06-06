from functools import wraps
from flask import request, g, jsonify, current_app
import jwt
from infrastructure.security.jwt_service import JWTService


def obter_usuario_da_requisicao() -> dict:
    if hasattr(g, "usuario") and g.usuario:
        return g.usuario

    auth_header = request.headers.get("Authorization")

    # Bypass auth in testing environment unless X-Enforce-Auth is requested
    if current_app.config.get("TESTING") and not request.headers.get("X-Enforce-Auth"):
        payload = {
            "id": 1,
            "email": "admin@empresa.com",
            "perfil": "ADMIN",
        }
        g.usuario = payload
        return payload

    if not auth_header:
        raise jwt.InvalidTokenError("Token de acesso obrigatorio.")

    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise jwt.InvalidTokenError("Formato de token invalido.")

    token = parts[1]
    payload = JWTService.decodificar_token(token)
    g.usuario = payload
    return payload


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            obter_usuario_da_requisicao()
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "UNAUTHORIZED", "message": "Token expirado."}), 401
        except jwt.InvalidTokenError as e:
            return jsonify({"error": "UNAUTHORIZED", "message": str(e)}), 401
        except Exception:
            return jsonify({"error": "UNAUTHORIZED", "message": "Token invalido."}), 401
        return f(*args, **kwargs)
    return decorated


def roles_required(*roles):
    role_names = {r.value if hasattr(r, "value") else str(r) for r in roles}

    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            try:
                usuario = obter_usuario_da_requisicao()
            except jwt.ExpiredSignatureError:
                return jsonify({"error": "UNAUTHORIZED", "message": "Token expirado."}), 401
            except jwt.InvalidTokenError as e:
                return jsonify({"error": "UNAUTHORIZED", "message": str(e)}), 401
            except Exception:
                return jsonify({"error": "UNAUTHORIZED", "message": "Token invalido."}), 401

            user_role = usuario.get("perfil")
            if user_role not in role_names:
                return jsonify({"error": "FORBIDDEN", "message": "Perfil insuficiente."}), 403

            return f(*args, **kwargs)
        return decorated
    return decorator
