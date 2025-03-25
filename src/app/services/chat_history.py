from agents.chat.storage import storage
from app.dtos.chat_history import ChatHistoryDTO, Message
import re
from settings.log import logger


class ChatHistoryService:
    def __init__(self, user_id: str):
        self.storage = storage
        self.user_id = user_id

    def get_storage(self):
        return self.storage

    def _create_chat_history_dto(
        self, session_id: str, session, is_all: bool = False
    ) -> ChatHistoryDTO:
        history, created_at = self._extract_history(
            session_id, session.memory.get("runs", [])
        )

        if not history:
            return None

        title = (
            session.extra_data.get("title")
            if session.extra_data and session.extra_data.get("title")
            else self._regex_question_reasoning_answer(history[0].content)[0]
        )
        return ChatHistoryDTO(
            title=title,
            data=history if not is_all else None,
            created_at=created_at,
            session_id=session_id,
        )

    def _regex_question_reasoning_answer(self, message: str) -> tuple[str, str, str]:
        # Using re.DOTALL flag to match across multiple lines
        pattern = r"<question>(.*?)</question>.*?<reasoning>(.*?)</reasoning>.*?<answer>(.*?)</answer>"
        match = re.search(pattern, message, re.DOTALL)
        if match:
            # Strip whitespace from extracted content
            question = match.group(1).strip()
            reasoning = match.group(2).strip()
            answer = match.group(3).strip()
            return question, reasoning, answer
        return message, None, None

    def _extract_history(self, session_id: str, runs: list[dict]):
        history: list[Message] = []
        if not runs:
            return [], None

        created_at = runs[0].get("message", {}).get("created_at")

        for run in runs:
            message = run.get("message", {})
            response = run.get("response", {})

            user_message = message.get("content", "")
            question, reasoning, _ = self._regex_question_reasoning_answer(user_message)

            # Get images from first message only if it exists
            images_message = next(
                (
                    msg.get("images")
                    for msg in response.get("messages", [])
                    if msg.get("images")
                ),
                None,
            )

            agent_message = response.get("content")

            # Build messages list with conditional reasoning
            messages = [
                Message(role="user", content=question, images=images_message),
                Message(role="reasoning", content=reasoning) if reasoning else None,
                (
                    Message(role="assistant", content=agent_message)
                    if agent_message
                    else None
                ),
            ]

            # Add only non-None messages
            history.extend(msg for msg in messages if msg is not None)

        return history, created_at

    def _get_session(self, sessions: list, session_id: str):
        return next((s for s in sessions if s.session_id == session_id), None)

    def get_history(self, session_id: str, limit: int, offset: int):
        logger.debug(f"[HISTORY] - user_id: {self.user_id}, session_id: {session_id}")

        if session_id:
            logger.debug(f"[GET_HISTORY] - session_id: {session_id}")
            session = self.get_storage().read(session_id, self.user_id)
            if not session:
                logger.debug(
                    f"No session found for {session_id} and user {self.user_id}"
                )
                return None
            return self._create_chat_history_dto(session_id=session_id, session=session)

        logger.debug(
            f"[GET_HISTORY] - all sessions with offset: {offset}, limit: {limit}"
        )
        sessions = self.get_storage().get_all_sessions(self.user_id)
        # sorted by updated_at
        sessions = sorted(sessions, key=lambda x: x.updated_at, reverse=True)
        logger.debug(f"[HISTORY] Get all sessions")
        if not sessions:
            return []
        # Apply offset and limit before processing sessions
        paginated_sessions = sessions[offset : offset + limit]
        return [
            dto
            for session in paginated_sessions
            if (dto := self._create_chat_history_dto(session, is_all=True)) is not None
        ]

    def delete_conversation(self, session_id: str):
        session = self.get_storage().read(session_id, self.user_id)
        logger.debug(f"[DELETE_CONVERSATION] - session: {session_id}")

        if not session:
            return None
        self.get_storage().delete_session(session.session_id)
        return None

    def update_title(self, session_id: str, title: str):
        session = self.get_storage().read(session_id, self.user_id)
        logger.debug(
            f"[UPDATE_TITLE] - session: {session_id} - user_id: {self.user_id}"
        )
        if not session:
            return None
        logger.debug(f"Session: {session}")
        if not session.extra_data:
            session.extra_data = {}
        session.extra_data["title"] = title
        self.get_storage().upsert(session)
        return None
