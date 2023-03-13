import scrapy
from scrapy.selector import Selector

from billions.items import D1evItem
from billions.util.dbtool import db
from billions.util.time import getwjj

# 已采集 10w条
class QuotesSpider(scrapy.Spider):
    name = "d1ev"
    #start_urls = ["https://www.d1ev.com/news"]
    start_urls = []
    for page in range(5470,5471,1):
        pageInfo = 'https://www.d1ev.com/news/list-' + str(page)
        start_urls.append(pageInfo)



    # allowe_do

    def parse(self, response):

        newsList = response.xpath("//div[@class='ws-news']//div[@class='article--wraped am-cf']").getall()
        print(response.url)
        # 解析获取每篇文章的路径 、缩略图，注意缩略图为空的情况
        for news in newsList:
            newsUrl = Selector(text=news).xpath("//a/@href").get()
            homeTuUrl = Selector(text=news).xpath("//img/@src").get()
            newsUrl = response.urljoin(newsUrl)

            d1evItem = D1evItem()
            d1evItem['image_path'] = self.name
            d1evItem['page'] =  response.url
            if "no-picture" not in homeTuUrl:  # 有些缩略图为空
                d1evItem['homeTuUrl'] = response.urljoin(homeTuUrl)
            d1evItem['newsUrl'] = newsUrl

            if  db.findUrl(newsUrl) : # 如果已经存在该URL，则返回
                return
            yield scrapy.Request(newsUrl, callback=self.parseNews, meta={"item": d1evItem})

        # 对于分页信息，进行分页采集

        # nextPage = response.xpath("//a[@rel='next']/@href").get()
        # if nextPage is not None:
        #     next_page = response.urljoin(nextPage)
        #     yield scrapy.Request(next_page, callback=self.parse)

    def parseNews(self, response):

        d1evItem = response.meta["item"]

        # 标题
        itit = response.xpath("//div[@class='ws-title']/h1/text()").get()
        d1evItem['itit'] = itit

        if db.findTitle(itit):
            return

        # 正文
        html_content = response.xpath("//div[@id='showall233']").get()  # type:str
        index = html_content.index("<div class=\"source--wrapper")
        html_content = html_content[:index]
        d1evItem['html_content'] = html_content

        # 正文中的图片
        image_urls = []
        if len(d1evItem['homeTuUrl']) > 0:  # 只有hometu存在的时候才处理
            image_urls.append(d1evItem['homeTuUrl'])
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
