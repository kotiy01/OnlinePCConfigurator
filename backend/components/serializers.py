from rest_framework import serializers
from .models import CPU, GPU, Motherboard, RAM, Storage, Case, PowerSupply, CPUCooler, CaseFan
from django.contrib.contenttypes.models import ContentType
from prices.models import ShopItem
from django.db import models

class BaseComponentSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    shop_name = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    in_stock = serializers.SerializerMethodField()

    min_price = serializers.SerializerMethodField()
    # shop_items = serializers.SerializerMethodField()

    def get_min_price(self, obj):
        model = obj._meta.model
        ct = ContentType.objects.get_for_model(model)
        min_price = ShopItem.objects.filter(
            content_type=ct,
            object_id=obj.id,
            in_stock=True
        ).aggregate(models.Min('price'))['price__min']
        return min_price

    # def get_shop_items(self, obj):
    #     model = obj._meta.model
    #     ct = ContentType.objects.get_for_model(model)
    #     shop_items = ShopItem.objects.filter(
    #         content_type=ct,
    #         object_id=obj.id,
    #         in_stock=True
    #     ).values('shop_name', 'price', 'url').order_by('price')  # сортируем по цене
    #     return list(shop_items)

    def get_shop_item(self, obj):
        model = obj._meta.model
        ct = ContentType.objects.get_for_model(model)
        return ShopItem.objects.filter(
            content_type=ct,
            object_id=obj.id,
            in_stock=True
        ).first()
    
    def get_name(self, obj):
        shop_item = self.get_shop_item(obj)
        return shop_item.name if shop_item else None

    def get_shop_name(self, obj):
        shop_item = self.get_shop_item(obj)
        return shop_item.shop_name if shop_item else None

    def get_price(self, obj):
        shop_item = self.get_shop_item(obj)
        return shop_item.price if shop_item else None

    def get_url(self, obj):
        shop_item = self.get_shop_item(obj)
        return shop_item.url if shop_item else None

    def get_image_url(self, obj):
        shop_item = self.get_shop_item(obj)
        return shop_item.image_url if shop_item else None

    def get_in_stock(self, obj):
        shop_item = self.get_shop_item(obj)
        return shop_item.in_stock if shop_item else False

class CPUSerializer(BaseComponentSerializer):
    class Meta:
        model = CPU
        fields = '__all__'

class GPUSerializer(BaseComponentSerializer):
    class Meta:
        model = GPU
        fields = '__all__'

class MotherboardSerializer(BaseComponentSerializer):
    class Meta:
        model = Motherboard
        fields = '__all__'

class RAMSerializer(BaseComponentSerializer):
    class Meta:
        model = RAM
        fields = '__all__'

class StorageSerializer(BaseComponentSerializer):
    class Meta:
        model = Storage
        fields = '__all__'

class CaseSerializer(BaseComponentSerializer):
    class Meta:
        model = Case
        fields = '__all__'

class PowerSupplySerializer(BaseComponentSerializer):
    class Meta:
        model = PowerSupply
        fields = '__all__'

class CPUCoolerSerializer(BaseComponentSerializer):
    class Meta:
        model = CPUCooler
        fields = '__all__'

class CaseFanSerializer(BaseComponentSerializer):
    class Meta:
        model = CaseFan
        fields = '__all__'