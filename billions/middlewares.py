# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import logging

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from fake_useragent import UserAgent


class BillionsSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

    def process_exception(self, request, exception, spider):
        if (
                isinstance(exception, self.EXCEPTIONS_TO_RETRY)
                and not request.meta.get('dont_retry', False)
        ):
            return self._retry(request, exception, spider)
#


class BillionsUserAgentMiddleware:
    """This middleware allows spiders to override the user_agent"""

    def __init__(self,crawler, user_agent='Scrapy'):
        self.user_agent = user_agent
        self.crawler =crawler

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler,crawler.settings['USER_AGENT'],)
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        return o

    def spider_opened(self, spider):
        self.user_agent = getattr(spider, 'user_agent', self.user_agent)

    def process_request(self, request, spider):
        ua = UserAgent()
        request.headers.setdefault(b'User-Agent', ua.random)

    def process_response(self, response, request, spider):

        if response.status != 200:
            value = self.crawler.stats.get_value("fail_url")
            if value is None:
                value = []
            value.append(response.url)
            self.crawler.stats.set_value('fail_url', value, spider=spider)



        return response

    def process_exception(self, request, exception, spider):

        value = self.crawler.stats.get_value("fail_url")
        if value is None:
            value = []
        value.append(request.url)
        self.crawler.stats.set_value('fail_url', value, spider=spider)

        logging.error(exception, exc_info=True)





