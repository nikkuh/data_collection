# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import re


class LibScraperPipeline:

    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        self.book_base = client['111121']

    def process_item(self, item, spider):

        item['authors'], item['name'] = item.pop('title').split(': ')
        item['base_price'] = int(item['base_price'])
        item['final_price'] = int(item['final_price'])
        item['rating'] = float(item['rating'])
        item['_id'] = int(re.findall(r'\d+', item['url'])[0])
        if not item['final_price']:
            item['final_price'] = item['base_price']

        collection = self.book_base[spider.name]
        collection.insert_one(item)

        return item
