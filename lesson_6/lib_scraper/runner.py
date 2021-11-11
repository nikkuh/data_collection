from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from lib_scraper.spiders.labirint import LabirintSpider
from lib_scraper import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LabirintSpider)
    process.start()