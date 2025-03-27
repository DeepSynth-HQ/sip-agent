from agno.tools import Toolkit
from .functions import OnChainFunctions
from agno.agent import Agent


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
        self.register(
            self.get_top_liquidity_protocols,
        )
        self.register(
            self.get_top_lending_protocols,
        )
        self.register(
            self.get_top_tvl_protocols,
        )
        self.register(
            self.get_trending_contracts,
        )
        self.register(
            self.get_contract_info,
        )
        self.register(
            self.staking,
        )
        self.register(
            self.unstaking,
        )

    def get_all_contracts(self) -> str:
        """Get all contracts on the Story Protocol network.

        Returns:
            str: The all contracts on the Story Protocol network.
        """
        return OnChainFunctions.get_all_contracts().model_dump_json()

    def get_story_ip_stats(self) -> str:
        """Get stats about the Story Protocol network.

        Returns:
            str: The stats about the Story Protocol network.
        """
        return OnChainFunctions.get_story_ip_stats().model_dump_json()

    def generate_wallet(self) -> str:
        """Generate a new wallet on the Story Protocol network.

        Returns:
            str: The new wallet on the Story Protocol network.
        """
        return OnChainFunctions.generate_wallet().model_dump_json()

    def get_top_liquidity_protocols(self, limit: int = 3) -> str:
        """Get top liquidity protocols on the Story Protocol network.

        Args:
            limit (int, optional): The number of top liquidity protocols to return. Defaults to 3.

        Returns:
            str: The top liquidity protocols on the Story Protocol network.
        """
        return OnChainFunctions.get_top_liquidity_protocols(
            limit=limit
        ).model_dump_json()

    def get_top_lending_protocols(self, limit: int = 3) -> str:
        """Get top lending protocols on the Story Protocol network.

        Args:
            limit (int, optional): The number of top lending protocols to return. Defaults to 3.

        Returns:
            str: The top lending protocols on the Story Protocol network.
        """
        return OnChainFunctions.get_top_lending_protocols(limit=limit).model_dump_json()

    def get_top_tvl_protocols(self, limit: int = 3) -> str:
        """Get top tvl (total value locked) protocols on the Story Protocol network.

        Args:
            limit (int, optional): The number of top tvl protocols to return. Defaults to 3.

        Returns:
            str: The top tvl protocols on the Story Protocol network.
        """
        return OnChainFunctions.get_top_tvl_protocols(limit=limit).model_dump_json()

    def get_trending_contracts(self, limit: int = 3) -> str:
        """Get trending contracts on the Story Protocol network.

        Args:
            limit (int, optional): The number of trending contracts to return. Defaults to 3.

        Returns:
            str: The trending contracts on the Story Protocol network.
        """
        return OnChainFunctions.get_trending_contracts(limit=limit).model_dump_json()

    def get_contract_info(self, address: str) -> str:
        """Get information about a specific contract on the Story Protocol network.

        Args:
            address (str): The address of the contract to get information about.

        Returns:
            str: The information about the contract on the Story Protocol network.
        """
        return OnChainFunctions.get_contract_info(address=address).model_dump_json()

    def staking(self, agent: Agent, amount: float) -> str:
        """Stake tokens on the Story Protocol network.

        Args:
            receiver (str): The address to receive the staked tokens (stIP)
            amount (float): The amount of tokens to stake

        Returns:
            str: The staking response on the Story Protocol network.
        """
        user_id = agent.context.get("user_id", None)
        if not user_id:
            raise ValueError("User ID is not set")
        return OnChainFunctions.staking(
            receiver=user_id, amount=amount
        ).model_dump_json()

    def unstaking(self, agent: Agent, amount: float) -> str:
        """Unstake tokens on the Story Protocol network.

        Args:
            amount (float): The amount of tokens to unstake

        Returns:
            str: The unstaking response on the Story Protocol network.
        """
        user_id = agent.context.get("user_id", None)
        if not user_id:
            raise ValueError("User ID is not set")
        return OnChainFunctions.unstaking(
            receiver=user_id, amount=amount
        ).model_dump_json()
