import logging
from scrapy.exceptions import DropItem
from prices.models import ShopItem as DjangoShopItem

logger = logging.getLogger(__name__)

class SavePipeline:
    def process_item(self, item, spider):
        data = {
            'shop_name': item.get('shop_name'),
            'shop_item_id': item.get('shop_item_id', ''),
            'name': item.get('name', ''),
            'price': item.get('price'),
            'currency': item.get('currency', 'RUB'),
            'in_stock': item.get('in_stock', True),
            'url': item.get('url', ''),
            'image_url': item.get('image_url', ''),
            'extracted_mpn': item.get('extracted_mpn', ''),
            'normalized_name': item.get('normalized_name', ''),
            'category': item.get('category', ''),
        }
        try:
            obj, created = DjangoShopItem.objects.update_or_create(
                shop_name=data['shop_name'],
                shop_item_id=data['shop_item_id'],
                defaults=data
            )
            spider.logger.debug(f"Saved ShopItem {obj.id} (created={created}) for {data['name']}")
        except Exception as e:
            spider.logger.error(f"Error saving ShopItem: {e}")
        return item