import os
import random
import re
import time
import traceback
from pathlib import Path

import requests
import scrapy
from loguru import logger
from scrapy import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import  WebDriverWait
import selenium.webdriver.support.expected_conditions as  EC
from tqdm import tqdm

from billions.items import D1evItem
from billions.util.DBTool import db
from billions.util.htmlUtil import getwjj
from urllib.parse import urljoin
import pickle

# project_path = Path.cwd().parent
# log_path = Path(project_path, "log")

from selenium import webdriver
# odaily 5/6
class OdailySpider(scrapy.Spider):
    name = "odaily"  # odaily
    # logger.add(f"./log/"+name+"Info.log", level="INFO", rotation="100MB", encoding="utf-8", enqueue=True, retention="10 days")
    custom_settings = {
        'DOWNLOAD_TIMEOUT': 30,
        'DOWNLOAD_DELAY': 0.1,  # delay in downloading images
        'RANDOMIZE_DOWNLOAD_DELAY': True,  # delay in downloading images
        'AUTOTHROTTLE_MAX_DELAY': 10,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 2 ,
        'LOG_ENABLED': True,  # 是否启动日志记录，默认True
        'LOG_FILE': 'log/'+name+'Error.log',  # 日志输出文件，如果为NONE，就打印到控制台
        'LOG_LEVEL': 'ERROR',  # 日志级别，默认debug
        # 'JOBDIR': "jobinf/"+name+"/001"
    }
    baseUrl = "https://www.odaily.news/"
    urls = set()

    # 如果需要重新跑程序，那么需要把urls.txt 删除重建
    urlsFile =  Path().absolute()/'spiders'/'coin'/'urls.txt'
    # allowe_do
    def start_requests(self):
        if os.path.getsize(self.urlsFile) > 0:
            with open(self.urlsFile, 'rb') as f:
                self.urls = pickle.load(f)
        maxId = 0
        count = 0
        currentId = 1000000
        isNeedBreak = False
        while True:

            try:
                # jsonRaw = json.dumps(payload)
                r = requests.get(
                    f"https://www.odaily.news/api/pp/api/app-front/feed-stream?feed_id=280&b_id={currentId}&per_page=20")
                # r = requests.post("https://www.odaily.news/api/pp/api/app-front/feed-stream?feed_id=280&b_id=280254&per_page=20", headers=headers)
                list = r.json()["data"]["items"]
                for l in list:
                    cover = l["web_cover"]
                    id = l["id"]
                    if count == 0:
                        maxId = id

                    currentId = id
                    print(f"id {id}、maxId{maxId}、 count {count}")
                    if count > 0 and id == maxId or id <= 100000:
                        print(f"error  id {id}、maxId{maxId}、 count {count}")
                        isNeedBreak = True
                    title = l["title"]
                    url = "https://www.odaily.news/post/" + str(l["entity_id"])

                    theUrl = "/post/" + str(l["entity_id"])
                    if theUrl in self.urls:
                        print(theUrl+"   existed")
                        continue
                    else:
                        self.urls.add(theUrl)
                        with open(self.urlsFile,'wb') as f:
                            pickle.dump(self.urls,f)


                    imiao = l["summary"]
                    print(f"{cover} {title}  {url} {imiao}")
                    count = count + 1

                    d1evItem = D1evItem()
                    d1evItem['image_path'] = self.name
                    d1evItem['page'] = url
                    d1evItem['itit'] = title
                    d1evItem['imiao'] = imiao
                    d1evItem['newsUrl'] = url
                    if "none" not in cover or len(cover)>0:
                        d1evItem['homeTuUrl'] = cover
                    logger.info("yield url: %s" % url)
                    yield SeleniumRequest(url=url, callback=self.parseNews, screenshot=False, dont_filter=True,
                                          wait_time=2,
                                          meta={"item": d1evItem})
            except:

                traceback.print_exc()

            if isNeedBreak:
                break
            print(f"currentId {currentId}")
            logger.info(f"currentId {currentId}")
            time.sleep(5)

    def parseNews(self, response):
        d1evItem = response.meta["item"]
        html_content = response.body.decode('utf-8')
        # 正文
        html_content = re.sub(r'原文链接', '原地址', html_content)
        html_content = re.sub(r'<p>.*?原文.*?</p>', '', html_content)
        html_content = re.sub(r'":"', '', html_content)
        res = re.search(r'content(.*?)",',html_content)
        if res and res.group(1):
            html_content = res.group(1) # type:str

        html_content = re.sub(r'</h', r'\r\n</h', html_content)

        if html_content is None:
            value = self.crawler.stats.get_value("empty_url")
            if value is None:
                value = []
            value.append(response.url)
            self.crawler.stats.set_value('empty_url', value)
            return
        d1evItem['html_content'] = html_content
        # 正文中的图片
        image_urls = []
        if d1evItem.get('homeTuUrl',None):  # 只有hometu存在的时候才处理
            image_urls.append(d1evItem['homeTuUrl'])
        rawImages = Selector(text=html_content).xpath("//img/@src").getall()
        images = []
        for img in rawImages:
            url = re.search(r'"(.*?)"', img)
            if res:
                images.append(url.group(1).rstrip('\\'))

        newImages = [response.urljoin(image) for image in images]
        image_urls.extend(newImages)
        d1evItem['image_urls'] = image_urls

        # 生成图片文件夹的路径
        d1evItem['wjj'] = getwjj()

        # 如果没有 title 以及 html 就不要生成内容了。
        if len(html_content) <=0 or len(d1evItem['itit']) <= 0:
            return
        # logger.info("    yield newsItem: %s" %dict(d1evItem))
        yield d1evItem
