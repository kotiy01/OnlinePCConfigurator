from rest_framework import serializers
from .models import ShopItem

class ShopItemSerializer(serializers.ModelSerializer):
    component_name = serializers.CharField(source='component.name', read_only=True)
    component_type = serializers.CharField(source='content_type.model', read_only=True)

    class Meta:
        model = ShopItem
        fields = ['id', 'shop_name', 'name', 'price', 'url', 'in_stock', 'component_name', 'component_type']