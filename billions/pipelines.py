# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from io import BytesIO
from pathlib import Path

from PIL import Image
from scrapy import Selector
from scrapy.pipelines.images import ImagesPipeline, ImageException
import re
import os
from twisted.enterprise import adbapi



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


class BillionsHtmlReplaceImagePathPipeline():
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
        # 对文章进行 nohtml 处理
        html_content = re.sub(r"<(.[^>]*)>", "", html_content)
        html_content = re.sub(r"\r", "", html_content)
        html_content = re.sub(r"\t", "", html_content)
        for i in range(20):
            html_content = re.sub(r"  ", " ", html_content)

        item["html_content"] = html_content
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

    def process_item(self, item, spider):
        dbpool = adbapi.ConnectionPool("dbmodule", 'mydb', 'andrew', 'password')
        return item
