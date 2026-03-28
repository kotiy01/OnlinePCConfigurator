from django.shortcuts import render
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import ShopItem
from .serializers import ShopItemSerializer

class ShopItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ShopItem.objects.filter(content_type__isnull=False)
    serializer_class = ShopItemSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['shop_name', 'content_type']
