from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class AppException(Exception):
    """Exception cơ bản dùng chung cho toàn app."""

    def __init__(self, status_code: int, message: str, detail: str | None = None):
        self.status_code = status_code
        self.message = message
        self.detail = detail


class NotFoundException(AppException):
    def __init__(self, message: str = "Resource not found", detail: str | None = None):
        super().__init__(status.HTTP_404_NOT_FOUND, message, detail)


class BadRequestException(AppException):
    def __init__(self, message: str = "Bad request", detail: str | None = None):
        super().__init__(status.HTTP_400_BAD_REQUEST, message, detail)


class ForbiddenException(AppException):
    def __init__(self, message: str = "Forbidden", detail: str | None = None):
        super().__init__(status.HTTP_403_FORBIDDEN, message, detail)


def error_response(
    status_code: int, message: str, detail: str | None = None
) -> JSONResponse:
    """Format lỗi thống nhất cho toàn bộ app."""
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "error": {
                "code": status_code,
                "message": message,
                "detail": detail,
            },
        },
    )


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return error_response(exc.status_code, exc.message, exc.detail)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        return error_response(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Validation error",
            str(exc.errors()),
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        return error_response(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Internal server error",
            str(exc) if app.debug else None,
        )
