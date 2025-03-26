from fastapi import FastAPI
from app.routes.agent import router as agent_router
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Request
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.errors import Error, ERROR_DETAILS
from fastapi.encoders import jsonable_encoder
from fastapi import status
from fastapi.responses import Response
from app.routes.auth import router as auth_router
from app.routes.user import router as user_router

app = FastAPI(
    title="Agent API",
)


class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {
                "error": ERROR_DETAILS[Error.VALIDATION_ERROR],
                "details": [
                    {"field": error["loc"][1], "message": error["msg"]}
                    for error in exc.errors()
                ],
                "body": exc.body,
            }
        ),
    )


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": ERROR_DETAILS[Error.HTTP_EXCEPTION],
            "details": exc.detail,
        },
    )


@app.middleware("http")
async def cors_handler(request: Request, call_next):
    if request.method == "OPTIONS":
        response = Response(
            status_code=204,
            headers={
                "Access-Control-Allow-Credentials": "true",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "*",
                "Access-Control-Allow-Headers": "*",
            },
        )
    else:
        response = await call_next(request)
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "*"

    return response


API_PREFIX_V1 = "/api/v1"
app.include_router(agent_router, prefix=API_PREFIX_V1)
app.include_router(auth_router, prefix=API_PREFIX_V1)
app.include_router(user_router, prefix=API_PREFIX_V1)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
