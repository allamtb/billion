import json

from web3 import Web3,HTTPProvider
# from web3.middleware import geth_poa_middleware

# w3 = Web3(HTTPProvider('https://bsc-dataseed.binance.org'))
# w3.middleware_onion.inject(geth_poa_middleware, layer=0)
w3 = Web3(HTTPProvider('https://bsc-dataseed.binance.org'))
privateKey = 'cd9094a9f2a3f02a569685dbbb788b82b49d2453c88f4d666ebcaedc33f91c56'
publicKey = '0xa049e642f2e62F243C57345f11521Ff60855B12f'
constract = '0x2dfF88A56767223A5529eA5960Da7A3F5f766406'

with open('abi.json', 'r') as abi_definition:
    abi = json.load(abi_definition)


contract = w3.eth.contract(address=constract, abi=abi)
# balance = contract.functions.balanceOf(publicKey).call()
# print(balance)

toKey = '0xF24b667b1C77889F351422A2A1eB9D82ffCFf0F2'

value = w3.to_wei('100', 'milli')
txn = contract.functions.transfer(toKey,value).build_transaction({
    # 私钥对应的公钥
    'nonce':w3.eth.get_transaction_count(publicKey),
    # 'maxFeePerGas'=3000000000,
    # maxPriorityFeePerGas=2000000000,
    'gas':55144,
    'gasPrice':w3.to_wei('5', 'gwei'),
    # # 公钥
    # value=w3.to_wei('23', 'milli'),
    'chainId':56,
}
)



signed_txn = w3.eth.account.sign_transaction(txn,private_key=privateKey)
result =w3.eth.send_raw_transaction(signed_txn.rawTransaction)
print(result)


balance = contract.functions.balanceOf(publicKey).call()
print(balance)