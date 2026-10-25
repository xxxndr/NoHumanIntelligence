import logging
from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger(__name__)

PROBLEM_JSON = "application/problem+json"
VALIDATION_TYPE = "urn:validation-error"


class FieldError(BaseModel):
    pointer: str
    detail: str
    code: str


class Problem(BaseModel):
    """RFC 9457 with custom 'errors' extension"""

    type: str = "about:blank"
    title: str
    status: int
    detail: str | None = None
    instance: str | None = None
    errors: list[FieldError] | None = None


def problem_response(
    request: Request,
    status: int,
    *,
    type: str = "about:blank",
    detail: str | None = None,
    errors: list[FieldError] | None = None,
    headers: dict[str, str] | None = None,
) -> JSONResponse:
    problem = Problem(
        type=type,
        title=HTTPStatus(status).phrase,
        status=status,
        detail=detail,
        instance=request.url.path,
        errors=errors,
    )
    return JSONResponse(
        problem.model_dump(exclude_none=True),
        status_code=status,
        media_type=PROBLEM_JSON,
        headers=headers,
    )


async def validation_handler(request: Request, exc: RequestValidationError):
    errors = [
        FieldError(
            pointer="/" + "/".join(str(p) for p in e["loc"]),
            detail=e["msg"],
            code=e["type"],
        )
        for e in exc.errors()
    ]
    return problem_response(
        request,
        HTTPStatus.UNPROCESSABLE_CONTENT,
        type=VALIDATION_TYPE,
        detail="La richiesta contiene campi non validi.",
        errors=errors,
    )


async def http_handler(request: Request, exc: StarletteHTTPException):
    return problem_response(
        request, exc.status_code, detail=str(exc.detail), headers=exc.headers
    )


async def unhandled_handler(request: Request, exc: Exception):
    logger.exception("errore non gestito su %s", request.url.path, exc_info=exc)
    return problem_response(
        request,
        HTTPStatus.INTERNAL_SERVER_ERROR,
        detail="Errore interno del server.",
    )


def install_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(RequestValidationError, validation_handler)
    app.add_exception_handler(StarletteHTTPException, http_handler)
    app.add_exception_handler(Exception, unhandled_handler)