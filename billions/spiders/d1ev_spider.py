import scrapy
import time
from scrapy.selector import Selector

from billions.items import D1evItem
from billions.util.time import getwjj


class QuotesSpider(scrapy.Spider):
    name = "d1ev"
    start_urls = [
        'https://www.d1ev.com/news',
    ]

    # allowe_do

    def parse(self, response):

        newsList = response.xpath("//div[@class='ws-news']//div[@class='article--wraped am-cf']").getall()

        # 解析获取每篇文章的路径 、缩略图，注意缩略图为空的情况

        for news in newsList:

            newsUrl = Selector(text=news).xpath("//a/@href").get()
            homeTuUrl = Selector(text=news).xpath("//img/@src").get()
            newsUrl = response.urljoin(newsUrl)
            print("新闻路径"+newsUrl)
            print("图片"+homeTuUrl)
            # 请求文章的路径
            d1evItem = D1evItem()
            d1evItem['image_path'] = 'd1ev'
            d1evItem['wjj'] = getwjj()
            d1evItem['homeTuUrl']=homeTuUrl
            d1evItem['newsUrl']=newsUrl

            yield scrapy.Request(newsUrl, callback=self.parseNews, meta={"item":d1evItem})


        # 对于分页信息，进行分页采集

        # nextPage =  response.xpath("//a[@rel='next']/@href").get()
        # if nextPage is not None:
        #     next_page = response.urljoin(nextPage)
        #     yield scrapy.Request(next_page, callback=self.parse)
        # time.sleep(1)

    def parseNews(self, response):

        d1evItem = response.meta["item"]
        html_content = response.xpath("//div[@id='showall233']").get()
        image_urls =[]
        image_urls.append(d1evItem['homeTuUrl'])
        d1evItem['image_urls']=image_urls
        
        yield d1evItem
        # d1evItem[]


        # 正则表达式获取文章正文

        # 获取图片列表，下载列表中的图片

        # 替换到文章中

        # 对文章进行处理 nohtml







        pass