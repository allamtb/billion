import json
import threading

import requests
import time
from tqdm import tqdm

headers = {

    "content-type": "application/json",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "accept": "*/*",
    "origin": "https://space.id",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "content-length": "754",
    "sec-ch-ua": "Google Chrome",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "macOS",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-si"

}

proxies = {
   'http': 'http://127.0.0.1:8888',
   'https': 'http://127.0.0.1:8888'
}

#
# payload = {"operationName": "domains", "variables": {
#             "input": {"query": bnb, "orderBy": "LIST_PRICE_ASC", "buyNow": 1, "network": 1,
#                       "domainStatuses": ["REGISTERED", "UNREGISTERED"], "first": 30}},
#                    "query": "query domains($input: ListDomainsInput!) {\n  domains(input: $input) {\n    exactMatch {\n      name\n      listPrice\n      lastSalePrice\n      tokenId\n      owner\n      network\n      orderSource\n      expirationDate\n      image\n      __typename\n    }\n    list {\n      name\n      listPrice\n      lastSalePrice\n      tokenId\n      owner\n      network\n      orderSource\n      expirationDate\n      image\n      __typename\n    }\n    pageInfo {\n      startCursor\n      endCursor\n      hasNextPage\n      __typename\n    }\n    __typename\n  }\n}"}
#


maxId = 0
count = 0
currentId = 1000000
isNeedBreak = False
while True:
    # jsonRaw = json.dumps(payload)
    r = requests.get(f"https://www.odaily.news/api/pp/api/app-front/feed-stream?feed_id=280&b_id={currentId}&per_page=20")
    # r = requests.post("https://www.odaily.news/api/pp/api/app-front/feed-stream?feed_id=280&b_id=280254&per_page=20", headers=headers)
    list = r.json()["data"]["items"]

    for l in list:
        print(l)
        cover = l["web_cover"]
        id = l["id"]
        if count == 0:
            maxId = id
        if count > 0 and currentId == maxId:
            isNeedBreak = True
        title = l["title"]
        url = "https://www.odaily.news/post/" +str(l["entity_id"])
        imiao = l["summary"]
        print(f"{cover} {title}  {url} {imiao}")
        count = count + 1
        currentId = id
    if isNeedBreak:
        break


print(maxId)
print(currentId)