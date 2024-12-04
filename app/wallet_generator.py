
from web3 import Web3
from bitcoinlib.wallets import Wallet

def generate_ethereum_wallet():
    """
    Generate an Ethereum wallet.
    Returns:
        address (str): Ethereum wallet address.
        private_key (str): Private key for the wallet.
    """
    account = Web3().eth.account.create()
    private_key = account.privateKey.hex()
    address = account.address
    return address, private_key

def generate_bitcoin_wallet():
    """
    Generate a Bitcoin wallet.
    Returns:
        address (str): Bitcoin wallet address.
        private_key (str): Private key for the wallet.
    """
    wallet = Wallet.create(name='BTC_Wallet', keys='random', network='bitcoin')
    key = wallet.get_key()
    address = key.address
    private_key = key.private_hex
    return address, private_key
