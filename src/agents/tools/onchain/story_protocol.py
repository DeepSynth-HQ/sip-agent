from agno.tools import Toolkit
from .functions import OnChainFunctions


class StoryProtocolTool(Toolkit):
    def __init__(self):
        super().__init__("story_protocol_tools")
        self.register(
            OnChainFunctions.get_all_contracts,
        )
        self.register(
            OnChainFunctions.get_story_ip_stats,
        )
        self.register(
            OnChainFunctions.generate_wallet,
        )
