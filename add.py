from web3 import Web3
from web3.contract import ConciseContract
import json
import random
import string
import time
#import main

num_iterations = 100


w3 = Web3(Web3.HTTPProvider('https://d539-2001-44c8-4610-326f-80b7-e289-4217-de24.ap.ngrok.io'))
w3.eth.default_account = w3.eth.accounts[0]
abi_address = '0xCE0f0F6817b0f1b3781bE15e3bf94eD6c24463DE' #abi_address
abi = json.loads("""[
        {
                "inputs": [
                        {
                                "internalType": "address",
                                "name": "id",
                                "type": "address"
                        },
                        {
                                "internalType": "uint256",
                                "name": "HN",
                                "type": "uint256"
                        },
                        {
                                "internalType": "string",
                                "name": "name",
                                "type": "string"
                        }
                ],
                "name": "addPatient",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
        },
        {
                "inputs": [
                        {
                                "internalType": "address",
                                "name": "id",
                                "type": "address"
                        },
                        {
                                "internalType": "uint256",
                                "name": "HN",
                                "type": "uint256"
                        },
                        {
                                "internalType": "uint256",
                                "name": "temp",
                                "type": "uint256"
                        },
                        {
                                "internalType": "uint256",
                                "name": "hr",
                                "type": "uint256"
                        },
                        {
                                "internalType": "uint256",
                                "name": "spo2",
                                "type": "uint256"
                        }
                ],
                "name": "addVitalSign",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
        },
        {
                "inputs": [
                        {
                                "internalType": "address",
                                "name": "id",
                                "type": "address"
                        }
                ],
                "name": "getPatient",

                "outputs": [
                        {
                                "internalType": "uint256",
                                "name": "",
                                "type": "uint256"
                        },
                        {
                                "internalType": "string",
                                "name": "",
                                "type": "string"
                        }
                ],
                "stateMutability": "view",
                "type": "function"
        },
        {
                "inputs": [
                        {
                                "internalType": "address",
                                "name": "id",
                                "type": "address"
                        }
                ],
                "name": "getVitalsign",
                "outputs": [
                        {
                                "components": [
                                        {
                                                "internalType": "address",
                                                "name": "ID",
                                                "type": "address"
                                        },
                                        {
                                                "internalType": "uint256",
                                                "name": "HN",
                                                "type": "uint256"
                                        },
                                        {
                                                "internalType": "uint256",
                                                "name": "temp",

                                                "type": "uint256"
                                        },
                                        {
                                                "internalType": "uint256",
                                                "name": "hr",
                                                "type": "uint256"
                                        },
                                        {
                                                "internalType": "uint256",
                                                "name": "spo2",
                                                "type": "uint256"
                                        },
                                        {
                                                "internalType": "uint256",
                                                "name": "time",
                                                "type": "uint256"
                                        }
                                ],
                                "internalType": "struct CovidPatients.VitalSign[]",
                                "name": "",
                                "type": "tuple[]"
                        }
                ],
                "stateMutability": "view",
                "type": "function"
        },
        {
                "inputs": [],
                "name": "owner",
                "outputs": [
                        {
                                "internalType": "address",
                                "name": "",
                                "type": "address"
                        }
                ],
                "stateMutability": "view",
                "type": "function"
        }
]
""") # replace with the ABI of the deployed contract

contract = w3.eth.contract(address=abi_address, abi=abi)
concise_contract = contract.functions

wallet_id = '0x476579e75d2dDd84f2A7b55261558d78aeeb54A2'
# loop 10 times to add random vital sign data
temp=[]
hr = []
spo2=[]
HN =[]
N=1

def uploap(temp,spo2,bpm,HN):

    tx_hash = concise_contract.addVitalSign(wallet_id, HN, temp, bpm, spo2).transact({'from': w3.eth.accounts[0]})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

    end_time = time.time()
    #total_time = end_time - start_time
    l = len(wallet_id)+ len(str(HN)) + len(str(temp)) +len(str(bpm))+len(str(spo2))
    print(f'{l}, {tx_receipt.gasUsed}')



#gas_used = 129994
#gas_price = 1000000000000 # 100 Gwei

#transaction_cost = gas_used * gas_price
#transaction_cost_eth = w3.fromWei(transaction_cost, 'ether')

#print(f'Transaction cost: {transaction_cost_eth} ether')


