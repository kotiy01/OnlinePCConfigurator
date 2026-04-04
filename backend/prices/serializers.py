from rest_framework import serializers
from .models import ShopItem

class ShopItemSerializer(serializers.ModelSerializer):
    component_name = serializers.CharField(source='component.name', read_only=True)
    component_type = serializers.CharField(source='content_type.model', read_only=True)

    class Meta:
        model = ShopItem
        fields = ['id', 'shop_name', 'name', 'price', 'url', 'in_stock', 'component_name', 'component_type']

class SelectedComponentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    brand = serializers.CharField()
    # socket = serializers.CharField()
    # cores_total = serializers.IntegerField()
    # tdp = serializers.IntegerField()
    # ... другие нужные характеристики
    
    # Поля из ShopItem
    shop_name = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    url = serializers.URLField()
    image_url = serializers.URLField()
    in_stock = serializers.BooleanField()
    shop_item_id = serializers.IntegerField()
    
    @classmethod
    def from_objects(cls, component, shop_item):
        """ Фабричный метод для создания сериализатора из двух объектов """
        data = {
            'id': component.id,
            'name': component.name,
            'brand': component.brand,
            # 'socket': getattr(component, 'socket', None),
            # 'cores_total': getattr(component, 'cores_total', None),
            # 'tdp': getattr(component, 'tdp', None),
            'shop_name': shop_item.shop_name,
            'price': shop_item.price,
            'url': shop_item.url,
            'image_url': shop_item.image_url,
            'in_stock': shop_item.in_stock,
            'shop_item_id': shop_item.id,
        }
        return cls(data)