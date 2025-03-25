from agents.base import agent


class AgentService:
    def __init__(self):
        self.agent = agent

    def run(
        self,
        message: str,
        images: list[str] = [],
        stream: bool = True,
        user_id: str = None,
        session_id: str = None,
    ):
        self.agent.user_id = user_id
        self.agent.session_id = session_id

        response = self.agent.run(message, images, stream)
        return response
