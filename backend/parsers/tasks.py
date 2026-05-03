from celery import shared_task
from django.core.management import call_command
import logging

logger = logging.getLogger(__name__)

@shared_task
def parse_regard():
    """ Парсинг regard.ru """
    call_command('parse_regard')
    return "Regard.ru parsing completed"

@shared_task
def parse_pc4games():
    """ Парсинг pc4games.ru """
    call_command('parse_pc4games')
    return "pc4games.ru parsing completed"

@shared_task
def match_all_shop_items():
    """ Матчинг товаров """
    call_command('match_mpn')
    return "Matching completed"