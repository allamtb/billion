import eth_account
import requests
import web3
from web3 import Web3,HTTPProvider

get = requests.get("http://www.baidu.com")

print(get)
# request_kwargs={
#
#   'timeout':60,
#   'proxies':{
#     'https':'https://t.91tianlu.pw:10146'
#   }
#
# }
# w3 = Web3(HTTPProvider('https://bsc-dataseed.binance.org'))
# print("number %s", w3.eth.block_number)
#
# ## 3000 milli = 3 ether
# w3.eth.send_transaction({
#   'to': '0xF24b667b1C77889F351422A2A1eB9D82ffCFf0F2',
#   'from': '0xa049e642f2e62F243C57345f11521Ff60855B12f',
#   'value': w3.to_wei('3000', 'milli'),
#   'gas': 21000,
#   'gasPrice':w3.to_wei('50','gwei')
# })

