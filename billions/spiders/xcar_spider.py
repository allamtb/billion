import scrapy
import time

from scrapy import signals
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest

from billions.items import D1evItem
from billions.util.csvUtil import CsvUtil
from billions.util.time import getwjj

from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class XcarSpider(scrapy.Spider):
    name = "xcar"  # 爱卡网


    # allowe_do
    def start_requests(self):

        carlist = CsvUtil.getCarList()
        for car in carlist:
            for page in range(1, 1001, 1):
                url = "https://search.xcar.com.cn/infosearch.php#?page=" + str(page) + "&searchValue=" + car + ""
                yield SeleniumRequest(url=url, callback=self.parse, screenshot=True,dont_filter=True)


    def parse(self, response):
        print(response.url)
        newsList = Selector(text=response.text).xpath("//div[@class='zx_list']/dl").getall()
        # 解析获取每篇文章的路径 、缩略图，注意缩略图为空的情况
        for news in newsList:
            title = ''.join(Selector(text=news).xpath("//dt/a//text()").getall())
            newsUrl = Selector(text=news).xpath("//dt/a/@href").get()

            d1evItem = D1evItem()
            d1evItem['image_path'] = self.name
            d1evItem['page'] = response.url
            d1evItem['itit'] = title
            d1evItem['newsUrl'] = response.urljoin(newsUrl)

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
            return
        yield d1evItem
