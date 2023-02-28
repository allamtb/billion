import time
from urllib.parse import urljoin
import scrapy
from scrapy.selector import Selector

from billions.items import BillionsItem, YiCheItem


class yicheSpider(scrapy.Spider):
    name = "yiche"
    yicheRootUrl = 'https://car.yiche.com/'

    def start_requests(self):
        urls = [
            'https://car.yiche.com/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        # 按字母A-Z排序的的所有信息
        getall = response.xpath("//div[@class='brand-list-item']").getall()
        for brands in getall:
            vendorList = Selector(text=brands).xpath("//div[@class='item-brand']").getall()
            # 按每个字母得到厂商信息
            # 获取厂商列表
            for vendor in vendorList:
                time.sleep(2)
                vendorHttpUrl = Selector(text=vendor).xpath("//@href").get()
                vendorHttpUrl= urljoin(self.yicheRootUrl,vendorHttpUrl)
                vendorImg = Selector(text=vendor).xpath("//img/@src").get()
                vendorImg= urljoin(self.yicheRootUrl,vendorImg)
                vendorName = Selector(text=vendor).xpath("//div[@class='brand-name']/text()").get()

                meta = {"vendorName":vendorName, "vendorImg":vendorImg}
                yield scrapy.Request(vendorHttpUrl, callback=self.parseCarBrand,meta=meta)

    def parseCarBrand(self, response):
        # 解析具体的汽车详情页面
        CarBrandList = response.xpath("//div[@class='search-result-list-item']").getall()
        vendor_name = response.meta['vendorName']
        vendorImg = response.meta['vendorImg']
        for carBrand in CarBrandList:
            CarBrandName = Selector(text=carBrand).xpath("//p[@class='cx-name text-hover']/text()").get()
            price = Selector(text=carBrand).xpath("//p[@class='cx-price']/text()").get()
            CarBrandImgHttpUrl = Selector(text=carBrand).xpath("//img/@src").get()
            CarDetailUrl = Selector(text=carBrand).xpath("//@href").get()
            CarDetailUrl = urljoin(self.yicheRootUrl, CarDetailUrl)

            item = YiCheItem()
            item["CarBrandName"]= CarBrandName
            item["price"] = price
            item['CarBrandImgHttpUrl'] = [CarBrandImgHttpUrl,CarBrandImgHttpUrl]
            item['CarDetailUrl'] = CarDetailUrl
            item['vendorName'] = vendor_name
            item['vendorImg'] = vendorImg

            yield scrapy.Request(CarDetailUrl, callback=self.parseCarDetail, meta={"YiCheItem":item})


        # 对于分页信息，进行分页采集
        nextPage = response.xpath("//a[@data-current='next']/@href").get()
        if nextPage is not None:
            next_page = urljoin(self.yicheRootUrl,nextPage)
            yield scrapy.Request(next_page, callback=self.parseCarBrand)
        time.sleep(1)

    def parseCarDetail(self,response):

        CarBrandList = response.xpath("//a[@class='car-item-jump']/text()").getall()
        # print(response.meta['CarBrandName'] + ":" + response.meta['price'] + "/n")
        YiCheItem = response.meta['YiCheItem']
        YiCheItem['CarBradList'] = CarBrandList
        yield YiCheItem

