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
        # 正文
        html_content = response.xpath("//div[@id='showall233']").get()
        index =html_content.index("<div class=\"source--wrapper")
        html_content=html_content[:index]
        #  正文中的图片
        image_urls =[]
        image_urls.append(d1evItem['homeTuUrl'])
        images = Selector(text=html_content).xpath("//img/@src").getall()
        image_urls.extend(images)
        d1evItem['image_urls']=image_urls
        d1evItem['html_content'] = html_content

        #todo 如果没有 title 以及 html 就不要生成了。
        yield d1evItem


        # 图片入库 （mysql）
        # 容错处理 1、 翻页的容错  2、 没有hometu的处理  3、 其他可能出错的保护
