import os
from dotenv import load_dotenv

load_dotenv('.env')

DB_NAME = os.getenv("DB_NAME")
GERERATE_KEY_AMOUNT = os.getenv("GERERATE_KEY_AMOUNT")
API_KEY = os.getenv("API_KEY")
IS_TESTNET = os.getenv("IS_TESTNET")
MASTER_ADDR = os.getenv("MASTER_ADDR")
MASTER_KEY = os.getenv("MASTER_KEY")
TRANSFER_AMOUNT = os.getenv("TRANSFER_AMOUNT")
CONTRACT_ADDR = os.getenv("CONTRACT_ADDR")
CONTRACT_ABI = os.getenv("CONTRACT_ABI")
JETTON_MASTER = os.getenv("JETTON_MASTER")

print(f'DB_NAME : {DB_NAME}')
print(f'GERERATE_KEY_AMOUNT : {GERERATE_KEY_AMOUNT}')
print(f'API_KEY : {API_KEY}')
print(f'IS_TESTNET : {IS_TESTNET}')
# print(f'MASTER_KEY : {MASTER_KEY}')
print(f'MASTER_ADDR : {MASTER_ADDR}')
print(f'TRANSFER_AMOUNT : {TRANSFER_AMOUNT}')
print(f'CONTRACT_ADDR : {CONTRACT_ADDR}')
print(f'CONTRACT_ABI : {CONTRACT_ABI}')
print(f'JETTON_MASTER : {JETTON_MASTER}')

import GenerateKey
import Batchoption
from contract import interctContract

def batchOp():
    clsBatchOp = Batchoption.BatchOption(DB_NAME, API_KEY, IS_TESTNET)
    # clsBatchOp.get_addr_balance(MASTER_ADDR)
    clsBatchOp.get_token_balance(MASTER_ADDR, JETTON_MASTER)
    
    # clsBatchOp.batch_transfer_ton(MASTER_KEY, 0.1, 4)
    
    # clsBatchOp.batch_transfer_jetton(MASTER_KEY, JETTON_MASTER, 10 * 10**9, 3)
    

def generatekey():
    clsGenKey = GenerateKey.GenerateKey(DB_NAME, API_KEY, IS_TESTNET)
    # clsGenKey.GenerateKey(5)
    
    clsGenKey.showDB(0)
    
def contractOp():
    clsCnt = interctContract.ContractTemplate(API_KEY, IS_TESTNET, CONTRACT_ADDR)
    clsCnt.onWithdrawNativeClicked(MASTER_KEY, 0.1)
    
if __name__ == "__main__":
    # generatekey()

    # batchOp()
    
    contractOp()
    