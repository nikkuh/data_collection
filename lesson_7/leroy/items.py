# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst


def process_price(value:str):
    try:
        value = value.replace(' ', '')
        value = int(value)
    except Exception as e:
        print(e)
    finally:
        return value

class LeroyItem(scrapy.Item):
    # define the fields for your item here like:

    url = scrapy.Field(output_processor=TakeFirst())
    _id = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(process_price), output_processor=TakeFirst())
    small_images = scrapy.Field()
    large_images = scrapy.Field()

