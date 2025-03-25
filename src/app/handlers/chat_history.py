from app.services.chat_history import ChatHistoryService
from app.dtos.chat_history import ChatHistoryDTO


class ChatHistoryHandler:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.service = ChatHistoryService(user_id)

    def get_chat_history(
        self, session_id: str, limit: int, offset: int
    ) -> ChatHistoryDTO:
        return self.service.get_history(session_id, limit, offset)

    def update_title(self, session_id: str, title: str) -> None:
        return self.service.update_title(session_id, title)
