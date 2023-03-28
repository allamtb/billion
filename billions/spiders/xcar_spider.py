import random
import time
from pathlib import Path
import scrapy
from loguru import logger
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest

from billions.items import D1evItem
from billions.util.csvUtil import CsvUtil
from billions.util.DBTool import db
from billions.util.htmlUtil import getwjj


# project_path = Path.cwd().parent
# log_path = Path(project_path, "log")


# 爱卡网，防爬虫了， 需要 selenium + 代理。
class XcarSpider(scrapy.Spider):
    name = "xcar"  # 爱卡网
    # logger.add(f"./log/xcarInfo.log", level="INFO", rotation="100MB", encoding="utf-8", enqueue=True, retention="10 days")
    custom_settings = {
        'DOWNLOAD_TIMEOUT': 30,
        'DOWNLOAD_DELAY': 0.1,  # delay in downloading images
        'RANDOMIZE_DOWNLOAD_DELAY': True,  # delay in downloading images
        'AUTOTHROTTLE_MAX_DELAY': 10,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 10,
        'LOG_ENABLED': True,  # 是否启动日志记录，默认True
        'LOG_FILE': 'log/xcarError.log',  # 日志输出文件，如果为NONE，就打印到控制台
        'LOG_LEVEL': 'ERROR',  # 日志级别，默认debug
        # 'JOBDIR': "jobinf/xcar/001"
    }


    # allowe_do
    def start_requests(self):

        carlist = CsvUtil.getCarList()
        for car in carlist:
            if carlist.index(car) > carlist.index("轩度"):
                for page in range(1, 1001, 1):
                    url = "http://search.xcar.com.cn/infosearch.php#?page=" + str(page) + "&searchValue=" + car + ""
                    logger.info("yield url: %s"%url)
                    delay = 1
                    ranDelay = random.uniform(0.5 * delay, 1.5 * delay)
                    time.sleep(ranDelay)
                    yield SeleniumRequest(url=url, callback=self.parse, screenshot=False, dont_filter=True, wait_time=2)


    def parse(self, response):

        logger.info(response.url)

        newsList = Selector(text=response.text).xpath("//div[@class='zx_list']/dl").getall()
        # 解析获取每篇文章的路径 、缩略图，注意缩略图为空的情况
        for news in newsList:
            title = ''.join(Selector(text=news).xpath("//dt/a//text()").getall())
            newsUrl = Selector(text=news).xpath("//dt/a/@href").get()

            d1evItem = D1evItem()
            d1evItem['image_path'] = self.name
            d1evItem['page'] = response.url
            d1evItem['itit'] = title
            url = response.urljoin(newsUrl)
            d1evItem['newsUrl'] = url

            if db.findUrl('inews_xcar',url):  # 如果已经存在该URL，则返回
                logger.info("url existed: %s" % url)
                return
            if db.findTitle('inews_xcar',title):  # 如果已经存在该标题，则返回
                logger.info("title existed: %s" % title)
                return

            logger.info("  yield newsUrl: %s" % newsUrl)
            yield scrapy.Request(newsUrl, callback=self.parseNews, meta={"item": d1evItem})

    def parseNews(self, response):
        d1evItem = response.meta["item"]
        # 正文
        html_content = response.xpath("//div[@id='newsbody']").get()  # type:str
        if html_content is None:
            html_content = response.xpath("//div[@class='detail_list_p clearfix']").get()  # type:
        if html_content is None:
            value = self.crawler.stats.get_value("empty_url")
            if value is None:
                value = []
            value.append(response.url)
            self.crawler.stats.set_value('empty_url', value)
            logger.info(" html content is none   ")
            return
        contentEnd = '<!-- 以上信息来自 -->'  # 去除文章末尾不需要的内容
        if  contentEnd in html_content:
            html_content = html_content[:html_content.index(contentEnd)]

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
            logger.info(" html or  itit is none   ")
            return
        logger.info("    yield newsItem: %s" %dict(d1evItem))
        yield d1evItem
