# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import logging
import time

import scrapy
from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from fake_useragent import UserAgent
from scrapy.http import HtmlResponse

from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class BillionsSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    def process_exception(self, request, exception, spider):
        spider.logger.error(exception, exc_info=True)


class BillionsUserAgentMiddleware:
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


