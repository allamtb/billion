"""
Extension for collecting core stats like items scraped and start/finish times
"""
import logging
import os
import shutil
import traceback
from datetime import datetime
from pathlib import Path
from PIL import Image
from scrapy import signals


class ErrorCheck:


    def __init__(self, stats,crawler):
        self.stats = stats
        self.start_time = None
        self.store_uri = crawler.settings.get('IMAGES_STORE')

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.stats,crawler)
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(o.item_scraped, signal=signals.item_scraped)
        crawler.signals.connect(o.item_dropped, signal=signals.item_dropped)
        crawler.signals.connect(o.spider_error, signal=signals.spider_error)
        return o

    def spider_opened(self, spider):
        pass

    def spider_closed(self, spider, reason):

        spider.logger.info(self.stats.get_stats())


    def spider_error(self, failure, response, spider):
        reason = failure.__class__.__name__
        self.stats.inc_value(f'spider_error_count/{reason}', spider=spider)
        spider.logger.error(failure,exc_info=True)

    def item_scraped(self, item, spider):

        spider.logger.info(self.stats.get_stats())
        print(self.stats.get_stats())
        # 缩略图补救; 如果图片url地址有， 但是没有下载成功， 那么就用下载成功的第一张图片做缩略图

        if item.get("homeTuUrl",None):
            homeTuDownLoaded = False
            for image in item.get('images'):
                if 'home.jpg' in image['path'] and image['status'] == 'downloaded':
                    homeTuDownLoaded = True
            if not homeTuDownLoaded:
                for image in item.get('images'):
                    if image['status'] == 'downloaded':
                        # 转为缩略图 ; 获取图片的路径， 生成一个缩略图
                        path = Path().absolute() / self.store_uri / image['path']
                        img = Image.open(path)
                        image = img.copy()
                        image.thumbnail((270, 270))
                        path = str(path)
                        if os.sep in path:
                            homeTuPath = path[:path.rindex(os.sep)] + "/home.jpg"
                            image.save(homeTuPath, 'JPEG')
                            break


    def item_dropped(self, item, spider, exception):
        spider.logger.info(self.stats.get_stats())
        reason = exception.__class__.__name__
        self.stats.inc_value(f'item_dropped_reasons_count/{reason}', spider=spider)
        image_path = item.get('image_path', "default")
        path = Path().absolute() / self.store_uri / image_path / item.get("wjj")
        if os.path.exists(path):
            shutil.rmtree(path)
