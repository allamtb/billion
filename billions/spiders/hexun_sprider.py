import json

import scrapy
from loguru import logger
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest

from billions.items import D1evItem
from billions.util.DBTool import db
from billions.util.htmlUtil import getwjj


# 和讯网未采集

class HeXunSpider(scrapy.Spider):

    name = "hexun"
    start_urls = ["http://auto.hexun.com/qcyw/index.html"]
    # logger.add(f"./log/" + name + "Info.log", level="INFO", rotation="100MB", encoding="utf-8", enqueue=True,
    #            retention="10 days")

    custom_settings = {
        'DOWNLOAD_TIMEOUT':15,
        'DOWNLOAD_DELAY': 0.4,  # delay in downloading images
        'RANDOMIZE_DOWNLOAD_DELAY': True,  # delay in downloading images
        # 'AUTOTHROTTLE_MAX_DELAY': 10,
        # 'AUTOTHROTTLE_TARGET_CONCURRENCY': 10,
        # 'LOG_ENABLED': True,  # 是否启动日志记录，默认True
        # 'LOG_FILE': 'log/' + name + 'Error.log',  # 日志输出文件，如果为NONE，就打印到控制台
        # 'LOG_LEVEL': 'ERROR',  # 日志级别，默认debug
        # # 'JOBDIR': "jobinf/" + name + "/001"
    }

    for page in reversed(range(1, 3923, 1)):
        url = "http://auto.hexun.com/qcyw/index-"+str(page)+".html"
        start_urls.append(url)

        # allowe_do

    def start_requests(self):
        for page in reversed(range(1, 3800, 1)):
            url = "http://auto.hexun.com/qcyw/index-" + str(page) + ".html"
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        logger.info(response.url)
        if response.text is None:
            return
        newsList = response.xpath("//div[@class='mainbox']//li").getall()

        # 解析获取每篇文章的路径 、缩略图，注意缩略图为空的情况
        for news in newsList:
            newsUrl = Selector(text=news).xpath("//a/@href").get()
            newsUrl = response.urljoin(newsUrl)
            title = Selector(text=news).xpath("//a/text()").get()

            d1evItem = D1evItem()
            d1evItem['image_path'] = self.name
            d1evItem['page'] = response.url
            d1evItem['newsUrl'] = newsUrl
            d1evItem['itit'] = title

            if db.findUrl('inews_'+self.name,newsUrl):  # 如果已经存在该URL，则返回
                logger.info("newsUrl existed: %s" % newsUrl)
                return
            logger.info("  yield newsUrl: %s" % newsUrl)
            yield scrapy.Request(url=newsUrl, callback=self.parseNews, meta={"item": d1evItem})

    def parseNews(self, response):

        d1evItem = response.meta["item"]


        # 正文
        html_content = response.xpath("//div[@class='art_contextBox']").get()  # type:str
        d1evItem['html_content'] = html_content

        # 如果没有 title 以及 html 就不要生成内容了。
        if len(html_content) < 0 or len(d1evItem['itit']) < 0 or '内容正在升级改造' in html_content :
            return

        # 正文中的图片
        image_urls = []
        if d1evItem.get('homeTuUrl',None):  # 只有hometu存在的时候才处理
            image_urls.append(d1evItem['homeTuUrl'])
        images = Selector(text=html_content).xpath("//img/@src").getall()
        # 列表推导
        newImages = [response.urljoin(image) for image in images if image and "." in image]
        image_urls.extend(newImages)
        d1evItem['image_urls'] = image_urls

        # 生成图片文件夹的路径
        d1evItem['wjj'] = getwjj()
        logger.info("    yield newsItem: %s" % dict(d1evItem))
        yield d1evItem
