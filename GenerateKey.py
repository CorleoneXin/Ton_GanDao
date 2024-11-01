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

class GenerateKey():
    tonClient = ToncenterClient
    db_account = None
    IS_TESTNET = bool
    def __init__(self, db:str, api_key:str, is_testNet:bool):
        db_name=f'db/{db}.db'
        self.db_account = dbconnect.DBSqlite(db_name)
        sql = f'CREATE TABLE BatchWallet (address CHAR(100) NOT NULL, privekey TEXT NOT NULL);'
        self.db_account.createTable(sql)
        
        self.tonClient = ToncenterClient(api_key, is_testNet)
        self.IS_TESTNET = is_testNet
    
    def GenerateKey(self, key_amount: int):
        for i in range(key_amount):
            wallet, public_key, private_key, mnemonic = WalletV5R1.create(self.tonClient)
            result = ' '.join(mnemonic)
            addr = wallet.address.to_str(True, True, False, self.IS_TESTNET)
            print(f"Address: {addr}")
            print(f"Memonic: {result}")
        
            sql = f"INSERT INTO BatchWallet VALUES"
            sql_value = " ('%s','%s')"%(addr ,result)
            sql_exec = sql + sql_value
            self.db_account.insertData(sql_exec)

        print('generate key success')    
        
    def showDB(self, retry_idx:int):
        sql_data = f"select * from BatchWallet"
        accounts = self.db_account.getData(sql_data)
        account_count  = len(accounts)
        for index in range(retry_idx, account_count):
            address = accounts[index][0]
            privkey = accounts[index][1]
            print(f"{index}-address: {address}")
            print(f" memnoic: {privkey}")