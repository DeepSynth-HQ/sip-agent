import requests
from typing import Optional, Generic, TypeVar, List, Dict, Any
from settings.config import config
from pydantic import BaseModel, Field, RootModel
from settings.log import logger

T = TypeVar("T")


class BaseResponse(BaseModel, Generic[T]):
    status: bool
    data: Optional[T]
    code: int


class GenerateWalletResponse(BaseModel):
    mnemonic: str
    address: str
    private_key: str = Field(alias="privateKey")


class StoryIpStatsResponse(BaseModel):
    average_block_time: int
    coin_image: str
    coin_price: str
    coin_price_change_percentage: float
    gas_price_updated_at: str
    gas_prices: dict
    gas_prices_update_in: int
    gas_used_today: str
    market_cap: str
    network_utilization_percentage: float
    secondary_coin_image: Optional[str]
    secondary_coin_price: Optional[str]
    static_gas_price: Optional[str]
    total_addresses: str
    total_blocks: str
    total_gas_used: str
    total_transactions: str
    transactions_today: str
    tvl: Optional[str]


class ContractImplementation(BaseModel):
    address: str
    name: Optional[str] = None


class ContractAddress(BaseModel):
    ens_domain_name: Optional[str]
    hash: str
    implementations: List[ContractImplementation]
    is_contract: bool
    is_scam: bool
    is_verified: bool
    metadata: Optional[Any]
    name: str
    private_tags: List[str]
    proxy_type: Optional[str]
    public_tags: List[str]
    watchlist_names: List[str]


class ContractInfo(BaseModel):
    address: ContractAddress
    certified: bool
    coin_balance: str
    compiler_version: str
    has_constructor_args: bool
    language: str
    license_type: str
    market_cap: Optional[str]
    optimization_enabled: bool
    transaction_count: Optional[int]
    verified_at: str


class TrendingContractInfo(ContractInfo):
    contract: str
    total_transactions_in_1d: int = Field(alias="totalTransactionsIn1d")


class ContractsResponse(BaseModel):
    items: List[ContractInfo]
    next_page_params: Optional[Dict[str, Any]]


class TrendingContractsResponse(RootModel[List[TrendingContractInfo]]):
    pass


class ContractInfoResponse(BaseModel):
    """Model for the contract info endpoint response which has a different structure."""

    address: str
    implementations: List[ContractImplementation]
    is_contract: bool
    is_verified: bool
    name: Optional[str] = None
    ens_domain_name: Optional[str] = None
    is_scam: bool = False
    metadata: Optional[Any] = None
    private_tags: List[str] = Field(default_factory=list)
    proxy_type: Optional[str] = None
    public_tags: List[str] = Field(default_factory=list)
    watchlist_names: List[str] = Field(default_factory=list)


class OracleBreakdown(BaseModel):
    name: str
    type: str
    proof: List[str]


class BaseProtocol(BaseModel):
    """Base model for all protocol types to reduce duplication."""

    id: str
    name: str
    address: Optional[str] = None
    symbol: str
    url: str
    description: str
    chain: str
    logo: str
    audits: str
    audit_note: Optional[str] = None
    gecko_id: Optional[str] = None
    cmc_id: Optional[str] = Field(alias="cmcId", default=None)
    category: str
    chains: List[str]
    oracles: List[str] = Field(default_factory=list)
    oracles_breakdown: Optional[List[OracleBreakdown]] = Field(
        alias="oraclesBreakdown", default=None
    )
    forked_from: List[str] = Field(alias="forkedFrom", default_factory=list)
    module: str
    twitter: Optional[str] = None
    audit_links: Optional[List[str]] = Field(alias="audit_links", default_factory=list)
    listed_at: Optional[int] = Field(alias="listedAt", default=None)
    methodology: Optional[str] = None
    slug: str
    tvl: float
    chain_tvls: Dict[str, float] = Field(alias="chainTvls")
    change_1h: str
    change_1d: str
    change_7d: str
    token_breakdowns: Dict[str, Any] = Field(
        alias="tokenBreakdowns", default_factory=dict
    )
    mcap: Optional[float] = None
    # Optional fields that may be present in some protocol types
    parent_protocol: Optional[str] = Field(alias="parentProtocol", default=None)
    github: Optional[List[str]] = None
    asset_token: Optional[str] = Field(alias="assetToken", default=None)


class LiquidityProtocol(BaseProtocol):
    """Liquidity protocol model with required asset_token field."""

    asset_token: str = Field(alias="assetToken")


class LendingProtocol(BaseProtocol):
    """Lending protocol model."""

    pass


class TvlProtocol(BaseProtocol):
    """TVL protocol model."""

    pass


class StakingResponse(BaseModel):
    tx_hash: str = Field(alias="txHash")


class CheckBalanceResponse(BaseModel):
    balance: str


