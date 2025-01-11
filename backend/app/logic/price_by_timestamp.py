import aiohttp

from typing import Optional

from fastapi.logger import logger
from web3 import Web3

from backend.app.core.config import settings
from backend.app.utils.helpers import get_rpc_url, get_token_pair_contract, get_abi


class ChainlinkGetPrice:
    def __init__(self, network: str, token_pair: str, timestamp: str, end_timestamp: str):
        self.network = network.lower()
        self.rpc_url, self.network_gas = get_rpc_url(self.network)
        self.web3 = Web3(Web3.HTTPProvider(self.rpc_url))
        self.chainlink_abi = get_abi("chainlink_feed_abi")
        self.token_pair = token_pair
        self.timestamp = timestamp
        self.end_timestamp = end_timestamp

        if not self.web3.is_connected():
            logger.error("Failed to connect to blockchain RPC.")
        
    async def get_local_round_id_by_timestamp(self, contract_address: str) -> Optional[str]:
        params = {
            "contractAddress": contract_address,
            "startTimestamp": self.timestamp,
            "endTimestamp": self.end_timestamp,
            "chain": self.network,
            "rpcUrl": self.rpc_url
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(settings.CHAINLIST_API_URL, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    phase_id = int(data["rounds"][0]["phaseId"])
                    local_round_id = int(data["rounds"][0]["roundId"])
                    return phase_id, local_round_id
                else:
                    logger.error(f"Failed to fetch price data. Status code: {response.status}")

    async def compute_global_round_id(self, phase_id: str, local_round_id: str) -> int:
        return (int(phase_id) << 64) | int(local_round_id)
    
    async def get_price_by_timestamp(self) -> Optional[float]:
        try:
            contract_address = await get_token_pair_contract(self.token_pair, self.network)
            phase_id, local_round_id = await self.get_local_round_id_by_timestamp(contract_address)
            round_id = await self.compute_global_round_id(phase_id=phase_id, local_round_id=local_round_id)
            contract = self.web3.eth.contract(address=self.web3.to_checksum_address(contract_address), abi=self.chainlink_abi)

            round_data = contract.functions.getRoundData(int(round_id)).call()
            decimals = contract.functions.decimals().call()

            price = float(round_data[1]) / (10 ** decimals)
            return price
        except Exception as e:
            logger.exception(f"An error occurred while fetching price from roundId: {e}")
            return None