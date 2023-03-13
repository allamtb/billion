# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import logging
import time

import requests
import scrapy
from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from fake_useragent import UserAgent
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from scrapy.http import HtmlResponse

from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class BillionsSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    def process_exception(self, request, exception, spider):
        spider.logger.error(exception, exc_info=True)


class BillionsUserAgentMiddleware(HttpProxyMiddleware):
    """This middleware allows spiders to override the user_agent"""

    def __init__(self, crawler, user_agent='Scrapy'):
        self.user_agent = user_agent
        self.crawler = crawler

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler, crawler.settings['USER_AGENT'], )
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        return o

    def spider_opened(self, spider):
        self.user_agent = getattr(spider, 'user_agent', self.user_agent)

    def process_request(self, request, spider):
        ua = UserAgent()
        request.headers.setdefault(b'User-Agent', ua.random)
        # ip = requests.get("http://get.9vps.com/getip.asp?username=15213283776&apikey=64304876&pwd=71ebf281cccfe9b06a433cc58e04739a&geshi=1&fenge=1&fengefu=&Contenttype=1&getnum=1&setcity=&operate=all")
        # if ip :
        #     request.meta["proxy"] = "http://"+ip.text.strip()


