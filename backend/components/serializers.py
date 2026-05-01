from rest_framework import serializers
from .models import CPU, GPU, Motherboard, RAM, Storage, Case, PowerSupply, CPUCooler, CaseFan
from django.contrib.contenttypes.models import ContentType
from prices.models import ShopItem
from django.db import models
from django.contrib.auth.models import User
from .models import Profile, SavedBuild

class BaseComponentSerializer(serializers.ModelSerializer):
    min_price = serializers.SerializerMethodField()
    shop_items = serializers.SerializerMethodField()

    def get_min_price(self, obj):
        # model = obj._meta.model
        ct = ContentType.objects.get_for_model(obj._meta.model)
        min_price = ShopItem.objects.filter(
            content_type=ct,
            object_id=obj.id,
            in_stock=True
        ).aggregate(models.Min('price'))['price__min']
        return min_price

    def get_shop_items(self, obj):
        model = obj._meta.model
        ct = ContentType.objects.get_for_model(model)
        shop_items = ShopItem.objects.filter(
            content_type=ct,
            object_id=obj.id,
            in_stock=True
        ).values('id', 'name', 'shop_name', 'in_stock', 'price', 'url', 'image_url').order_by('price')  # сортировка по цене
        return list(shop_items)

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



class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'avatar', 'date_joined')

    def get_avatar(self, obj):
        if hasattr(obj, 'profile') and obj.profile.avatar:
            return obj.profile.avatar
        return None

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password2 = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': 'Пароли не совпадают'})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user)
        return user

class SavedBuildSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedBuild
        fields = ('id', 'name', 'build_data', 'created_at', 'updated_at')