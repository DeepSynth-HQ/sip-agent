from app.services.agent import AgentServices
from app.dtos.agent import AgentChatRequest
import json
from fastapi.responses import StreamingResponse


class AgentHandler:
    def __init__(self):
        self.agent_service = AgentServices()

    def run(
        self,
        request: AgentChatRequest,
    ):
        def event_generator():
            aggregate_response = ""
            for chunk in self.agent_service.run(message = request.message, stream = True, stream_intermediate_steps=True):
                if chunk.content_type == "answer":
                    aggregate_response += str(chunk.content)
                data = {
                    "v": str(chunk.content),
                    "t": chunk.content_type,
                }
                yield f"event: {chunk.content_type}\ndata: {json.dumps(data)}\n\n"
            data = {
                "v": aggregate_response,
            }
            yield f"event: end\ndata: {json.dumps(data)}\n\n"

        return StreamingResponse(event_generator(), media_type="text/event-stream")

