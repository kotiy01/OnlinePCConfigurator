from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os
import sys
from pathlib import Path

class Command(BaseCommand):
    help = 'Parse Regard.ru for all components'

    def handle(self, *args, **options):
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'parsers.scrapy_spiders.settings')
        from parsers.scrapy_spiders.spiders.regard_spider import RegardSpider

        process = CrawlerProcess(get_project_settings())
        process.crawl(RegardSpider)
        process.start()

        self.stdout.write(self.style.SUCCESS('Parsing completed'))