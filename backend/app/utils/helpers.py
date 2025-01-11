import json
import aiohttp

from pathlib import Path

from backend.app.core.config import settings
from fastapi.logger import logger

from backend.extra.network_slug import NetworkSlug, NetworkURLs


BASE_DIR = Path(__file__).resolve().parents[3]
NETWORKS_PATH = BASE_DIR / 'backend' / 'extra' / 'networks.json'


def get_abi(abi_name: str) -> list:
    project_root = Path(__file__).resolve().parents[3] 
    abi_path = project_root / 'backend' / 'extra' / 'abi' / f'{abi_name}.json'
    abi_path = abi_path.resolve()

    if not abi_path.is_file():
        raise FileNotFoundError(f"There is no ABI with this name: {abi_name}")
    
    with abi_path.open('r') as abi_file:
        abi = json.load(abi_file)
    return abi

def get_rpc_url(network_slug: str) -> tuple[str, str]:
    print(f"[network_slug]: {network_slug}")
    try:
        with open(NETWORKS_PATH, 'r') as network_file:
            data = json.load(network_file)
            for network in data['network']:
                if network['slug'] == network_slug:
                    network_rpc_url = network['rpc_url']
                    network_gas = network['settings']['MAX_GAS']
        return network_rpc_url, network_gas
    except Exception:
        raise Exception(f"No such network - {network_slug}")


async def get_token_pair_contract(token_pair: str, network: str):
    """Func to get address for token pair dynamically"""
    
    network_enum = NetworkSlug[network.upper()]
    url = NetworkURLs[network_enum.name].value
    print(f"[url]: {url}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                path_to_find = token_pair
                result = next((item for item in data if item.get("path") == path_to_find), None)
                if result:
                    proxy_address = result["proxyAddress"]
                    return proxy_address
                else:
                    logger.info(f"No data found for path '{path_to_find}'.")
            else:
                logger.info(f"Failed to fetch data. Status code - {response.status}")
