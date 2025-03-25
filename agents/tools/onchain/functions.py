import requests
from typing import Optional, Generic, TypeVar, List, Dict, Any
from settings.config import config
from pydantic import BaseModel, Field
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
    name: str


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


class ContractsResponse(BaseModel):
    items: List[ContractInfo]
    next_page_params: Optional[Dict[str, Any]]


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


if __name__ == "__main__":
    print(OnChainFunctions.get_all_contracts())
