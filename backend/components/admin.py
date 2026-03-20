from django.contrib import admin

from .models import (
    CPU, GPU, Motherboard, RAM, Storage, CPUCooler, Case, CaseFan, PowerSupply
)

# Базовый класс для настройки общих полей
class BaseComponentAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'mpn', 'opendb_id')
    search_fields = ('name', 'brand', 'mpn')
    list_filter = ('brand')
    readonly_fields = ('opendb_id',) # защищита от случайного изменения

@admin.register(CPU)
class CPUAdmin(BaseComponentAdmin):
    list_display = ('name', 'brand', 'socket', 'cores_total', 'threads', 'tdp')
    list_filter = ('brand', 'socket', 'cores_total')
    search_fields = ('name', 'brand', 'mpn', 'socket')

@admin.register(GPU)
class GPUAdmin(BaseComponentAdmin):
    list_display = ('name', 'brand', 'chipset', 'memory')
    list_filter = ('brand', 'chipset_manufacturer', 'memory_type')
    search_fields = ('name', 'brand', 'chipset')

@admin.register(Motherboard)
class MotherboardAdmin(BaseComponentAdmin):
    list_display = ('name', 'brand', 'socket', 'form_factor', 'chipset')
    list_filter = ('brand', 'socket', 'form_factor', 'chipset')
    search_fields = ('name', 'brand', 'socket', 'chipset')

@admin.register(RAM)
class RAMAdmin(BaseComponentAdmin):
    list_display = ('name', 'brand', 'ram_type', 'total_capacity', 'speed')
    list_filter = ('brand', 'ram_type', 'speed')
    search_fields = ('name', 'brand')

@admin.register(Storage)
class StorageAdmin(BaseComponentAdmin):
    list_display = ('name', 'brand', 'type', 'capacity', 'form_factor', 'interface')
    list_filter = ('brand', 'type', 'interface')
    search_fields = ('name', 'brand')

@admin.register(CPUCooler)
class CPUCoolerAdmin(BaseComponentAdmin):
    list_display = ('name', 'brand', 'height', 'water_cooled', 'fanless')
    list_filter = ('brand', 'water_cooled', 'fanless')
    search_fields = ('name', 'brand')

@admin.register(Case)
class CaseAdmin(BaseComponentAdmin):
    list_display = ('name', 'brand', 'case_type', 'color')
    list_filter = ('brand', 'case_type', 'has_transparent_side_panel')
    search_fields = ('name', 'brand')

@admin.register(CaseFan)
class CaseFanAdmin(BaseComponentAdmin):
    list_display = ('name', 'brand', 'size', 'quantity', 'led')
    list_filter = ('brand', 'size', 'pwm', 'led')
    search_fields = ('name', 'brand')

@admin.register(PowerSupply)
class PowerSupplyAdmin(BaseComponentAdmin):
    list_display = ('name', 'brand', 'wattage', 'form_factor', 'efficiency_rating', 'modular')
    list_filter = ('brand', 'form_factor', 'efficiency_rating', 'modular')
    search_fields = ('name', 'brand')
