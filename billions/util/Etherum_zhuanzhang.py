from time import sleep

import eth_account
import requests
import web3
from hexbytes import HexBytes
from web3 import Web3,HTTPProvider
from web3.middleware import geth_poa_middleware



w3 = Web3(HTTPProvider('https://bsc-dataseed.binance.org'))

w3.middleware_onion.inject(geth_poa_middleware, layer=0)
privatekeys = [
'd532f5bc859f5e0a1bb64932db446452b3a47f829386a7d72dd9efe49226f6d0',
'8e083509b023e18871b12accd74028ff45523cb5a49082f2454e4f058c8e852a',
'2274a329783095395883d3862265c0ea6281dffd0951f4496d8a095620f37020',
'3b75492cfbfa8a0a975d4499decfe6efd58d7043602c7783739355c5dd520fb1',
'3d6fc0a5f795176309813f085aec7bb7aab4f96b7d4d023facdd4552e18322cb',
'c7089b5db67adc3946dd5fcf2c821ea1a32b41e792b1a93d23901dc626a9d198',
'8012c0dcc98c0acaf541cc11c054a94d4992567c0b0f73b5138098264fee4979',
'6f2505d75b2901ec8e841827d0742c1b189ae986ae6b5ee7ec307e63bd8656b4',
'bb0f10e8701d38dfaac41bf81c007c2d1e7c1dee31aebf82c6a0e38d166b7abc',
'decab9d2683dcd5117b7b0aa7f1b81344cc7ab3c6f4308370171feba6f1b9222'
]

publickeys = [

'0x8C76731C900a4014d7EBc136F97411486d963641',
'0x24fe8386eB9D3Af67E9353A5047699861B90F90d',
'0xF6C461E1aC33f5AfDBa5c95cc603c6b58854E1A8',
'0x4423cbbdB558c6cdD6e3AE72EA24Aad893589C7C',
'0xc5e0F20aBfc99E2C7A7D69742B6F558F9f77Ec2D',
'0xA8e23A87f5f0E1fc42332918Ca70398b3c5C09b0',
'0x5FaAE6e05d36B70e47f9F0c287B438D0ffD44d4a',
'0xF6d7C57eFE9a5eDf9E3C62A26cbFFb91b4CB0A53',
'0xE27de3427550E9823E093FD03be50fD8fdf98ffC',
'0xCE79ABc6E4A1770c7efB4b62D7bEF6eaC26E7021'
]

#
# for publickey in publickeys:
#     balancePub = w3.eth.get_balance(publickey)
#     print(publickey+":"+str(w3.from_wei(balancePub,'ether')))




def fabi(privateKey, publicKey, toKey):

    # 每个账号转 0.22
    signed_txn = w3.eth.account.sign_transaction(dict(
        # 私钥对应的公钥
        nonce=w3.eth.get_transaction_count(publicKey),
        # maxFeePerGas=3000000000,
        # maxPriorityFeePerGas=2000000000,
        gas=21000,
        gasPrice =w3.to_wei('5','gwei'),
        #公钥
        to=toKey,
        value= w3.to_wei('23', 'milli'),
        chainId=56,
      ),
        #私钥
        privateKey
    )
    print(privateKey + ":" + toKey + "0.023")
    w3.eth.send_raw_transaction(signed_txn.rawTransaction)


def autoFabi():
    with open('公钥.txt') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            toKey = line.strip()
            balance = w3.eth.get_balance(toKey)
            balance = w3.from_wei(balance,'ether')
            print(toKey + ":" + str(balance))
            if balance >0:
                print(toKey  + "已经有币，无需再发")
                continue
            # 每个privatekey 处理10个发币
            index = int(i / 10)
            privatekey = privatekeys[index]
            publickey = publickeys[index]
            balancePub = w3.eth.get_balance(publickey)
            ether = w3.from_wei(balancePub, 'ether')
            print(publickey+":"+str(ether))
            if ether < 0.023:
                print(toKey+"error: 钱不够发了"+publickey)
                continue

            fabi(privatekey, publickey, toKey)
            sleep(12)

            newBalance = w3.eth.get_balance(toKey)
            if newBalance >= 0.023:
                print(toKey+"success"+str(newBalance))
            else:
                print(toKey + "error" + str(newBalance))

# autoFabi()
with open('公钥.txt') as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
                toKey = line.strip()
                balance = w3.eth.get_balance(toKey)
                ether =  w3.from_wei(balance, 'ether')
                if balance==0 or ether >0.01 :
                    print(str(i) +"   "+ toKey + ":" + str(w3.from_wei(balance,'ether')))