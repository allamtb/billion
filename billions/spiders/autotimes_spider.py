from pathlib import Path
import scrapy
from loguru import logger
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest

from billions.items import D1evItem
from billions.util.csvUtil import CsvUtil
from billions.util.dbtool import db
from billions.util.time import getwjj
# project_path = Path.cwd().parent
# log_path = Path(project_path, "log")


# 汽车时代网，3月10日,已采集完毕；


class autoTimesSpider(scrapy.Spider):
    name = "autotimes"  # 汽车时代网
    # logger.add(f"./log/"+name+"Info.log", level="INFO", rotation="100MB", encoding="utf-8", enqueue=True, retention="10 days")
    custom_settings = {
        'DOWNLOAD_TIMEOUT': 30,
        'DOWNLOAD_DELAY': 0.1,  # delay in downloading images
        'RANDOMIZE_DOWNLOAD_DELAY': True,  # delay in downloading images
        'AUTOTHROTTLE_MAX_DELAY': 10,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 10,
        'LOG_ENABLED': True,  # 是否启动日志记录，默认True
        'LOG_FILE': 'log/'+name+'Error.log',  # 日志输出文件，如果为NONE，就打印到控制台
        'LOG_LEVEL': 'ERROR',  # 日志级别，默认debug
        # 'JOBDIR': "jobinf/"+name+"/001"
    }

    # allowe_do
    def start_requests(self):

                for page in range(848, 3259, 1):
                    url = "https://www.autotimes.com.cn/news/"+str(page)+".html"
                    logger.info("yield url: %s"%url)
                    yield SeleniumRequest(url=url, callback=self.parse, screenshot=False, dont_filter=True, wait_time=2)


    def parse(self, response):

        logger.info(response.url)

        newsList = Selector(text=response.text).xpath("//div[@class='auto_wz_5']").getall()
        # 解析获取每篇文章的路径 、缩略图，注意缩略图为空的情况
        for news in newsList:
            title =   Selector(text=news).xpath("//a[@class='wz_link1']/text()").get()
            newsUrl = Selector(text=news).xpath("//a[@class='wz_link1']/@href").get()
            homeTuUrl = Selector(text=news).xpath("//img/@src").get()

            d1evItem = D1evItem()
            d1evItem['image_path'] = self.name
            d1evItem['page'] = response.url
            d1evItem['itit'] = title
            newsUrl = response.urljoin(newsUrl)
            d1evItem['newsUrl'] = newsUrl

            if homeTuUrl is not None and "." in homeTuUrl and "no-picture" not in homeTuUrl:  # 有些缩略图为空
                d1evItem['homeTuUrl'] = response.urljoin(homeTuUrl)

            if db.findUrl('inews_'+self.name,newsUrl):  # 如果已经存在该URL，则返回
                logger.info("newsUrl existed: %s" % newsUrl)
                return
            if db.findTitle('inews_'+self.name,title):  # 如果已经存在该标题，则返回
                logger.info("title existed: %s" % title)
                return

            logger.info("  yield newsUrl: %s" % newsUrl)
            yield scrapy.Request(newsUrl, callback=self.parseNews, meta={"item": d1evItem})

    def parseNews(self, response):
        d1evItem = response.meta["item"]
        # 正文
        html_content = response.xpath("//div[@id='cont']").get()  # type:str
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

        images = Selector(text=html_content).xpath("//img/@src").getall()
        # 列表推导
        newImages = [response.urljoin(image) for image in images]
        image_urls.extend(newImages)
        d1evItem['image_urls'] = image_urls

        # 生成图片文件夹的路径
        d1evItem['wjj'] = getwjj()

        # 如果没有 title 以及 html 就不要生成内容了。
        if len(html_content) < 0 or len(d1evItem['itit']) < 0:
            return
        logger.info("    yield newsItem: %s" %dict(d1evItem))
        yield d1evItem
