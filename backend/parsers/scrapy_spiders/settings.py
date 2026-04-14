BOT_NAME = 'Spider-Man'
SPIDER_MODULES = ['parsers.scrapy_spiders.spiders']
NEWSPIDER_MODULE = 'parsers.scrapy_spiders.spiders'

ROBOTSTXT_OBEY = False
HTTPCACHE_ENABLED = True

TWISTED_REACTOR = 'twisted.internet.selectreactor.SelectReactor'

DOWNLOAD_DELAY = 3
RANDOMIZE_DOWNLOAD_DELAY = True

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

COOKIES_ENABLED = True
RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 403, 408]

LOG_LEVEL = 'INFO'

ITEM_PIPELINES = {
    'parsers.scrapy_spiders.pipelines.SavePipeline': 300,
}