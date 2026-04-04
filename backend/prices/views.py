from django.shortcuts import render
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import ShopItem
from .serializers import ShopItemSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import SelectedComponentSerializer

class ShopItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ShopItem.objects.filter(content_type__isnull=False)
    serializer_class = ShopItemSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['shop_name', 'content_type']

@api_view(['GET'])
def get_component_with_shop(request, component_id, content_type_id, shop_item_id):
    """ Возвращает компонент с конкретным магазином """
    from django.contrib.contenttypes.models import ContentType
    ct = ContentType.objects.get(id=content_type_id)
    model = ct.model_class()
    component = model.objects.get(id=component_id)
    shop_item = ShopItem.objects.get(id=shop_item_id)
    
    serializer = SelectedComponentSerializer.from_objects(component, shop_item)
    return Response(serializer.data)