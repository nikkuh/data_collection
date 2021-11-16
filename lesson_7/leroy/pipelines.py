# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient


class LeroyPipeline:
    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        self.leroy_base = client['16_11_2021']

    def process_item(self, item, spider):
        collection = self.leroy_base[spider.name]
        collection.insert_one(item)

        return item

class LeroyLargePhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['large_images']:
            for img in item['large_images']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['large_images'] = [itm[1] for itm in results if itm[0]]
        return item

class LeroySmallPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['small_images']:
            for img in item['small_images']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['small_images'] = [itm[1] for itm in results if itm[0]]
        return item