import json
import re
import time
from pathlib import Path
import scrapy
from loguru import logger
from scrapy import signals
from scrapy.http import HtmlResponse
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest

from billions.items import D1evItem
# from billions.util.RegexUtil import fixCsv
from billions.util.RichSelenium import baidubaike
from billions.util.csvUtil import CsvUtil
from billions.util.DBTool import db
from billions.util.htmlUtil import getwjj


# project_path = Path.cwd().parent
# log_path = Path(project_path, "log")


# 百度，3月14日


class Baidu(scrapy.Spider):
    name = "baike"  # 百度百科
    logger.add(f"./log/" + name + "Info.log", level="INFO", rotation="100MB", encoding="utf-8", enqueue=True,
               retention="10 days")
    custom_settings = {
        'DOWNLOAD_TIMEOUT': 30,
        'DOWNLOAD_DELAY': 1,  # delay in downloading images
        'RANDOMIZE_DOWNLOAD_DELAY': True,  # delay in downloading images
        # 'AUTOTHROTTLE_MAX_DELAY': 10,
        # 'AUTOTHROTTLE_TARGET_CONCURRENCY': 10,
        'LOG_ENABLED': True,  # 是否启动日志记录，默认True
        'LOG_FILE': 'log/' + name + 'Error.log',  # 日志输出文件，如果为NONE，就打印到控制台
        'LOG_LEVEL': 'ERROR',  # 日志级别，默认debug
        # 'JOBDIR': "jobinf/"+name+"/001",
        'ITEM_PIPELINES': {
            'billions.pipelines.BillionsImagePipeline': 1,
            'billions.pipelines.BillionsReplaceImage1PathPipeline': 2,
            'billions.pipelines.BillionsNoHtmlTagPipeline': 3,
            'billions.pipelines.BillionJinghuaPipelineForBaidu': 4,
            'billions.pipelines.BillionsReplaceImage2PathPipeline': 5,
            # 'billions.pipelines.BillionsCaiPipeline': 6,
            'billions.pipelines.BillionImiaoPipeline': 7,
            "billions.pipelines.BillionsDBPipelineForBaike": 8,
        }
    }

    # allowe_do
    def start_requests(self):
        car  = [('埃安','广汽埃安','','https://baike.baidu.com/item/%E5%B9%BF%E6%B1%BD%E5%9F%83%E5%AE%89?fromModule=lemma_search-history'),
                ('大运','山西大运','','https://baike.baidu.com/item/%E5%B1%B1%E8%A5%BF%E5%A4%A7%E8%BF%90%E6%B1%BD%E8%BD%A6?fromModule=lemma_search-box'),
                ('华凯','长春一汽华凯','','https://baike.baidu.com/item/%E9%95%BF%E6%98%A5%E4%B8%80%E6%B1%BD%E5%8D%8E%E5%87%AF%E6%B1%BD%E8%BD%A6%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8?fromModule=lemma_search-box'),
                ('RAM','道奇Ram','','https://baike.baidu.com/item/%E9%81%93%E5%A5%87Ram/4126733?fromModule=search-result_lemma-recommend'),
                ('钧天','南昌钧天','','https://baike.baidu.com/item/%E5%8D%97%E6%98%8C%E9%92%A7%E5%A4%A9%E6%B1%BD%E8%BD%A6%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/53623006?fromModule=search-result_lemma-recommendhuahua'),
                ('时风','时风集团','','https://baike.baidu.com/item/%E6%97%B6%E9%A3%8E%E9%9B%86%E5%9B%A2?fromModule=lemma_search-box'),
                ('盛唐','江苏盛唐','','https://baike.baidu.com/item/%E6%B1%9F%E8%8B%8F%E7%9B%9B%E5%94%90%E8%BD%A6%E4%B8%9A%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/22179771?fr=aladdin'),
                ('三一集团','三一汽车制造','','https://baike.baidu.com/item/%E4%B8%89%E4%B8%80%E6%B1%BD%E8%BD%A6%E5%88%B6%E9%80%A0%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/20059249?fromModule=search-result_lemma-recommend'),
                ('神州','神州租车','','https://baike.baidu.com/item/%E5%8C%97%E4%BA%AC%E7%A5%9E%E5%B7%9E%E6%B1%BD%E8%BD%A6%E7%A7%9F%E8%B5%81%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8?fromtitle=%E7%A5%9E%E5%B7%9E%E6%B1%BD%E8%BD%A6%E7%A7%9F%E8%B5%81%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8&fromid=722434&fromModule=lemma_search-box'),
                 ('坦克','坦克800','','https://baike.baidu.com/item/%E5%9D%A6%E5%85%8B800?fromModule=lemma_search-box'),
                ('前途','前途汽车','','https://baike.baidu.com/item/%E5%89%8D%E9%80%94%E6%B1%BD%E8%BD%A6/23624264?fr=aladdin'),
                ('仰望','比亚迪仰望','比亚迪','https://baike.baidu.com/item/%E4%BB%B0%E6%9C%9B/62192854?fromModule=search-result_lemma-recommend'),
                ('魔方','北京魔方','北京汽车','https://baike.baidu.com/item/%E5%8C%97%E4%BA%AC%E9%AD%94%E6%96%B9?fromModule=lemma_search-box'),
                # ('兴运','北汽黑豹G6','北汽黑豹',''),
                ('海鸥','比亚迪海鸥','比亚迪','https://baike.baidu.com/item/%E6%AF%94%E4%BA%9A%E8%BF%AA%E6%B5%B7%E9%B8%A5/62559046?fr=aladdin'),
                ('海豚','比亚迪海豚','比亚迪','https://baike.baidu.com/item/%E6%AF%94%E4%BA%9A%E8%BF%AA%E6%B5%B7%E8%B1%9A?fromModule=lemma_search-box'),
                ('帕萨特','帕萨特','大众','https://baike.baidu.com/item/%E5%B8%95%E8%90%A8%E7%89%B9/1023285?fromModule=lemma_search-box'),
                ('优越','开沃汽车','开沃汽车','https://baike.baidu.com/item/%E5%BC%80%E6%B2%83D07/56234841?fr=aladdin'),
                ('型格','型格INTEGRA','本田','https://baike.baidu.com/item/%E5%9E%8B%E6%A0%BCINTEGRA?fromModule=lemma_search-box'),
                ('江苏车驰','江苏车驰','','https://baike.baidu.com/item/%E6%B1%9F%E8%8B%8F%E8%BD%A6%E9%A9%B0%E6%B1%BD%E8%BD%A6%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/20031417?fromModule=search-result_lemma-recommend'),
                ('傲旋','江苏车驰','江苏车驰','https://baike.baidu.com/item/%E5%82%B2%E6%97%8B/61184431?fromModule=search-result_lemma-recommend'),
                ('AM晓奥汽车','晓奥汽车','','https://baike.baidu.com/item/%E4%B8%8A%E6%B5%B7%E6%99%93%E5%A5%A5%E6%B1%BD%E8%BD%A6%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8?fromModule=lemma_search-box'),
                ('别克','别克','','https://baike.baidu.com/item/%E5%88%AB%E5%85%8B/557597?fromModule=lemma-qiyi_sense-lemma'),
                ('百智新能源','百智大猫','','https://baike.baidu.com/item/%E7%99%BE%E6%99%BA%E5%A4%A7%E7%8C%AB?fromModule=lemma_search-box#reference-[2]-35933118-wrap'),
                ('铂驰','铂驰T系列','','https://baike.baidu.com/item/%E9%93%82%E9%A9%B0T%E7%B3%BB%E5%88%97/56144679?fr=aladdin'),
                ('北奔重卡','北奔V3重卡','','https://baike.baidu.com/item/%E5%8C%97%E5%A5%94V3%E9%87%8D%E5%8D%A1/15556616?fromModule=search-result_lemma-recommend'),
                ('宝骐汽车','浙江宝骐汽车有限公司','','https://baike.baidu.com/item/%E6%B5%99%E6%B1%9F%E5%AE%9D%E9%AA%90%E6%B1%BD%E8%BD%A6%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/20023431?fromModule=search-result_lemma-recommend'),
                ('北汽泰普','北汽泰普越野车科技有限公司','','https://baike.baidu.com/item/%E5%8C%97%E6%B1%BD%E6%B3%B0%E6%99%AE%E8%B6%8A%E9%87%8E%E8%BD%A6%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/21429468?fromModule=search-result_lemma-recommend'),
                ('北汽黑豹','北汽黑豹（威海）汽车有限公司','','https://baike.baidu.com/item/%E5%8C%97%E6%B1%BD%E9%BB%91%E8%B1%B9%EF%BC%88%E5%A8%81%E6%B5%B7%EF%BC%89%E6%B1%BD%E8%BD%A6%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/51237194?fromModule=search-result_lemma-recommend'),
                ('长安凯程','重庆长安凯程汽车科技有限公司','','https://baike.baidu.com/item/%E9%87%8D%E5%BA%86%E9%95%BF%E5%AE%89%E5%87%AF%E7%A8%8B%E6%B1%BD%E8%BD%A6%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/60835644?fromModule=search-result_lemma-recommend'),
                ('东风轻型车','东风轻型专用车','','https://baike.baidu.com/item/%E4%B8%9C%E9%A3%8E%E8%BD%BB%E5%9E%8B%E4%B8%93%E7%94%A8%E8%BD%A6/1202403?fromModule=search-result_lemma-recommend'),
                ('大力牛魔王','大力牛魔王','','https://baike.baidu.com/item/%E5%A4%A7%E5%8A%9B%E7%89%9B%E9%AD%94%E7%8E%8B/62455355?fromModule=lemma-qiyi_sense-lemma'),
                ('大发电动屋','泰安市大发电动汽车制造有限公司','','https://baike.baidu.com/item/%E6%B3%B0%E5%AE%89%E5%B8%82%E5%A4%A7%E5%8F%91%E7%94%B5%E5%8A%A8%E6%B1%BD%E8%BD%A6%E5%88%B6%E9%80%A0%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/52214426?fromModule=search-result_lemma-recommend'),
                ('福田法拉利','法拉利','','https://baike.baidu.com/item/%E6%B3%95%E6%8B%89%E5%88%A9/159977?fr=aladdin'),
                ('国机智骏','国机智骏','','https://baike.baidu.com/item/%E5%9B%BD%E6%9C%BA%E6%99%BA%E9%AA%8F%E6%B1%BD%E8%BD%A6%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/23474393?fromModule=search-result_lemma-recommend'),
                ('法诺新能源','法诺新能源','','https://baike.baidu.com/item/%E6%B7%B1%E5%9C%B3%E6%B3%95%E8%AF%BA%E6%96%B0%E8%83%BD%E6%BA%90%E6%B1%BD%E8%BD%A6%E6%8E%A7%E8%82%A1%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/51542207?fromModule=search-result_lemma-recommend'),
                ('国金汽车','国金汽车','','https://baike.baidu.com/item/%E5%B1%B1%E4%B8%9C%E5%9B%BD%E9%87%91%E6%B1%BD%E8%BD%A6%E5%88%B6%E9%80%A0%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/19984889?fromModule=search-result_lemma-recommend'),
                ('宝骐汽车','浙江宝骐汽车有限公司','','https://baike.baidu.com/item/%E6%B5%99%E6%B1%9F%E5%AE%9D%E9%AA%90%E6%B1%BD%E8%BD%A6%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/20023431?fromModule=search-result_lemma-recommend'),
                ('国吉商用车','浙江宝骐汽车有限公司','','https://baike.baidu.com/item/%E5%90%89%E6%9E%97%E7%9C%81%E5%9B%BD%E5%90%89%E6%8E%A7%E8%82%A1%E9%9B%86%E5%9B%A2%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/60339945?fr=aladdin'),
                ('东风EV新能源','东风EV新能源','','https://baike.baidu.com/item/%E4%B8%9C%E9%A3%8EEV%E6%96%B0%E8%83%BD%E6%BA%90EX1/61354560?fr=aladdin'),
                ]

       # car =fixCsv()

        for item in car:
            d1evItem = D1evItem()
            d1evItem['lei11'] = item[0]  #
            d1evItem['lei22'] = item[2]  #
            d1evItem['imiao'] = item[0]
            url = item[3]
            if db.findUrl('baike_baidu', url):  # 如果已经存在该URL，则返回
                      logger.info("newsUrl existed: %s" % url)
                      continue
            yield SeleniumRequest(url=url, callback=self.parse, meta={"item": d1evItem}, screenshot=False, dont_filter=True)

        # venders = CsvUtil.getVender()
        # for vender in venders:
        #       d1evItem = D1evItem()
        #       d1evItem['lei11'] = vender[0] #厂商自己就是父类
        #       d1evItem['lei22'] = ""
        #       d1evItem['imiao'] = vender[0]
        #       url = baidubaike(vender[0])
        #       # if db.findUrl('baike_baidu', url):  # 如果已经存在该URL，则返回
        #       #     logger.info("newsUrl existed: %s" % url)
        #       #     continue
        #       yield SeleniumRequest(url=url, callback=self.parse, meta={"item": d1evItem}, screenshot=False, dont_filter=True)
        #
        # cars = CsvUtil.getCar()
        # for car in cars:
        #     d1evItem = D1evItem()
        #     d1evItem['lei11'] = car[1] # 父类是厂商
        #     d1evItem['lei22'] = car[0] # 子类是自己
        #     d1evItem['imiao'] = car[0]
        #     url = baidubaike(car[0])
        #     # if db.findUrl('baike_baidu', url):  # 如果已经存在该URL，则返回
        #     #     logger.info("newsUrl existed: %s" % url)
        #     #     continue
        #     yield SeleniumRequest(url=url, callback=self.parse,meta={"item": d1evItem},screenshot=False, dont_filter=True)


    def parse(self, response):
        d1evItem = response.meta["item"]
        logger.info(response.url)
        title = response.xpath("//span[@class='ec-pc_text-desc']//text()").get()

        if title is None:
            title = response.xpath("//div[@class='lemma-desc']//text()").get()
        if title is None:
            logger.error(response.url + "need check")
        title = d1evItem.get("imiao", "") + "--" + title

        contents = response.xpath("//div[@data-pid] | //div[@class='para']").getall()

        html = ""
        for content in contents:
            if 'data-pid="card"' not in content:
                html = html + " " + content

        image_urls = []
        homeTuUrl = response.xpath("//div[@class='summary-pic']//img/@src").get()

        if  homeTuUrl is not None and "no-picture" not in homeTuUrl:  # 有些缩略图为空
            d1evItem['homeTuUrl'] = response.urljoin(homeTuUrl)
            image_urls.append(d1evItem['homeTuUrl'])

        images = Selector(text=html).xpath("//img/@src").getall()
        # 列表推导
        newImages = [response.urljoin(image) for image in images if 'data:image' not in image]

        images2 = Selector(text=html).xpath("//img/@data-src").getall()
        newImages2 = [response.urljoin(image) for image in images2]
        newImages.extend(newImages2)

        image_urls.extend(newImages)
        # 生成图片文件夹的路径
        # 如果没有 title 以及 html 就不要生成内容了。
        if html is None or len(html) < 0 or title is None or len(title) < 0:
            logger.error(response.url + "need check")
            return

        dds = response.xpath("//div[@data-pid='card']//dd").getall()
        for dd in dds:
            if "http" in dd:
                p = re.compile(r"http([\s\S]*?)</dd>")
                result = p.search(dd)
                if result:
                    d1evItem['iurl'] = "http" + result.group(1)
        d1evItem['image_path'] = self.name
        d1evItem['page'] = response.url
        d1evItem['itit'] = title
        d1evItem['html_content'] = html
        d1evItem['image_urls'] = image_urls
        d1evItem['wjj'] = getwjj()
        d1evItem['page'] = response.url
        d1evItem['newsUrl'] = response.url
        logger.info("    yield newsItem: %s" % dict(d1evItem))

        yield d1evItem