class OnChainFunctions:
    @staticmethod
    def generate_wallet() -> BaseResponse[GenerateWalletResponse]:
        """
        Generate a wallet for story protocol. This function will return the mnemonic, address, and private key.

        Returns:
            BaseResponse[GenerateWalletResponse]: Generate wallet response
        """
        response = requests.get(
            f"{config.STORY_PROTOCOL_API_BASE_URL}/evm/story/testnet/generate-wallet",
        )
        return BaseResponse[GenerateWalletResponse].model_validate(response.json())

    @staticmethod
    def get_story_ip_stats() -> BaseResponse[StoryIpStatsResponse]:
        """
        Get story ip stats. This function will return the story ip stats. Including the average block time, gas price, gas used today, total addresses, total blocks, total gas used, total transactions, transactions today, tvl, etc.

        Returns:
            BaseResponse[StoryIpStatsResponse]: Story ip stats
        """
        response = requests.get(
            f"{config.STORY_PROTOCOL_API_BASE_URL}/evm/story/mainnet/stats",
        )
        return BaseResponse[StoryIpStatsResponse].model_validate(response.json())

    @staticmethod
    def get_all_contracts() -> BaseResponse[ContractsResponse]:
        """
        Get all verified contracts on the Story Protocol network.

        Returns:
            BaseResponse[ContractsResponse]: Contracts response
        """
        response = requests.get(
            f"{config.STORY_PROTOCOL_API_BASE_URL}/evm/story/mainnet/stats/all-contracts",
        )
        json_response = response.json()
        return BaseResponse[ContractsResponse].model_validate(json_response)

    @staticmethod
    def get_trending_contracts(
        limit: int = 3,
    ) -> BaseResponse[List[TrendingContractInfo]]:
        """
        Get trending contracts on the Story Protocol network.

        Args:
            limit (int): The top N trending contracts to return.

        Returns:
            BaseResponse[List[TrendingContractInfo]]: Trending contracts
        """
        response = requests.get(
            f"{config.STORY_PROTOCOL_API_BASE_URL}/evm/story/testnet/contract/trending",
            params={"limit": limit},
        )
        return BaseResponse[List[TrendingContractInfo]].model_validate(response.json())

    @staticmethod
    def get_contract_info(address: str) -> BaseResponse[ContractInfoResponse]:
        """
        Get contract info by address.

        Args:
            address (str): The contract address to look up

        Returns:
            BaseResponse[ContractInfoResponse]: Contract information
        """
        response = requests.get(
            f"{config.STORY_PROTOCOL_API_BASE_URL}/evm/story/testnet/contract/find/{address}",
        )
        return BaseResponse[ContractInfoResponse].model_validate(response.json())

    @staticmethod
    def get_top_liquidity_protocols(
        limit: int = 3,
    ) -> BaseResponse[List[LiquidityProtocol]]:
        """
        Get top liquidity protocols on the Story Protocol network.

        Args:
            limit (int): The top N liquidity protocols to return.

        Returns:
            BaseResponse[List[LiquidityProtocol]]: Top liquidity protocols
        """
        response = requests.get(
            f"{config.STORY_PROTOCOL_API_BASE_URL}/evm/story/testnet/pool/topLPStaking",
            params={"limit": limit},
        )
        return BaseResponse[List[LiquidityProtocol]].model_validate(response.json())

    @staticmethod
    def get_top_lending_protocols(
        limit: int = 3,
    ) -> BaseResponse[List[LendingProtocol]]:
        """
        Get top lending protocols on the Story Protocol network.
        """
        response = requests.get(
            f"{config.STORY_PROTOCOL_API_BASE_URL}/evm/story/testnet/pool/topLending",
            params={"limit": limit},
        )
        return BaseResponse[List[LendingProtocol]].model_validate(response.json())

    @staticmethod
    def get_top_tvl_protocols(limit: int = 3) -> BaseResponse[List[TvlProtocol]]:
        """
        Get top tvl (total value locked) protocols on the Story Protocol network.
        """
        response = requests.get(
            f"{config.STORY_PROTOCOL_API_BASE_URL}/evm/story/testnet/pool/topTvl",
            params={"limit": limit},
        )
        return BaseResponse[List[TvlProtocol]].model_validate(response.json())

    @staticmethod
    def staking(receiver: str, amount: float) -> BaseResponse[StakingResponse]:
        """
        Stake tokens on the Story Protocol network.

        Args:
            receiver (str): The address to receive the staked tokens (stIP)
            amount (float): The amount of tokens to stake

        Returns:
            BaseResponse[StakingResponse]: Staking response
        """
        response = requests.post(
            f"{config.STORY_PROTOCOL_API_BASE_URL}/evm/story/mainnet/metapool/staking",
            json={"receiver": receiver, "amount": str(amount)},
        )
        return BaseResponse[StakingResponse].model_validate(response.json())

    @staticmethod
    def unstaking(receiver: str, amount: float) -> BaseResponse[StakingResponse]:
        """
        Unstake tokens on the Story Protocol network.

        Args:
            receiver (str): The address to receive the unstaked tokens
            amount (float): The amount of shares to unstake

        Returns:
            BaseResponse[StakingResponse]: Unstaking response
        """
        response = requests.post(
            f"{config.STORY_PROTOCOL_API_BASE_URL}/evm/story/mainnet/metapool/unstaking",
            json={"receiver": receiver, "owner": receiver, "shares": str(amount)},
        )
        return BaseResponse[StakingResponse].model_validate(response.json())

    @staticmethod
    def check_erc20_balance(
        address: str, token_address: str
    ) -> BaseResponse[CheckBalanceResponse]:
        """
        Check the balance of an ERC20 token for a given address.

        Args:
            address (str): The address to check the balance of
            token_address (str): The address of the ERC20 token

        Returns:
            BaseResponse[CheckBalanceResponse]: Check balance response
        """
        response = requests.get(
            f"{config.STORY_PROTOCOL_API_BASE_URL}/evm/story/testnet/erc20-balance/{address}/{token_address}",
        )
        return BaseResponse[CheckBalanceResponse].model_validate(response.json())

    @staticmethod
    def check_sepolia_balance(address: str) -> BaseResponse[CheckBalanceResponse]:
        """
        Check the balance of an address on the Sepolia testnet.
        """
        response = requests.get(
            f"{config.STORY_PROTOCOL_API_BASE_URL}/evm/story/testnet/balance/{address}",
        )
        return BaseResponse[CheckBalanceResponse].model_validate(response.json())


if __name__ == "__main__":
    print(
        OnChainFunctions.unstaking(
            "0x783FC27915754512E72b5811599504eCa458E4C5",
            0.1,
        )
    )
