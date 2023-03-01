# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from io import BytesIO
from scrapy.pipelines.images import ImagesPipeline, ImageException

class BillionsImagePipeline(ImagesPipeline):


    def file_path(self, request, response=None, info=None, *, item=None):
        # image_guid = hashlib.sha`1(to_bytes(request.url)).hexdigest()
        image_urls=  item.get('image_urls',[])
        image_path=  item.get('image_path',"default")
        wjj = item.get('wjj','error')
        image_guid =image_urls.index(request.url)
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
        if image_guid ==0 and homeTuUrl != "none":  #只有第一张图片,且不存在缩略图的时候，才需要生成缩略图
            thumb_image, thumb_buf = self.convert_image(image,(270, 270))
            yield thumb_path, thumb_image, thumb_buf



class BillionsHtmlContentPipeline():

    def process_item(self, item, spider):

        path = item.get('images')[0]["path"]

        print(path)