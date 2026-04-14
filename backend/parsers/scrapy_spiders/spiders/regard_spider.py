import scrapy
import re
from urllib.parse import urljoin
from ..items import ShopItem

class RegardSpider(scrapy.Spider):
    name = 'regard'
    allowed_domains = ['regard.ru']
    start_urls = [
        ('https://www.regard.ru/catalog/1001/processory', 'CPU'),
        ('https://www.regard.ru/catalog/1000/materinskie-platy', 'Motherboard'),
        ('https://www.regard.ru/catalog/1010/operativnaya-pamyat', 'RAM'),
        ('https://www.regard.ru/catalog/1013/videokarty', 'GPU'),
        ('https://www.regard.ru/catalog/1015/nakopiteli-ssd', 'Storage'),
        ('https://www.regard.ru/catalog/1032/korpusa', 'Case'),
        ('https://www.regard.ru/catalog/1225/bloki-pitaniya', 'PowerSupply'),
        ('https://www.regard.ru/catalog/5162/kulery-dlya-processorov', 'CPUCooler'),
        ('https://www.regard.ru/catalog/1004/ventilyatory-dlya-korpusa', 'CaseFan'),
        ('https://www.regard.ru/catalog/1008/zidkostnoe-oxlazdenie-szo', 'CPUCooler'),
    ]

    custom_settings = {
        'DOWNLOAD_DELAY': 5,                 # задержка между запросами
        'RANDOMIZE_DOWNLOAD_DELAY': True,    # случайная задержка
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1, # только один запрос за раз
        'AUTOTHROTTLE_ENABLED': True,        # автоматическое управление скоростью
        'AUTOTHROTTLE_START_DELAY': 1,
        'AUTOTHROTTLE_MAX_DELAY': 8,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 1.0,
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'COOKIES_ENABLED': True,
        'RETRY_TIMES': 3,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 403, 408, 429],
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Referer': 'https://www.regard.ru/',
        }
    }

    def start_requests(self):
        for url, category in self.start_urls:
            yield scrapy.Request(url, meta={'category': category}, callback=self.parse_category)

    def parse_category(self, response):
        category = response.meta['category']
        products = response.css('div.Card_wrap__hES44')
        if not products:
            self.logger.error(f"No products found on {response.url}")
            return

        self.logger.info(f'Found {len(products)} products on {response.url}')

        for prod in products:
            item = ShopItem()
            item['shop_name'] = 'regard.ru'
            item['category'] = category

            # Название
            name = prod.css('.CardText_title__7bSbO::text').get()
            if not name:
                name = prod.css('.CardText_title__7bSbO span::text').get()
            if name:
                item['name'] = name.strip()
            else:
                self.logger.warning(f"No name found, skipping product on {response.url}")
                continue

            # Цена
            price = prod.css('.Price_price__m2aSe::text').get()
            price_parts = prod.css('.Price_price__m2aSe ::text').getall()
            price_text = ''.join(price_parts)
            if price_text:
                price_clean = re.sub(r'[^\d]', '', price_text)
                if price_clean:
                    item['price'] = price_clean

            # Ссылка
            link = prod.css('a.CardText_link__C_fPZ::attr(href)').get()
            if link:
                item['url'] = urljoin(response.url, link)
            else:
                continue

            # Артикул магазина
            id_text = prod.css('.CardId_id__mCbo0::text').get()
            if id_text:
                match = re.search(r'ID:\s*(\d+)', id_text)
                if match:
                    item['shop_item_id'] = match.group(1)

            # Наличие
            stock_text = prod.css('p.Card_inStockText__ciAyD::text').get()
            if stock_text:
                item['in_stock'] = 'в наличии' in stock_text.lower()

            # Изображение
            img = prod.css('img.CardImageSlider_image__W65ZP::attr(src)').get()
            if img:
                item['image_url'] = urljoin(response.url, img)

            # Извлечение MPN
            yield scrapy.Request(
                item['url'],
                meta={'item': item},
                callback=self.parse_product_page
            )

        # Пагинация
        next_page = response.css('a[rel="next"]::attr(href)').get()
        if not next_page:
            next_page = response.xpath('//a[contains(text(), "Далее")]/@href').get()
        if next_page:
            yield scrapy.Request(
                urljoin(response.url, next_page),
                meta={'category': category},
                callback=self.parse_category
            )

    def parse_product_page(self, response):
        item = response.meta['item']
        mpn = None
        spec_items = response.css('.CharacteristicsItem_item__QnlK2')
        for si in spec_items:
            label = si.css('.CharacteristicsItem_name__Q7B8V span::text').get()
            if label and 'Код производителя' in label:
                value = si.css('.CharacteristicsItem_value__fgPkc .CharacteristicsItem_valueData__d_mHr::text').get()
                if value:
                    mpn = value.strip()
                    break
        if mpn:
            item['extracted_mpn'] = mpn
        yield item