from fastapi import FastAPI
from app.routes.agent import router as agent_router
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Request
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.errors import Error, ERROR_DETAILS
from fastapi.encoders import jsonable_encoder
from fastapi import status

app = FastAPI()


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


API_PREFIX_V1 = "/api/v1"
app.include_router(agent_router, prefix=API_PREFIX_V1)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
