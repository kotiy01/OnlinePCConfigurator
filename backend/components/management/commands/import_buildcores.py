import os
import json
import re
from datetime import datetime
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from components.models import (
    CPU, GPU, Motherboard, RAM, Storage, CPUCooler,
    Case, CaseFan, PowerSupply
)

class Command(BaseCommand):
    help = 'Import all components from BuildCores OpenDB'

    # Словарь соответствия имени папки
    FOLDER_TO_MODEL = {
        'CPU': CPU,
        'GPU': GPU,
        'Motherboard': Motherboard,
        'RAM': RAM,
        'Storage': Storage,
        'CPUCooler': CPUCooler,
        'Case': Case,
        'CaseFan': CaseFan,
        'PowerSupply': PowerSupply,
    }

    def add_arguments(self, parser):
        parser.add_argument('repo_path', type=str, help='Path to BuildCores OpenDB root folder')
        parser.add_argument('--category', type=str, help='Import only specific category')

    def handle(self, *args, **options):
        repo_path = options['repo_path']
        if not os.path.isdir(repo_path):
            self.stderr.write(self.style.ERROR(f'Path not found: {repo_path}'))
            return

        category_filter = options.get('category')

        # Проход по всем подпапкам первого уровня (уровня категории)
        for folder_name in os.listdir(repo_path):
            folder_path = os.path.join(repo_path, folder_name)
            if not os.path.isdir(folder_path):
                continue

            if category_filter and folder_name.lower() != category_filter.lower():
                continue

            # Проверка, есть ли модель для этой категории
            model = self.FOLDER_TO_MODEL.get(folder_name)
            if not model:
                self.stdout.write(self.style.WARNING(f'Skipping unknown folder: {folder_name}'))
                continue

            self.stdout.write(f'Importing {folder_name} into {model.__name__}...')

            # Счетчики
            created_count = 0
            updated_count = 0
            error_count = 0

            # Проходим по всем JSON-файлам в папке категории
            for filename in os.listdir(folder_path):
                if not filename.endswith('.json'):
                    continue

                file_path = os.path.join(folder_path, filename)
                opendb_id = filename[:-5]

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                except Exception as e:
                    self.stderr.write(self.style.ERROR(f'Error reading {file_path}: {e}'))
                    error_count += 1
                    continue

                # Преобразование данных в зависимости от модели
                try:
                    obj_data = self.transform_data(data, model, folder_name)
                except Exception as e:
                    self.stderr.write(self.style.ERROR(f'Error transforming {opendb_id}: {e}'))
                    error_count += 1
                    continue

                # Добавление opendb_id
                obj_data['opendb_id'] = opendb_id

                # Создание или обновление записи
                try:
                    with transaction.atomic():
                        obj, created = model.objects.update_or_create(
                            opendb_id=opendb_id,
                            defaults=obj_data
                        )
                    if created:
                        created_count += 1
                    else:
                        updated_count += 1
                except Exception as e:
                    self.stderr.write(self.style.ERROR(f'Error saving {opendb_id}: {e}'))
                    error_count += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f'{folder_name}: Created {created_count}, Updated {updated_count}, Errors {error_count}'
                )
            )

    def transform_data(self, data, model, category):
        """ Метод преобразования JSON в словарь для модели """
        # Общие поля из metadata
        metadata = data.get('metadata', {})
        result = {
            'name': metadata.get('name', ''),
            'brand': metadata.get('manufacturer', ''),
            'series': metadata.get('series', ''),
            'variant': metadata.get('variant', ''),
            'release_year': metadata.get('releaseYear'),
            'part_numbers_json': metadata.get('part_numbers', []),
        }

        # Заполнение mpn первым part number
        part_numbers = metadata.get('part_numbers', [])
        if part_numbers:
            result['mpn'] = part_numbers[0]

        # Дополнительная обработка в зависимости от категории
        if category == 'CPU':
            self.transform_cpu(data, result)
        elif category == 'GPU':
            self.transform_gpu(data, result)
        elif category == 'Motherboard':
            self.transform_motherboard(data, result)
        elif category == 'RAM':
            self.transform_ram(data, result)
        elif category == 'Storage':
            self.transform_storage(data, result)
        elif category == 'CPUCooler':
            self.transform_cpu_cooler(data, result)
        elif category == 'Case':
            self.transform_case(data, result)
        elif category == 'CaseFan':
            self.transform_case_fan(data, result)
        elif category == 'PowerSupply':
            self.transform_power_supply(data, result)

        # Удаление ключей с None, чтобы не перезаписывать существующие значения
        return {k: v for k, v in result.items() if v is not None}

    def transform_cpu(self, data, result):
        cores = data.get('cores', {})
        result.update({
            'cores_total': cores.get('total'),
            'cores_performance': cores.get('performance'),
            'threads': cores.get('threads'),
        })

        clocks = data.get('clocks', {}).get('performance', {})
        result.update({
            'base_clock': clocks.get('base'),
            'boost_clock': clocks.get('boost'),
        })

        cache = data.get('cache', {})
        result.update({
            'l2_cache': cache.get('l2'),
            'l3_cache': cache.get('l3'),
        })

        specs = data.get('specifications', {})
        integrated_graphics = specs.get('integratedGraphics', {})
        result['integrated_graphics'] = integrated_graphics.get('model', '')

        memory = specs.get('memory', {})
        result.update({
            'max_memory': memory.get('maxSupport'),
            'memory_types': memory.get('types', []),
        })

        result.update({
            'tdp': specs.get('tdp'),
            'ecc_support': specs.get('eccSupport'),
            'includes_cooler': specs.get('includesCooler'),
            'packaging': specs.get('packaging'),
            'lithography': specs.get('lithography'),
            'smt': specs.get('simultaneousMultithreading'),
        })

        result.update({
            'microarchitecture': data.get('microarchitecture'),
            'core_family': data.get('coreFamily'),
            'socket': data.get('socket'),
        })

    def transform_gpu(self, data, result):
        result.update({
            'chipset_manufacturer': data.get('chipset_manufacturer'),
            'chipset': data.get('chipset'),
            'memory': data.get('memory'),
            'memory_type': data.get('memory_type'),
            'core_base_clock': data.get('core_base_clock'),
            'core_boost_clock': data.get('core_boost_clock'),
            'effective_memory_clock': data.get('effective_memory_clock'),
            'memory_bus': data.get('memory_bus'),
            'interface': data.get('interface'),
            'frame_sync': data.get('frame_sync'),
            'length': data.get('length'),
            'tdp': data.get('tdp'),
            'case_expansion_slot_width': data.get('case_expansion_slot_width'),
            'total_slot_width': data.get('total_slot_width'),
            'cooling': data.get('cooling'),
            'color': self.list_to_str(data.get('color', [])),
            'core_count': data.get('core_count'),
            'power_connectors': data.get('power_connectors', {}),
            'video_outputs': data.get('video_outputs', {}),
        })

    def transform_motherboard(self, data, result):
        memory = data.get('memory', {})
        result.update({
            'socket': data.get('socket'),
            'form_factor': data.get('form_factor'),
            'chipset': data.get('chipset'),
            'color': self.list_to_str(data.get('color', [])),
            'memory_max': memory.get('max'),
            'memory_type': memory.get('ram_type'),
            'memory_slots': memory.get('slots'),
            'sata_6_gb_s': data.get('storage_devices', {}).get('sata_6_gb_s'),
            'm2_slots': len(data.get('m2_slots', [])),
            'm2_slots_info': data.get('m2_slots', []),
            'pcie_slots_info': data.get('pcie_slots', []),
            'raid_support': data.get('raid_support'),
            'onboard_ethernet': self.list_to_str(data.get('onboard_ethernet', [])),
            'wireless': '',
            'audio': data.get('audio', {}).get('chipset', ''),
            'back_panel_ports': self.list_to_str(data.get('back_panel_ports', [])),
            'power_connectors': data.get('power_connectors', {}),
            'usb_headers': data.get('usb_headers', {}),
            'fan_headers': data.get('fan_headers', {}),
            'rgb_headers': data.get('rgb_headers', {}),
            'bios_features': data.get('bios_features', {}),
        })

    def transform_ram(self, data, result):
        modules = data.get('modules', {})
        result.update({
            'modules_quantity': modules.get('quantity'),
            'capacity_per_module': modules.get('capacity_gb'),
            'total_capacity': data.get('capacity'),
            'speed': data.get('speed'),
            'ram_type': data.get('ram_type'),
            'form_factor': data.get('form_factor'),
            'color': self.list_to_str(data.get('color', [])),
            'cas_latency': data.get('cas_latency'),
            'timings': data.get('timings'),
            'voltage': data.get('voltage'),
            'ecc': data.get('ecc'),
            'registered': data.get('registered'),
            'heat_spreader': data.get('heat_spreader'),
            'rgb': data.get('rgb'),
            'profile_support': data.get('profile_support', []),
        })

    def transform_storage(self, data, result):
        result.update({
            'capacity': data.get('capacity'),
            'type': data.get('type'),
            'form_factor': data.get('form_factor'),
            'interface': data.get('interface'),
            'nvme': data.get('nvme'),
            'rpm': data.get('rpm'),
        })

    def transform_cpu_cooler(self, data, result):
        result.update({
            'min_fan_rpm': data.get('min_fan_rpm'),
            'max_fan_rpm': data.get('max_fan_rpm'),
            'min_noise_level': data.get('min_noise_level'),
            'max_noise_level': data.get('max_noise_level'),
            'color': self.list_to_str(data.get('color', [])),
            'height': data.get('height'),
            'cpu_sockets': self.list_to_str(data.get('cpu_sockets', [])),
            'water_cooled': data.get('water_cooled'),
            'radiator_size': data.get('radiator_size'),
            'fanless': data.get('fanless'),
            'fan_size': data.get('fan_size'),
            'fan_quantity': data.get('fan_quantity'),
        })

    def transform_case(self, data, result):
        result.update({
            'case_type': data.get('form_factor'),
            'supported_motherboard_form_factors': self.list_to_str(data.get('supported_motherboard_form_factors', [])),
            'color': self.list_to_str(data.get('color', [])),
            'power_supply': data.get('power_supply'),
            'side_panel': data.get('side_panel'),
            'has_transparent_side_panel': data.get('has_transparent_side_panel'),
            'front_panel_usb': data.get('front_panel_usb'),
            'max_video_card_length': data.get('max_video_card_length'),
            'max_cpu_cooler_height': data.get('max_cpu_cooler_height'),
            'internal_3_5_bays': data.get('internal_3_5_bays'),
            'internal_2_5_bays': data.get('internal_2_5_bays'),
            'expansion_slots': data.get('expansion_slots'),
            'dimensions': data.get('dimensions'),
            'volume': data.get('volume'),
            'weight': data.get('weight'),
            'supported_power_supply_form_factors': self.list_to_str(data.get('supported_power_supply_form_factors', [])),
        })

    def transform_case_fan(self, data, result):
        result.update({
            'size': data.get('size'),
            'color': self.list_to_str(data.get('color', [])),
            'quantity': data.get('quantity'),
            'min_airflow': data.get('min_airflow'),
            'max_airflow': data.get('max_airflow'),
            'min_noise_level': data.get('min_noise_level'),
            'max_noise_level': data.get('max_noise_level'),
            'pwm': data.get('pwm'),
            'led': data.get('led'),
            'connector': data.get('connector'),
            'controller': data.get('controller'),
            'static_pressure': data.get('static_pressure'),
            'flow_direction': data.get('flow_direction'),
        })

    def transform_power_supply(self, data, result):
        result.update({
            'wattage': data.get('wattage'),
            'form_factor': data.get('form_factor'),
            'efficiency_rating': data.get('efficiency_rating'),
            'modular': data.get('modular'),
            'color': self.list_to_str(data.get('color', [])),
            'length': data.get('length'),
            'fanless': data.get('fanless'),
            'connectors': data.get('connectors', {}),
        })

    def list_to_str(self, lst):
        """ Преобразование списка в строку через запятую """
        if not lst:
            return ''
        return ', '.join(str(x) for x in lst if x)