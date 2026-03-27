import scrapy

class ShopItem(scrapy.Item):
    shop_name = scrapy.Field()
    shop_item_id = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    in_stock = scrapy.Field()
    url = scrapy.Field()
    image_url = scrapy.Field()
    extracted_mpn = scrapy.Field()
    normalized_name = scrapy.Field()
    category = scrapy.Field()