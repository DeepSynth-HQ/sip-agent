from src.agents.base import MetapoolAgent
class AgentServices:
    def __init__(self, user_id: str, session_id: str):
        self.agent_service = MetapoolAgent(user_id=user_id, session_id=session_id)
    def run(self, message: str, stream: bool = True, stream_intermediate_steps= True):
        return self.agent_service.run(message, stream=stream, stream_intermediate_steps= stream_intermediate_steps)
    