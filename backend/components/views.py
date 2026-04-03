from django.shortcuts import render
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import CPU, GPU, Motherboard, RAM, Storage, Case, PowerSupply, CPUCooler, CaseFan
from .serializers import CPUSerializer, GPUSerializer, MotherboardSerializer, RAMSerializer, StorageSerializer, CaseSerializer, PowerSupplySerializer, CPUCoolerSerializer, CaseFanSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from compatibility.checker import check_compatibility
from django.db.models import Exists, OuterRef
from prices.models import ShopItem
from django.contrib.contenttypes.models import ContentType

class HasPricesMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        has_prices = self.request.query_params.get('has_prices')
        if has_prices and has_prices.lower() == 'true':
            content_type = ContentType.objects.get_for_model(self.queryset.model)
            queryset = queryset.filter(
                Exists(ShopItem.objects.filter(
                    content_type=content_type,
                    object_id=OuterRef('id'),
                    in_stock=True
                ))
            )
        return queryset

class CPUViewSet(HasPricesMixin, viewsets.ReadOnlyModelViewSet):
    """ API для просмотра процессоров """
    queryset = CPU.objects.filter(is_verified=True)
    serializer_class = CPUSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['socket', 'brand', 'cores_total', 'base_clock', 'boost_clock']
    search_fields = ['name', 'brand', 'series']
    ordering_fields = ['price']
    ordering = ['brand', 'name']

class GPUViewSet(HasPricesMixin, viewsets.ReadOnlyModelViewSet):
    """ API для просмотра видеокарт """
    queryset = GPU.objects.filter(is_verified=True)
    serializer_class = GPUSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['memory', 'brand', 'memory_type', 'interface']
    search_fields = ['name', 'brand', 'series']
    ordering_fields = ['price']
    ordering = ['brand', 'name']

class MotherboardViewSet(HasPricesMixin, viewsets.ReadOnlyModelViewSet):
    """ API для просмотра материнских плат """
    queryset = Motherboard.objects.filter(is_verified=True)
    serializer_class = MotherboardSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['socket', 'brand', 'form_factor', 'chipset', 'memory_type']
    search_fields = ['name', 'brand', 'series']
    ordering_fields = ['price']
    ordering = ['brand', 'name']

class RAMViewSet(HasPricesMixin, viewsets.ReadOnlyModelViewSet):
    """ API для просмотра оперативной памяти """
    queryset = RAM.objects.filter(is_verified=True)
    serializer_class = RAMSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['total_capacity', 'brand', 'speed', 'ram_type', 'modules_quantity']
    search_fields = ['name', 'brand', 'series']
    ordering_fields = ['price']
    ordering = ['brand', 'name']

class StorageViewSet(HasPricesMixin, viewsets.ReadOnlyModelViewSet):
    """ API для просмотра накопителей """
    queryset = Storage.objects.filter(is_verified=True)
    serializer_class = StorageSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['capacity', 'brand', 'type', 'form_factor', 'interface']
    search_fields = ['name', 'brand', 'series']
    ordering_fields = ['price']
    ordering = ['brand', 'name']

class CaseViewSet(HasPricesMixin, viewsets.ReadOnlyModelViewSet):
    """ API для просмотра корпусов """
    queryset = Case.objects.filter(is_verified=True)
    serializer_class = CaseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['case_type', 'brand', 'supported_motherboard_form_factors', 'has_transparent_side_panel']
    search_fields = ['name', 'brand', 'series']
    ordering_fields = ['price']
    ordering = ['brand', 'name']

class PowerSupplyViewSet(HasPricesMixin, viewsets.ReadOnlyModelViewSet):
    """ API для просмотра блоков питания """
    queryset = PowerSupply.objects.filter(is_verified=True)
    serializer_class = PowerSupplySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['wattage', 'brand', 'form_factor', 'efficiency_rating']
    search_fields = ['name', 'brand', 'series']
    ordering_fields = ['price']
    ordering = ['brand', 'name']

class CPUCoolerViewSet(HasPricesMixin, viewsets.ReadOnlyModelViewSet):
    """ API для просмотра охлаждения процессора """
    queryset = CPUCooler.objects.filter(is_verified=True)
    serializer_class = CPUCoolerSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['cpu_sockets', 'brand', 'water_cooled', 'fan_quantity']
    search_fields = ['name', 'brand', 'series']
    ordering_fields = ['price']
    ordering = ['brand', 'name']

class CaseFanViewSet(HasPricesMixin, viewsets.ReadOnlyModelViewSet):
    """ API для просмотра вентиляторов """
    queryset = CaseFan.objects.filter(is_verified=True)
    serializer_class = CaseFanSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['size', 'brand', 'quantity', 'led', 'flow_direction']
    search_fields = ['name', 'brand', 'series']
    ordering_fields = ['price']
    ordering = ['brand', 'name']


@api_view(['POST'])
def compatibility_check(request):
    build = request.data.get('build', {})
    compatible, messages = check_compatibility(build)
    return Response({
        'compatible': compatible,
        'messages': messages,
    })