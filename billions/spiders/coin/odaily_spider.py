import os
import re
import time
from pathlib import Path
import scrapy
from loguru import logger
from scrapy import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import  WebDriverWait
import selenium.webdriver.support.expected_conditions as  EC
from tqdm import tqdm

from billions.items import D1evItem
from billions.util.DBTool import db
from billions.util.htmlUtil import getwjj
from urllib.parse import urljoin
import pickle

# project_path = Path.cwd().parent
# log_path = Path(project_path, "log")

from selenium import webdriver
# odaily 5/6
class OdailySpider(scrapy.Spider):
    name = "odaily"  # odaily
    # logger.add(f"./log/"+name+"Info.log", level="INFO", rotation="100MB", encoding="utf-8", enqueue=True, retention="10 days")
    custom_settings = {
        'DOWNLOAD_TIMEOUT': 30,
        'DOWNLOAD_DELAY': 0.1,  # delay in downloading images
        'RANDOMIZE_DOWNLOAD_DELAY': True,  # delay in downloading images
        'AUTOTHROTTLE_MAX_DELAY': 10,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 10,
        'LOG_ENABLED': True,  # 是否启动日志记录，默认True
        'LOG_FILE': 'log/'+name+'Error.log',  # 日志输出文件，如果为NONE，就打印到控制台
        'LOG_LEVEL': 'ERROR',  # 日志级别，默认debug
        # 'JOBDIR': "jobinf/"+name+"/001"
    }
    baseUrl = "https://www.odaily.news/"
    urls = set()

    # 如果需要重新跑程序，那么需要把urls.txt 删除重建
    urlsFile =  Path().absolute()/'spiders'/'coin'/'urls.txt'

    # allowe_do
    def start_requests(self):
        if os.path.getsize(self.urlsFile) > 0:
            with open(self.urlsFile, 'rb') as f:
                self.urls = pickle.load(f)
        import undetected_chromedriver as uc
        driver = uc.Chrome()
        driver.get(self.baseUrl)
        errorTime = 0
        times = 10000000
        pbar = tqdm(total=times)
        for i in range(times):
            result = Selector(text=driver.page_source).xpath('//div[@class="iZVHKqX_"]').getall()
            result1 = Selector(text=driver.page_source).xpath('//div[@class="_1I8wgn0k"]').getall()
            result.extend(result1)
            for rs in result:
                selector = Selector(text=rs)
                url = ""
                title = ""
                homeTu = ""
                if "_3OxLPO8K" in rs:
                    url = selector.xpath("//a/@href").get()
                    title = selector.xpath("//div[@class='_2-YXSDjv']/text()").get()
                    imiao = selector.xpath("//div[@class='_35gCv5dI']/text()").get()
                    homeTu = "none"
                elif "_1I8wgn0k" in rs:
                    url = selector.xpath("//a/@href").get()
                    title = selector.xpath("//h3[@class='_1__EitIA']/text()").get()
                    imiao = selector.xpath("//p[@class='_3YfETPl3']/text()").get()
                    homeTu = selector.xpath("//img/@src").get()

                if url in self.urls:
                    continue
                else:
                    self.urls.add(url)
                    with open(self.urlsFile,'wb') as f:
                        pickle.dump(self.urls,f)
                d1evItem = D1evItem()
                d1evItem['image_path'] = self.name
                d1evItem['page'] = url
                d1evItem['itit'] = title
                newsUrl = urljoin(self.baseUrl,url)
                d1evItem['newsUrl'] = newsUrl
                if "none" not in homeTu:
                    d1evItem['homeTuUrl'] = urljoin(self.baseUrl,homeTu)
                logger.info("yield url: %s"%newsUrl)
                yield SeleniumRequest(url=newsUrl, callback=self.parseNews, screenshot=False, dont_filter=True, wait_time=2,meta={"item": d1evItem})

            try:
                WebDriverWait(driver, 10). \
                    until(EC.visibility_of_element_located((By.XPATH, '//p[@class="_2fq3alzs"]'))).click()
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                time.sleep(4)
            except:
                errorTime  = errorTime+1
                print(f"错误 errorTime 次")
                if(errorTime ==100):
                    break
            pbar.update(1)

    def parseNews(self, response):
        d1evItem = response.meta["item"]
        html_content = response.body.decode('utf-8')
        # 正文
        html_content = re.sub(r'原文链接', '原地址', html_content)
        html_content = re.sub(r'<p>.*?原文.*?</p>', '', html_content)
        html_content = re.sub(r'":"', '', html_content)
        res = re.search(r'content(.*?)",',html_content)
        if res and res.group(1):
            html_content = res.group(1) # type:str

        html_content = re.sub(r'</h', r'\r\n</h', html_content)

        if html_content is None:
            value = self.crawler.stats.get_value("empty_url")
            if value is None:
                value = []
            value.append(response.url)
            self.crawler.stats.set_value('empty_url', value)
            return
        d1evItem['html_content'] = html_content
        # 正文中的图片
        image_urls = []
        if d1evItem.get('homeTuUrl',None):  # 只有hometu存在的时候才处理
            image_urls.append(d1evItem['homeTuUrl'])
        rawImages = Selector(text=html_content).xpath("//img/@src").getall()
        images = []
        for img in rawImages:
            url = re.search(r'"(.*?)"', img)
            if res:
                images.append(url.group(1).rstrip('\\'))

        newImages = [response.urljoin(image) for image in images]
        image_urls.extend(newImages)
        d1evItem['image_urls'] = image_urls

        # 生成图片文件夹的路径
        d1evItem['wjj'] = getwjj()

        # 如果没有 title 以及 html 就不要生成内容了。
        if len(html_content) <=0 or len(d1evItem['itit']) <= 0:
            return
        logger.info("    yield newsItem: %s" %dict(d1evItem))
        yield d1evItem
