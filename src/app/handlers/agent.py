from app.services.agent import AgentService
from app.dtos.agent import AgentChatRequest
import json
from fastapi.responses import StreamingResponse
from app.models.user import User


class AgentHandler:
    def __init__(self):
        self.agent_service = AgentService()

    def run(
        self,
        request: AgentChatRequest,
        user: User,
    ):
        def event_generator():
            aggregate_response = ""
            for chunk in self.agent_service.run(
                request.message,
                request.images,
                request.stream,
                user.id,
                request.session_id,
            ):
                if chunk.content_type == "str":
                    aggregate_response += str(chunk.content)
                data = {
                    "v": str(chunk.content),
                    "t": chunk.content_type,
                }
                yield f"event: {chunk.content_type}\ndata: {json.dumps(data)}\n\n"

            # Yield the final response
            data = {
                "v": aggregate_response,
            }
            yield f"event: end\ndata: {json.dumps(data)}\n\n"

        return StreamingResponse(event_generator(), media_type="text/event-stream")
