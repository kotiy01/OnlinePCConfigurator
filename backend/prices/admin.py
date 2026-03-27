from django.contrib import admin
from .models import ShopItem

@admin.register(ShopItem)
class ShopItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop_name', 'name', 'price', 'in_stock', 'last_seen', 'component')
    list_filter = ('shop_name', 'in_stock', 'category')
    search_fields = ('name', 'shop_item_id')
