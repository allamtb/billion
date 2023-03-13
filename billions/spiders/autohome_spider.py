import json

import scrapy
import time
from scrapy.selector import Selector

from billions.items import D1evItem
from billions.util.time import getwjj


# 未采集
# 这个是在 .net 环境采集的，需要重新采集。
class HuanQiuSpider(scrapy.Spider):
    name = "autohome"
    start_urls = []
    for page in range(1, 10607, 1):
        url = "https://www.autohome.com.cn/all/" + str(page) + "/#liststart";
        start_urls.append(url)

    def parse(self, response):

        if response.text is None:
            return

        newsList = response.xpath("//ul[@class='article']//li").getall()

        print(response.url)
        # 解析获取每篇文章的路径 、缩略图，注意缩略图为空的情况
        for news in newsList:
            newsUrl = Selector(text=news).xpath("//a/@href").get()
            homeTuUrl = Selector(text=news).xpath("//img/@src").get()
            newsUrl = response.urljoin(newsUrl)

            d1evItem = D1evItem()
            d1evItem['image_path'] = self.name
            d1evItem['page'] = response.url
            if "no-picture" not in homeTuUrl:  # 有些缩略图为空
                d1evItem['homeTuUrl'] = response.urljoin(homeTuUrl)
            d1evItem['newsUrl'] = newsUrl
            yield scrapy.Request(newsUrl, callback=self.parseNews, meta={"item": d1evItem})

    def parseNews(self, response):

        d1evItem = response.meta["item"]

        #title
        title = response.xpath("//div[@id='articlewrap']/h1/text()").get()  # type:str
        d1evItem['itit'] = title

        # 正文
        html_content = response.xpath("//div[@id='articleContent']").get()  # type:str
        d1evItem['html_content'] = html_content


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

        # 如果没有 title 以及 html 就不要生成内容了。
        if len(html_content) < 0 or len(d1evItem['itit']) < 0:
            pass
        yield d1evItem
