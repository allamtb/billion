import json
import time
from pathlib import Path
import scrapy
from loguru import logger
from scrapy import signals
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest

from billions.items import D1evItem
from billions.util.csvUtil import CsvUtil
from billions.util.dbtool import db
from billions.util.time import getwjj
# project_path = Path.cwd().parent
# log_path = Path(project_path, "log")


# 懂车帝，3月10日


class DongChe(scrapy.Spider):

    dictx = {}
    name = "dongche"  # 懂车帝
    logger.add(f"./log/"+name+"Info.log", level="INFO", rotation="100MB", encoding="utf-8", enqueue=True, retention="10 days")
    custom_settings = {
        'DOWNLOAD_TIMEOUT': 30,
        'DOWNLOAD_DELAY': 1,  # delay in downloading images
        'RANDOMIZE_DOWNLOAD_DELAY': True,  # delay in downloading images
        'AUTOTHROTTLE_MAX_DELAY': 10,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 10,
        # 'LOG_ENABLED': False,  # 是否启动日志记录，默认True
        # 'LOG_FILE': 'log/'+name+'Error.log',  # 日志输出文件，如果为NONE，就打印到控制台
        # 'LOG_LEVEL': 'ERROR',  # 日志级别，默认debug
        # 'JOBDIR': "jobinf/"+name+"/001"
    }

    # allowe_do
    def start_requests(self):
        self.crawler.signals.connect(self.spider_closed, signal=signals.spider_closed)
        for page in range(1, 10000, 1):
            url = "https://www.dongchedi.com/community/"+str(page)
            logger.info("yield url: %s"%url)
            time.sleep(1)
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        logger.info(response.url)
        title = response.xpath("//div[@class='tw-w-5/10']/h1/text()").get()
        num = response.xpath("//p[@class='community-header_value__3MNnx tw-text-common-white tw-font-medium']/text()").get()
        self.dictx[title] = (num,response.url)
        print(f"汽车： {title} 人气 {num}")
        logger.info(self.dictx)


    def spider_closed(self, spider, reason):
        with open('dongche.txt','w') as f:
            f.write(json.dumps(self.dictx))
