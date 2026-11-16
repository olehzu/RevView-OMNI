"""The one place failures become the section 8.2.3 error envelope (section 8.2.1).

Every failure is translated here, at the trust boundary, into a stable upper-case
code and a safe message. Exception details never reach the caller. An unavailable
external system keeps its name in ``source`` and is never reported as empty or passing.
"""

import logging
from collections.abc import Mapping

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.integration.common import IntegrationUnavailable

logger = logging.getLogger(__name__)


class AppError(Exception):
    """A failure the application reports to the caller with a stable code."""

    def __init__(self, status_code: int, code: str, message: str) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.message = message


def error_response(
    status_code: int,
    code: str,
    message: str,
    source: str | None = None,
    headers: Mapping[str, str] | None = None,
) -> JSONResponse:
    """Build the section 8.2.3 error envelope."""
    return JSONResponse(
        status_code=status_code,
        content={"error": {"code": code, "message": message, "source": source}},
        headers=headers,
    )


def _unavailable_code(source: str) -> str:
    return f"{source.upper()}_UNAVAILABLE"


async def _app_error(_: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, AppError)
    return error_response(exc.status_code, exc.code, exc.message)


async def _integration_unavailable(_: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, IntegrationUnavailable)
    return error_response(
        503,
        _unavailable_code(exc.source),
        f"{exc.source} is unavailable, so its evidence could not be read.",
        exc.source,
    )


async def _validation_failed(_: Request, __: Exception) -> JSONResponse:
    return error_response(422, "VALIDATION_FAILED", "The request is not valid.")


_HTTP_CODES = {404: "NOT_FOUND", 405: "METHOD_NOT_ALLOWED"}
_HTTP_MESSAGES = {
    404: "The requested resource does not exist.",
    405: "The method is not allowed on this resource.",
}


async def _http_error(_: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, StarletteHTTPException)
    return error_response(
        exc.status_code,
        _HTTP_CODES.get(exc.status_code, "REQUEST_FAILED"),
        _HTTP_MESSAGES.get(exc.status_code, "The request could not be completed."),
        headers=exc.headers,  # for example the Allow header of a 405
    )


async def _internal_error(request: Request, exc: Exception) -> JSONResponse:
    # The path and exception type only: never request bodies, source, or diff content (8.2.7).
    logger.error(
        "unhandled error path=%s type=%s", request.url.path, type(exc).__name__
    )
    return error_response(500, "INTERNAL_ERROR", "An unexpected error occurred.")


def register_error_handlers(app: FastAPI) -> None:
    """Install the envelope translation on the application."""
    app.add_exception_handler(AppError, _app_error)
    app.add_exception_handler(IntegrationUnavailable, _integration_unavailable)
    app.add_exception_handler(RequestValidationError, _validation_failed)
    app.add_exception_handler(StarletteHTTPException, _http_error)
    app.add_exception_handler(Exception, _internal_error)
