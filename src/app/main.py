from fastapi import FastAPI
from app.routes.agent import router as agent_router

app = FastAPI()
API_PREFIX_V1 = "/api/v1"
app.include_router(agent_router, prefix=API_PREFIX_V1)
