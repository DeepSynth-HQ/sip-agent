from agno.tools import Toolkit
from .functions import OnChainFunctions


class StoryProtocolTool(Toolkit):
    def __init__(self):
        super().__init__("story_protocol_tools")
        self.register(
            self.get_all_contracts,
        )
        self.register(
            self.get_story_ip_stats,
        )
        self.register(
            self.generate_wallet,
        )

    def get_all_contracts(self) -> str:
        return OnChainFunctions.get_all_contracts().model_dump_json()

    def get_story_ip_stats(self) -> str:
        return OnChainFunctions.get_story_ip_stats().model_dump_json()

    def generate_wallet(self) -> str:
        return OnChainFunctions.generate_wallet().model_dump_json()
