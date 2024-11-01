import asyncio

# ton package
from pytoniq_core import Address, begin_cell,VmTuple, Cell
from tonutils.utils import to_amount, to_nano
from tonutils.jetton import JettonMaster, JettonWallet
from tonutils.client import ToncenterClient
from tonutils.wallet import (
    WalletV3R1,
    # Uncomment the following lines to use different wallet versions:
    WalletV3R2,
    WalletV4R1,
    WalletV4R2,
    WalletV5R1,
    HighloadWalletV2,
    HighloadWalletV3,
)


# NOTE: 这个合约模版使用的admin地址类型是v4r2，具体调用时，需要使用对应的钱包地址的对应版本，此处的合约wallet不具备普适性
class ContractTemplate():
    tonClient = ToncenterClient
    IS_TESTNET = bool
    CONTRACT_ADDRESS = str
    
    def __init__(self, api_key:str, is_testNet:bool, cnt_addr:str):
        self.tonClient = ToncenterClient(api_key, is_testNet)
        self.IS_TESTNET = is_testNet
        self.CONTRACT_ADDRESS = cnt_addr
        
    def onWithdrawNativeClicked(self, masterKey : str, amount:float):
        tonAmount = float(amount)
        print(tonAmount)
        
        wallet, public_key, private_key, mnemonic  = WalletV4R2.from_mnemonic(self.tonClient, masterKey, 698983191);
        print(f"exitWallet Address: {wallet.address.to_str(True, True, False, True)}")
        payload = (begin_cell()
        .store_uint(195467089, 32)
        .store_coins(to_nano(tonAmount))
        .end_cell())
        body = (begin_cell().store_cell(payload).end_cell());
        # Send Tx
        tx_hash = asyncio.run(wallet.transfer(
            destination=self.CONTRACT_ADDRESS,
            amount= 0.1,
            body=body
        ))

        print(f"Transaction hash: {tx_hash}")

    def onQueryStatusClicked(self):
        res = asyncio.run(self.client.run_get_method(self.CONTRACT_ADDRESS, 'stopped'));
        print(f"res is: {res}")
        hex_value = res['stack'][0]['value']
        
        integer_value = int(hex_value, 16)
        print(f"Stop Status : {integer_value}")
    
    
    def onStopClicked(self, masterKey : str):

        wallet, public_key, private_key, mnemonic  = WalletV4R2.from_mnemonic(self.tonClient, masterKey, 698983191);
        print(f"exitWallet Address: {wallet.address.to_str(True, True, False, True)}")

        body = (begin_cell()
        .store_uint(0, 32)
        .store_string("Stop")
        .end_cell())
        # Send Tx
        tx_hash = asyncio.run(wallet.transfer(
            destination=self.CONTRACT_ADDRESS,
            amount= 0.01,
            body=body
        ))
        print(f"Transaction hash: {tx_hash}")
        
    def onResumeClicked(self, masterKey : str):

        wallet, public_key, private_key, mnemonic  = WalletV4R2.from_mnemonic(self.tonClient, masterKey, 698983191);
        print(f"exitWallet Address: {wallet.address.to_str(True, True, False, True)}")

        body = (begin_cell()
        .store_uint(0, 32)
        .store_string("Resume")
        .end_cell())
        # Send Tx
        tx_hash = asyncio.run(wallet.transfer(
            destination=self.CONTRACT_ADDRESS,
            amount= 0.01,
            body=body
        ))
        print(f"Transaction hash: {tx_hash}")
