import json

import requests

headers = {

    "Content-type": "application/json",
    "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-encoding": "gzip, deflate, br",
    "Accept-language": "zh-CN,zh;q=0.9",
    "Bnc-Uuid": "zh-CN,zh;q=0.9",
    "content-length": "63",
    "Cookie": "cid=zQDeHXFr; bnc-uuid=8b6eb09e-7a16-4052-aae2-b1f7a8009a4d; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22187fe5f8a4593-0f988be78f10a48-26031a51-2073600-187fe5f8a46915%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTg3ZmU1ZjhhNDU5My0wZjk4OGJlNzhmMTBhNDgtMjYwMzFhNTEtMjA3MzYwMC0xODdmZTVmOGE0NjkxNSJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%22187fe5f8a4593-0f988be78f10a48-26031a51-2073600-187fe5f8a46915%22%7D; userPreferredCurrency=USD_USD; BNC_FV_KEY=3312c62b39d4a629a72d5c964e13b07c28cb4613; _gid=GA1.2.1038647143.1683599888; aliyungf_tc=142c957897703bebd9b6f9a048578585646f7101f336dece21c351dd293dc564; BNC_FV_KEY_EXPIRE=1683802770238; _ga=GA1.2.369787330.1683599887; lang=zh-cn; _gat=1; _ga_3WP50LGEEC=GS1.1.1683793515.7.1.1683796660.46.0.0",
    "sec-ch-ua": "Google Chrome",
    "Csrftoken": "d41d8cd98f00b204e9800998ecf8427e",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "macOS",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-si",
    "Lang":"zh-CN"
}
#339
payload = {"pageIndex":1,"pageSize":20,"type":2,"userId":0}
jsonRaw = json.dumps(payload)
# r =requests.get("https://space.id/tld/bnb?query=85828524")
r = requests.post("https://www.suitechsui.org/bapi/composite/v1/friendly/pgc/news/list?", headers=headers, data=jsonRaw)
# print(r.text)
list = r.json()["data"]["vos"]
for li in list:
    title = li["title"]
    imiao = li["subTitle"]
    id = li["id"]
    url = li["webLink"]

    print(f"title{title} , imiao {imiao} , id {id} , url {url}")


