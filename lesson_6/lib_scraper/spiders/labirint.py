import scrapy
from scrapy.http import HtmlResponse
from lib_scraper.items import LibScraperItem

# Сюда вводим поисковый запрос для сайта
search_field_input = 'java'

class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    start_urls = [f'https://www.labirint.ru/search/{search_field_input}/?stype=0']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@class='pagination-next__text']/@href").getall()[1]
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//a[@class = 'product-title-link']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.book_parse)

    def book_parse(self, response: HtmlResponse):

        url = response.url
        title = response.xpath("//h1/text()").get()
        base_price = response.xpath("//span[@class = 'buying-price-val-number']/text()").get()
        if not base_price:
            base_price = response.xpath("//span[@class = 'buying-priceold-val-number']/text()").get()
        final_price = response.xpath("//span[@class = 'buying-pricenew-val-number']/text()").get()
        rating = response.xpath("//div[@id = 'rate']/text()").get()
        yield LibScraperItem(url= url, title= title, base_price= base_price,
                             rating = rating, final_price = final_price)