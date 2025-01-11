from enum import Enum


class NetworkSlug(str, Enum):
    MAINNET = 'mainnet'
    GOERLI = 'goerli'
    ARBITRUM = 'arbitrum'
    BSC = 'bsc'
    POLYGON = 'polygon'
    AVALANCHE = 'avalanche'
    FANTOM = 'fantom'
    MOONBEAM = 'moonbeam'
    MOONRIVER = 'moonriver'
    OPTIMISM = 'optimism'
    METIS = 'metis'
    GNOSIS = 'gnosis'

class NetworkURLs(str, Enum):
    MAINNET = "https://reference-data-directory.vercel.app/feeds-mainnet.json"
    ARBITRUM = "https://reference-data-directory.vercel.app/feeds-ethereum-mainnet-arbitrum-1.json"
    BSC = "https://reference-data-directory.vercel.app/feeds-bsc-mainnet.json"
    POLYGON = "https://reference-data-directory.vercel.app/feeds-matic-mainnet.json"
    AVALANCHE = "https://reference-data-directory.vercel.app/feeds-avalanche-mainnet.json"
    FANTOM = "https://reference-data-directory.vercel.app/feeds-fantom-mainnet.json"
    MOONBEAM = "https://reference-data-directory.vercel.app/feeds-polkadot-mainnet-moonbeam.json"
    MOONRIVER = "https://reference-data-directory.vercel.app/feeds-kusama-mainnet-moonriver.json"
    OPTIMISM = "https://reference-data-directory.vercel.app/feeds-ethereum-mainnet-optimism-1.json"
    METIS = "https://reference-data-directory.vercel.app/feeds-ethereum-mainnet-andromeda-1.json"
    GNOSIS = "https://reference-data-directory.vercel.app/feeds-xdai-mainnet.json"