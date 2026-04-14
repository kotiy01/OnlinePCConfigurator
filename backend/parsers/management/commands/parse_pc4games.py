from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os

class Command(BaseCommand):
    help = 'Parse pc4games.ru for all components'

    def handle(self, *args, **options):
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'parsers.scrapy_spiders.settings')
        from parsers.scrapy_spiders.spiders.pc4games_spider import Pc4gamesSpider

        process = CrawlerProcess(get_project_settings())
        process.crawl(Pc4gamesSpider)
        process.start()

        self.stdout.write(self.style.SUCCESS('Parsing completed'))