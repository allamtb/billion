# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from io import BytesIO
from pathlib import Path

import MySQLdb
from MySQLdb import _mysql
from PIL import Image
from scrapy import Selector
from scrapy.pipelines.images import ImagesPipeline, ImageException
import re
import os
from twisted.enterprise import adbapi


# 下载图片、缩略图
from billions.util.htmlUtil import imiao, noHtml


class BillionsImagePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        # image_guid = hashlib.sha`1(to_bytes(request.url)).hexdigest()
        image_urls = item.get('image_urls', [])
        image_path = item.get('image_path', "default")
        wjj = item.get('wjj', 'error')
        image_guid = image_urls.index(request.url)
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
        yield path, image, buf
        image_urls = item.get('image_urls', [])
        image_path = item.get('image_path', "default")
        homeTuUrl = item.get('homeTuUrl', "none")
        wjj = item.get('wjj', 'error')
        image_guid = image_urls.index(request.url)
        thumb_path = f'{image_path}/{wjj}/home.jpg'
        if image_guid == 0 and homeTuUrl != "none":  # 只有第一张图片,且不存在缩略图的时候，才需要生成缩略图
            thumb_image, thumb_buf = self.convert_image(image, (270, 270))
            yield thumb_path, thumb_image, thumb_buf


# 替换文章中图片的路径
class BillionsReplaceImage1PathPipeline():
    def process_item(self, item, spider):

        html_content = item.get("html_content")
        # 替换文章中的图片地址为已经下载好的图片地址
        for image in item.get('images'):
            if (image['status'] == 'downloaded'):
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


class BillionsNoHtmlTagPipeline():
    def process_item(self, item, spider):
        html_content = item.get("html_content")
        item["html_content"] =  noHtml(html_content)
        return item


# 替换文章中图片的路径回来，同时添加上 tag 信息
class BillionsReplaceImage2PathPipeline():
    def process_item(self, item, spider):
        html_content = item.get("html_content")
        #todo 对alt添加标签
        html_content = re.sub("eeimg", "<img alt=\"\" src=\"/eeimg/{HostI}/img",html_content)
        item["html_content"] = html_content
        return item

class BillionImiaoPipeline():
    def process_item(self, item, spider):
        html_content = item.get("html_content")
        html_content = noHtml(html_content)
        item["imiao"] = imiao(html_content,100)
        return item


class BillionsCaiPipeline():
    def process_item(self, item, spider):
        for image in item.get('images'):
            if (image['status'] == 'downloaded'):
                filePathOld = image['path']
                img = Image.open('image/' + filePathOld)
                width, height = img.size
                cai = 30
                cropped = img.crop((0, cai, width, height - cai))  # 左 # 上 #右 # 下
                # 'd1ev/20230301185559556105/1.jpg'
                filePathNew = filePathOld.replace(".jpg", "_bak.jpg")
                filePathNew = Path().absolute() / "image" / filePathNew
                cropped.save(filePathNew)
                pathold = Path().absolute() / "image" / filePathOld
                os.remove(pathold)
                os.rename(filePathNew, pathold)
        return item


class BillionsDBPipeline():
    def __init__(self):
        from MySQLdb.cursors import DictCursor
        dbparms =  dict(host="localhost",
                        user="root",
                        password="billions",
                        database="billion",
                        charset='utf8',
                        use_unicode=True,
                        cursorclass=DictCursor)

        self.dbpool = adbapi.ConnectionPool("MySQLdb",**dbparms)

    def process_item(self, item, spider):

        query = self.dbpool.runInteraction(self.do_insert,item)
        query.addErrback(self.handle_error,item,spider)

        return item

    def do_insert(self,cursor,item):
        sql = "insert into inews (itit,ihtml,wjj,ikey,imiao,biaoq,url,json) " \
              "values (%s,%s,%s,%s,%s,%s,%s,%s)"

        params = list()

        params.append(item.get("itit"," "))   #todo
        params.append(item.get("html_content", " "))
        params.append(item.get("wjj"))
        params.append(item.get("ikey"," "))   # todo
        params.append(item.get("imiao"," ").replace("'","''"))
        params.append(item.get("biaoq"," ")) # todo
        params.append(item.get("url"," "))   # todo
        params.append(item.get("json", "[ ]"))  #todo

        cursor.execute(sql, tuple(params))

    def handle_error(self,failure, item,spider):
        print(failure)

