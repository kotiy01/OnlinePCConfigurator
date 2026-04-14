import scrapy
import re
from urllib.parse import urljoin
from ..items import ShopItem

class Pc4gamesSpider(scrapy.Spider):
    name = 'pc4games'
    allowed_domains = ['pc4games.ru']
    start_urls = [
        ('https://pc4games.ru/catalog/protsessory/', 'CPU'),
        ('https://pc4games.ru/catalog/materinskie_platy/', 'Motherboard'),
        ('https://pc4games.ru/catalog/operativnaya_pamyat/', 'RAM'),
        ('https://pc4games.ru/catalog/videokarty/', 'GPU'),
        ('https://pc4games.ru/catalog/zhestkie_diski_ssd/', 'Storage'),
        ('https://pc4games.ru/catalog/korpusa/', 'Case'),
        ('https://pc4games.ru/catalog/bloki_pitaniya/', 'PowerSupply'),
        ('https://pc4games.ru/catalog/ventilyatory_i_sistemy_okhlazhdeniya/', 'Cooling'),
    ]

    custom_settings = {
        'DOWNLOAD_DELAY': 3,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'COOKIES_ENABLED': True,
        'RETRY_TIMES': 3,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 403, 408],
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Referer': 'https://pc4games.ru/',
        }
    }

    def start_requests(self):
        for url, category in self.start_urls:
            yield scrapy.Request(url, meta={'category': category}, callback=self.parse_category)

    def parse_category(self, response):
        category = response.meta['category']
        products = response.css('div.catalog_item_wrapp')
        if not products:
            self.logger.error(f"No products found on {response.url}")
            return

        self.logger.info(f'Found {len(products)} products on {response.url}')

        for prod in products:
            item = ShopItem()
            item['shop_name'] = 'pc4games.ru'
            item['category'] = category

            # Название
            name = prod.css('.item-title a span::text').get()
            if not name:
                name = prod.css('.item-title a::text').get()
            if name:
                item['name'] = name.strip()
            else:
                continue  # пропускаем без названия

            if category == 'Cooling':
                name_lower = name.lower()
                if 'cpu' in name_lower or 'процессор' in name_lower or 'кулер' in name_lower:
                    item['category'] = 'CPUCooler'
                else:
                    item['category'] = 'CaseFan'
            else:
                item['category'] = category

            # Цена
            price = prod.css('.price_value::text').get()
            if price:
                price_clean = re.sub(r'[^\d]', '', price)
                if price_clean:
                    item['price'] = price_clean

            # Артикул магазина (shop_item_id)
            article_text = prod.css('.article_block .muted::text').get()
            if article_text:
                match = re.search(r'Арт\.:\s*(\S+)', article_text)
                if match:
                    item['shop_item_id'] = match.group(1)

            # Ссылка
            link = prod.css('a.thumb::attr(href)').get()
            if link:
                item['url'] = urljoin(response.url, link)
            else:
                continue

            # Наличие
            stock_text = prod.css('.item-stock .value::text').get()
            if stock_text:
                item['in_stock'] = 'Доступно' in stock_text or 'Достаточно' in stock_text or 'Много' in stock_text or 'Мало' in stock_text


            # Изображение
            img = prod.css('img.lazy::attr(data-src)').get()
            if not img:
                img = prod.css('img::attr(src)').get()
            if img:
                item['image_url'] = urljoin(response.url, img)

            # Извлечение MPN
            yield scrapy.Request(
                item['url'],
                meta={'item': item},
                callback=self.parse_product_page,
                dont_filter=True,
                errback=self.handle_error
            )

        # Пагинация
        next_page = response.css('a.flex-next::attr(href)').get()
        if not next_page:
            current = response.css('.module-pagination .cur::text').get()
            if current:
                current_num = int(current)
                next_num = current_num + 1
                next_link = response.css(f'.module-pagination a[href*="PAGEN_1={next_num}"]::attr(href)').get()
                if next_link:
                    next_page = next_link
        if next_page:
            yield response.follow(next_page, callback=self.parse_category, meta={'category': category})

    def parse_product_page(self, response):
        item = response.meta['item']
        mpn = None

        rows = response.css('table.props_list tr')
        for row in rows:
            label = row.css('td.char_name .js-prop-title::text').get()
            if label and 'Код производителя' in label:
                mpn = row.css('td.char_value .js-prop-value::text').get()
                if mpn:
                    mpn = mpn.strip()
                    break

        if mpn:
            item['extracted_mpn'] = mpn
        yield item