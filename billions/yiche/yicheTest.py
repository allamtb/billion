import time

import requests;
from scrapy.selector import Selector

from billions.yiche.CarDict import CarDict
from urllib.parse import urljoin

CarbrandHtml = requests.get("https://car.yiche.com/")

carBrandSelector = Selector(text=CarbrandHtml.text)

getall = carBrandSelector.xpath("//div[@class='brand-list-item']").getall()

yicheRootUrl = 'https://car.yiche.com/'

for brands in getall:

    letter = Selector(text=brands).xpath("//div[@class='item-letter']/text()").get()
    vendorList = Selector(text=brands).xpath("//div[@class='item-brand']").getall()

    # 获取厂商列表
    for vendor in vendorList:
        time.sleep(2)
        vendorImgHttpUrl = Selector(text=vendor).xpath("//@href").get()

        vendorImgHttpUrl = urljoin(yicheRootUrl, vendorImgHttpUrl)

        vendorName = Selector(text=vendor).xpath("//div[@class='brand-name']/text()").get()

        car_dict = CarDict()
        car_dict.vendorImgHttpUrl = vendorImgHttpUrl
        car_dict.vendorName = vendorName
        CarbrandHtml = requests.get(vendorImgHttpUrl)
        carBrandSelector = Selector(text=CarbrandHtml.text)
        CarBrandList = carBrandSelector.xpath("//div[@class='search-result-list-item']").getall()
        # 具体页面，获取厂商对应的车款列表
        for carBrand in CarBrandList:
            CarBrandName = Selector(text=carBrand).xpath("//p[@class='cx-name text-hover']/text()").get()
            price = Selector(text=carBrand).xpath("//p[@class='cx-price']/text()").get()
            CarBrandHttpUrl = Selector(text=carBrand).xpath("//img/@src").get()
            CarDetailUrl = Selector(text=carBrand).xpath("//@href").get()
            CarDetailUrl = urljoin(yicheRootUrl, CarDetailUrl)

            print(CarBrandName + ":" + price + "/n")


        # 对于分页信息，进行分页采集
        nextPage = carBrandSelector.xpath("//a[@data-current='next']/@href").get()
        nextPage = urljoin(yicheRootUrl, nextPage)

        while yicheRootUrl != nextPage:
            CarbrandHtml = requests.get(nextPage)
            carBrandSelector = Selector(text=CarbrandHtml.text)
            CarBrandList = carBrandSelector.xpath("//div[@class='search-result-list-item']").getall()
            # 具体页面，获取厂商对应的车款列表
            for carBrand in CarBrandList:
                CarBrandName = Selector(text=carBrand).xpath("//p[@class='cx-name text-hover']/text()").get()
                price = Selector(text=carBrand).xpath("//p[@class='cx-price']/text()").get()
                CarBrandHttpUrl = Selector(text=carBrand).xpath("//img/@src").get()
                CarDetailUrl = Selector(text=carBrand).xpath("//@href").get()
                CarDetailUrl = urljoin(yicheRootUrl, CarDetailUrl)
                print(CarBrandName + ":" + price + "/n")

            # 对于分页信息，进行分页采集
            nextPage = carBrandSelector.xpath("//a[@data-current='next']/@href").get()

            nextPage = urljoin(yicheRootUrl, nextPage)
            print(nextPage)

