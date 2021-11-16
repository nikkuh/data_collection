import scrapy
from scrapy.http import HtmlResponse
from leroy.items import LeroyItem
from scrapy.loader import ItemLoader
num_pages = 2

class LightSpider(scrapy.Spider):
    name = 'light'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/catalogue/lampochki/']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[contains(@aria-label, 'Следующая страница')]/@href").getall()[0]
        for _ in range(num_pages):
            if next_page:
                yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//a[@data-qa = 'product-name']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.parse_link)
            print()

    def parse_link(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroyItem(), response=response)
        loader.add_value('url', response.url)
        loader.add_value('_id', response.url)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('price', "//span[@slot = 'price']/text()")
        loader.add_xpath('small_images', "//img[@slot = 'thumbs']/@src")
        loader.add_xpath('large_images', "//img[@alt = 'product image']/@src")
        yield loader.load_item()


