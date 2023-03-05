# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import traceback
from io import BytesIO
from pathlib import Path

import scrapy
from PIL import Image
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline, ImageException
import re
import os
from twisted.enterprise import adbapi
import json
import shutil

# 下载图片、缩略图
from billions.util.csvUtil import CsvUtil
from billions.util.htmlUtil import imiao, noHtml
import logging


class PipeLineFather():

    def process_item(self, item, spider):
        try:
            self.process_the_item(item,spider)
        except Exception  as ex:
            #todo 记录日志，log 来记录
            str = traceback.print_exc()
            #  print(dict(item))
            raise DropItem(ex)
        else:
            return item

    def process_the_item(self, item, spider):
        pass


class BillionsImagePipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None, *, item=None):
        image_urls = item.get('image_urls', [])
        image_path = item.get('image_path', "default")
        wjj = item.get('wjj', 'error')
        image_guid = image_urls.index(request.url)
        homeTuUrl = item.get('homeTuUrl', "none")
        if image_guid == 0 and homeTuUrl != "none":
            return f'{image_path}/{wjj}/home.jpg'
        else:
            return f'{image_path}/{wjj}/{image_guid}.jpg'

    # 生成缩略图，对图片列表中的第一张图片生成缩略图。
    def get_images(self, response, request, info, *, item=None):
        path = self.file_path(request, response=response, info=info, item=item)
        orig_image = self._Image.open(BytesIO(response.body))

        width, height = orig_image.size
        if width < self.min_width or height < self.min_height:
            raise ImageException("Image too small "
                                 f"({width}x{height} < "
                                 f"{self.min_width}x{self.min_height})")
        image, buf = self.convert_image(orig_image)

        image_urls = item.get('image_urls', [])
        image_path = item.get('image_path', "default")
        homeTuUrl = item.get('homeTuUrl', "none")
        wjj = item.get('wjj', 'error')
        image_guid = image_urls.index(request.url)
        thumb_path = f'{image_path}/{wjj}/home.jpg'

        if image_guid == 0:  # 对第一张图片，需要生成缩略图
            thumb_image, thumb_buf = self.convert_image(image, (270, 270))
            yield thumb_path, thumb_image, thumb_buf

        # 这里文章的图片才需要yield。 若是第一张图片，又存在缩略图url，表示他是缩略图，就不要再下载为文章图片了。
        if not (image_guid == 0 and homeTuUrl != "none"):
            yield path, image, buf


# 替换文章中图片的路径
class BillionsReplaceImage1PathPipeline(PipeLineFather):

    def process_the_item(self, item, spider):

        html_content = item.get("html_content")
        # 替换文章中的图片地址为已经下载好的图片地址
        for image in item.get('images'):
            if image['status'] == 'downloaded':
                filePath = image['path']
                fileUrl = image['url']
                # 'd1ev/20230301185559556105/1.jpg'  获取 20230301185559556105/1.jpg
                filePath = filePath[filePath.index("/") + 1:]
                replaceAfter = "\n" + "eeimg/" + filePath + "\n"
                # 注意使用？ ，表示要三思，懒汉模式；否则会恶汉匹配
                replaceBefore = r"<img src=\"" + fileUrl + r".*?\">"
                html_content = re.sub(replaceBefore, replaceAfter, html_content)

        item["html_content"] = html_content
        return item


class BillionsNoHtmlTagPipeline(PipeLineFather):
    def process_the_item(self, item, spider):
        html_content = item.get("html_content")
        item["html_content"] = noHtml(html_content)
        return item


# 替换文章中图片的路径回来，同时添加上 tag 信息
class BillionsReplaceImage2PathPipeline(PipeLineFather):

    def process_the_item(self, item, spider):
        html_content = item.get("html_content")
        tag = CsvUtil.findTag(htmlCount=html_content)
        if len(tag) < 1:
            item["ikey"] = item.get("itit", " ")
        else:
            item["ikey"] = tag
        item["biaoq"] = tag
        imgtag = "< img alt =\"" + tag + "\" src=\"/eeimg/{HostI}/img"

        html_content = re.sub("eeimg", imgtag, html_content)
        html_content = re.sub(".jpg", ".jpg \"/>", html_content)
        item["html_content"] = html_content

        return item


