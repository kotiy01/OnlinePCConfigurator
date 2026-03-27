from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class ShopItem(models.Model):
    # Связь с эталонным компонентом
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    component = GenericForeignKey('content_type', 'object_id')

    # Данные из магазина
    shop_name = models.CharField(max_length=100, default='regard.ru')
    shop_item_id = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='RUB')
    in_stock = models.BooleanField(default=True)
    url = models.URLField(max_length=500)
    image_url = models.URLField(max_length=500, blank=True)

    # Поля для сопоставления
    extracted_mpn = models.CharField(max_length=100, blank=True, db_index=True)
    normalized_name = models.CharField(max_length=500, blank=True, db_index=True)

    # Категория
    category = models.CharField(max_length=50, blank=True, db_index=True)

    # Дата получения
    last_seen = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('shop_name', 'shop_item_id')
        indexes = [
            models.Index(fields=['shop_name', 'last_seen']),
            models.Index(fields=['extracted_mpn']),
        ]

    def __str__(self):
        return f"{self.name} ({self.shop_name})"