from modules import dbconnect
# ton package
from pytoniq_core import Address, begin_cell,VmTuple
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

import asyncio

class BatchOption():
    tonClient = ToncenterClient
    db_account = None
    IS_TESTNET = bool
    
    def __init__(self, db:str, api_key:str, is_testNet:bool):
        db_name=f'db/{db}.db'
        self.db_account = dbconnect.DBSqlite(db_name)
        self.tonClient = ToncenterClient(api_key, is_testNet)
        self.IS_TESTNET = is_testNet
        
    def get_addr_balance(self, addr:str):
        res = asyncio.run(self.tonClient.run_get_method(addr, 'TonBalance'))
        print(f"Query result is: {res}")
        hex_value = res['stack'][0]['value']
        integer_value = int(hex_value, 16)
        print(f"TonBalance is: {integer_value}")
        pass
    
    def get_token_balance(self, addr:str, jettonMaster: str):
        jetton_wallet_address = asyncio.run(JettonMaster.get_wallet_address(
            client=self.tonClient,
            owner_address=addr,
            jetton_master_address=jettonMaster,
        ))
        # get Jetton Balance
        jetton_wallet_data = asyncio.run(JettonWallet.get_wallet_data(
            client=self.tonClient,
            jetton_wallet_address=jetton_wallet_address,
        ))

        print(f"Jetton wallet data): {jetton_wallet_data}")
        print(f"Jetton wallet balance (Jettons): {jetton_wallet_data.balance}")
        pass
    
    
    def batch_transfer_ton(self, masterKey:str, amount:float, retryIdx:int):
        sql_data = f"select * from BatchWallet"
        accounts = self.db_account.getData(sql_data)
        account_count  = len(accounts)

        wallet, public_key, private_key, mnemonic   = WalletV5R1.from_mnemonic(self.tonClient, masterKey);
        for index in range(retryIdx, account_count):
            addr = accounts[index][0]
            # privKey = accounts[index][1]
            # wallet_target, public_key, private_key, mnemonic   = WalletV5R1.from_mnemonic(self.tonClient, privKey);
            # print(wallet_target.address.to_str(True, True, False, self.IS_TESTNET))
        
            tx_hash = asyncio.run(wallet.transfer(
                destination=addr,
                amount = amount,
                body="Tx Ton",
            ))
    
            print(f'Processing Tx : {index} - {addr}')
            print(f'{tx_hash}')

        
    def batch_transfer_jetton(self, masterKey:str,jettonMaster:str, jtamount:float, retryIdx:int):
        sql_data = f"select * from BatchWallet"
        accounts = self.db_account.getData(sql_data)
        account_count  = len(accounts)

        wallet, public_key, private_key, mnemonic   = WalletV5R1.from_mnemonic(self.tonClient, masterKey);
        print(wallet.address.to_str(True, True, False, self.IS_TESTNET))
        for index in range(retryIdx, account_count):
            addr = accounts[index][0]
            # privKey = accounts[index][1]
            # wallet_target, public_key, private_key, mnemonic   = WalletV5R1.from_mnemonic(self.tonClient, privKey);
            # print(wallet_target.address.to_str(True, True, False, self.IS_TESTNET))
            # 获取jetton_wallet_src
            jetton_wallet_address = asyncio.run(JettonMaster.get_wallet_address(
                client=self.tonClient,
                owner_address=wallet.address.to_str(),
                jetton_master_address=jettonMaster,
            ))
            # 构建交易
            body = JettonWallet.build_transfer_body(
                recipient_address=addr,
                response_address=wallet.address,
                jetton_amount=int(jtamount),
                forward_payload=(
                    begin_cell()
                    .store_uint(0, 32)  # Text comment opcode
                    .store_snake_string("Tx Jetton")
                    .end_cell()
                ),
                forward_amount=1,
            )
            # 将消息发送到 对应的jetton钱包
            tx_hash = asyncio.run(wallet.transfer(
                destination=jetton_wallet_address,
                amount=0.05,
                body=body,
            ))
            print(f'Processing Tx : {index} - {addr}')
            print(f'{tx_hash}')
        