class BillionImiaoPipeline(PipeLineFather):
    def process_the_item(self, item, spider):
        html_content = item.get("html_content")
        html_content = noHtml(html_content)
        item["imiao"] = imiao(html_content, 100)
        return item


# 净化正文，主动去除一些标记
class BillionJinghuaPipeline(PipeLineFather):

    def process_the_item(self, item, spider):
        html_content = item.get("html_content")
        html_content = re.sub(r"（.*）", "", html_content)
        html_content = re.sub(r"\[汽车之家.*\]", "", html_content)
        html_content = re.sub("&nbsp;", "", html_content)
        html_content = re.sub("<!--", "", html_content)
        html_content = re.sub("-->", "", html_content)
        item["html_content"] = html_content

        return item


class BillionsCaiPipeline(PipeLineFather):
    def __init__(self, store_uri):
        self.store_uri = store_uri

    @classmethod
    def from_settings(cls, settings):
        store_uri = settings['IMAGES_STORE']
        return cls(store_uri)

    def process_the_item(self, item, spider):


        for image in item.get('images'):
            if 'home.jpg' in image['path']:  # 如果是缩略图，就不裁。
                continue
            if (image['status'] == 'downloaded'):
                filePathOld = image['path']
                img = Image.open(self.store_uri + '/' + filePathOld)
                width, height = img.size
                cai = 30
                if (height - cai) > cai:  # 不能出现 图片左边纹理
                    cropped = img.crop((0, cai, width, height - cai))  # 左 # 上 #右 # 下
                    # 'd1ev/20230301185559556105/1.jpg'
                    filePathNew = filePathOld.replace(".jpg", "_bak.jpg")
                    filePathNew = Path().absolute() / self.store_uri / filePathNew
                    cropped.save(filePathNew)
                    pathold = Path().absolute() / self.store_uri / filePathOld
                    os.remove(pathold)
                    os.rename(filePathNew, pathold)
        return item


class BillionsDBPipeline(PipeLineFather):

    @classmethod
    def from_settings(cls, settings):
        store_uri = settings['IMAGES_STORE']
        return cls(store_uri)

    def __init__(self, store_uri):
        self.store_uri = store_uri

        from MySQLdb.cursors import DictCursor
        dbparms = dict(host="localhost",
                       user="root",
                       password="billions",
                       database="billion",
                       charset='utf8',
                       use_unicode=True,
                       cursorclass=DictCursor)

        self.dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

    def process_the_item(self, item, spider):

        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)
        return item

    def do_insert(self, cursor, item):
        sql = "insert into inews_test (itit,ihtml,wjj,ikey,imiao,biaoq,url,json) " \
              "values (%s,%s,%s,%s,%s,%s,%s,%s)"

        params = list()
        params.append(item.get("itit", " "))
        params.append(item.get("html_content", " "))
        # 只有当图片下载成功的时候，图片的wjj才需要入数据库。
        imageDownLoad = False
        for image in item.get('images'):
            if (image['status'] == 'downloaded'):
                imageDownLoad = True
        if imageDownLoad:
            params.append(item.get("wjj", " "))
        else:
            params.append(" ")
        params.append(item.get("ikey", " "))
        params.append(item.get("imiao", " ").replace("'", "''"))
        params.append(item.get("biaoq", " "))
        params.append(item.get("newsUrl", " "))
        json1 = json.dumps(dict(item))
        params.append(json1)

        cursor.execute(sql, tuple(params))

    def handle_error(self, failure, item, spider):
        image_path = item.get('image_path', "default")
        path = Path().absolute() / self.store_uri / image_path / item.get("wjj")
        shutil.rmtree(path)
        logging.error(failure)
        logging.error(dict(item))
        print(failure)
