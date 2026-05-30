class AppError(Exception):
    def __init__(self, message: str, status_code: int = 400, code: str = "APP_ERROR"):
        self.message = message
        self.status_code = status_code
        self.code = code
        super().__init__(message)


class NotFoundError(AppError):
    def __init__(self, message: str):
        super().__init__(message, 404, "NOT_FOUND")


class ConflictError(AppError):
    def __init__(self, message: str):
        super().__init__(message, 409, "CONFLICT")


class ValidationError(AppError):
    def __init__(self, message: str):
        super().__init__(message, 400, "VALIDATION_ERROR")
