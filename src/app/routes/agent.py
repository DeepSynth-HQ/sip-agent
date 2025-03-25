from fastapi import APIRouter
from app.dtos.agent import AgentChatRequest
from app.handlers.agent import AgentHandler

router = APIRouter(prefix="/agents")


@router.post("/chat")
def agent(request: AgentChatRequest):
    agent_handler = AgentHandler()
    return agent_handler.run(request)
