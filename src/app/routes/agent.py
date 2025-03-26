from fastapi import APIRouter, Depends
from app.dtos.agent import AgentChatRequest
from app.handlers.agent import AgentHandler
from app.dtos.chat_history import UpdateTitleRequest
from app.handlers.chat_history import ChatHistoryHandler
from typing import Optional
from fastapi import Query
from app.models.user import User
from app.core.middlewares.auth import get_current_user

router = APIRouter(prefix="/agents", tags=["agents"])


@router.post("/chat")
def agent(request: AgentChatRequest, user: User = Depends(get_current_user)):
    agent_handler = AgentHandler()
    return agent_handler.run(request, user)


@router.post("/history/title")
def update_title(request: UpdateTitleRequest, user: User = Depends(get_current_user)):
    chat_history_handler = ChatHistoryHandler(user.id)
    return chat_history_handler.update_title(request.session_id, request.title)


@router.get("/history")
def get_history(
    session_id: Optional[str] = Query(None),
    limit: Optional[int] = Query(10, ge=1, le=100),
    offset: Optional[int] = Query(0, ge=0),
    user: User = Depends(get_current_user),
):
    chat_history_handler = ChatHistoryHandler(user.id)
    return chat_history_handler.get_chat_history(session_id, limit, offset)
