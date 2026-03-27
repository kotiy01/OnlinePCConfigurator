import logging
from django.contrib.contenttypes.models import ContentType
from components.models import (
    CPU, Motherboard, RAM, GPU, Storage, Case, PowerSupply, CPUCooler, CaseFan
)
from prices.models import ShopItem

logger = logging.getLogger(__name__)

ALL_MODELS = [
    CPU, Motherboard, RAM, GPU, Storage, Case, PowerSupply, CPUCooler, CaseFan
]


def find_component_by_mpn(mpn):
    """ Поиск эталонного компонента по MPN """
    if not mpn:
        return None

    mpn_upper = mpn.upper().strip()

    for model in ALL_MODELS:
        # Поиск по полю mpn
        try:
            comp = model.objects.filter(mpn__iexact=mpn_upper).first()
            if comp:
                logger.debug(f"Found by mpn field: {comp}")
                return comp
        except Exception as e:
            logger.error(f"Error searching {model.__name__} by mpn field: {e}")

        # Поиск в part_numbers_json
        try:
            all_items = list(model.objects.filter(is_verified=True).values(
                'id', 'mpn', 'part_numbers_json', 'brand', 'name'
            ))
            for item in all_items:
                # Проверка поля mpn
                if item.get('mpn') and item['mpn'].upper() == mpn_upper:
                    return model.objects.get(id=item['id'])

                # Проверка part_numbers_json
                part_numbers = item.get('part_numbers_json')
                if part_numbers:
                    if isinstance(part_numbers, list):
                        if any(pn.upper() == mpn_upper for pn in part_numbers):
                            return model.objects.get(id=item['id'])
                    elif isinstance(part_numbers, str):
                        if part_numbers.upper() == mpn_upper:
                            return model.objects.get(id=item['id'])
        except Exception as e:
            logger.error(f"Error searching {model.__name__} in part_numbers_json: {e}")

    return None


class MPNMatcher:
    def __init__(self):
        self.stats = {
            'total': 0,
            'matched': 0,
            'by_mpn_field': 0,
            'by_part_numbers': 0,
            'errors': 0
        }

    def run(self, limit=None):
        """ Запуск матчинга для всех несопоставленных товаров """
        items = ShopItem.objects.filter(
            content_type__isnull=True,
            object_id__isnull=True,
            extracted_mpn__isnull=False
        ).exclude(extracted_mpn='')

        if limit:
            items = items[:limit]

        self.stats['total'] = items.count()
        logger.info(f"Starting MPN matching for {self.stats['total']} items")

        for item in items:
            mpn = item.extracted_mpn
            if not mpn:
                logger.debug(f"Skipping item without MPN: {item.name}")
                continue

            try:
                component = find_component_by_mpn(mpn)

                if component:
                    # Сохранение связи
                    content_type = ContentType.objects.get_for_model(component)
                    item.content_type = content_type
                    item.object_id = component.id
                    item.save()

                    self.stats['matched'] += 1

                    if component.mpn and component.mpn.upper() == mpn.upper():
                        self.stats['by_mpn_field'] += 1
                    else:
                        self.stats['by_part_numbers'] += 1

                    logger.info(f"✅ MATCHED: {item.name} -> {component}")
                else:
                    logger.info(f"❌ NO MATCH: {item.name} (MPN: {mpn})")

            except Exception as e:
                logger.error(f"Error matching item {item.id}: {e}")
                self.stats['errors'] += 1

        self._log_stats()
        return self.stats['matched']

    def _log_stats(self):
        """ Вывод статистики матчинга """
        logger.info("=" * 50)
        logger.info("MATCHING STATISTICS:")
        logger.info(f"  Total items processed: {self.stats['total']}")
        logger.info(f"  Matched: {self.stats['matched']}")
        logger.info(f"    - by mpn field: {self.stats['by_mpn_field']}")
        logger.info(f"    - by part_numbers_json: {self.stats['by_part_numbers']}")
        logger.info(f"  Not matched: {self.stats['total'] - self.stats['matched']}")
        logger.info(f"  Errors: {self.stats['errors']}")
        if self.stats['total'] > 0:
            logger.info(f"  Success rate: {self.stats['matched'] / self.stats['total'] * 100:.1f}%")
        logger.info("=" * 50)

if __name__ == "__main__":
    # Для тестирования
    import django
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()