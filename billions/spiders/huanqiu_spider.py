import json

import scrapy
import time
from scrapy.selector import Selector

from billions.items import D1evItem
from billions.util.time import getwjj


class HuanQiuSpider(scrapy.Spider):
    name = "huanqiu"
    start_urls = []
    for page in range(1, 9900, 1):
        url = "https://auto.huanqiu.com/api/list?node=%22/e3pmh24qk/e3pmh25cs%22,%22/e3pmh24qk/e3pmtj57c%22,%22/e3pmh24qk/e3pmtkgc2%22,%22/e3pmh24qk/e3pn02mp3%22,%22/e3pmh24qk/e3pn4el6u%22,%22/e3pmh24qk/ej8aajlga%22," \
              "%22/e3pmh24qk/en0e9b249%22&offset=" + str(page) + "&limit=100"
        start_urls.append(url)

    def parse(self, response):

        if response.text is None:

            value = self.crawler.stats.get_value("no_content_url")
            if value is None:
                value = []
            value.append(response.url)
            self.crawler.stats.set_value('no_content_url', value)
            return
        response_text = response.text.replace("\\", "\\\\")  # 对json中的反斜杠转义
        jsonText = json.loads(response_text,strict=False)# type: json
        for content in jsonText['list']:
            if len(content) == 0:
                continue
            title = content.get('title')
            homeTuUrl = content.get('cover')
            newsUrl = content['aid']
            newsUrl = "https://auto.huanqiu.com/article/" + newsUrl

            d1evItem = D1evItem()
            d1evItem['image_path'] = self.name
            d1evItem['page'] = response.url
            if homeTuUrl is not None  and "." in homeTuUrl and "no-picture" not in homeTuUrl:  # 有些缩略图为空
                d1evItem['homeTuUrl'] = response.urljoin(homeTuUrl)
            d1evItem['itit'] = title
            d1evItem['newsUrl'] = response.urljoin(newsUrl)

            yield scrapy.Request(newsUrl, callback=self.parseNews, meta={"item": d1evItem})

    def parseNews(self, response):

        d1evItem = response.meta["item"]

        # 正文
        html_content = response.xpath("//textarea[@class='article-content']").get()  # type:str
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
