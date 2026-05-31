from flask import jsonify
from werkzeug.exceptions import HTTPException

from application.errors import AppError


def register_error_handlers(app):
    @app.errorhandler(AppError)
    def handle_app_error(error: AppError):
        return jsonify({"error": error.code, "message": error.message}), error.status_code

    @app.errorhandler(ValueError)
    def handle_value_error(error: ValueError):
        return jsonify({"error": "VALIDATION_ERROR", "message": str(error)}), 400

    @app.errorhandler(HTTPException)
    def handle_http_exception(error: HTTPException):
        return jsonify({"error": error.name.upper().replace(" ", "_"), "message": error.description}), error.code

    @app.errorhandler(Exception)
    def handle_unexpected_error(error: Exception):
        app.logger.exception(error)
        return jsonify({"error": "INTERNAL_SERVER_ERROR", "message": "Erro interno no servidor."}), 500
