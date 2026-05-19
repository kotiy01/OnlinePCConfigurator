from django.test import TestCase
from compatibility.rules import (
    check_cpu_motherboard,
    check_cpu_ram,
    check_motherboard_ram,
    check_cpu_cooler,
    check_motherboard_case,
    check_gpu_case,
    check_psu_case,
    check_storage_motherboard,
)


class TestCPUMotherboardCompatibility(TestCase):
    def test_compatible_sockets(self):
        cpu = type('CPU', (), {'socket': 'AM5'})()
        motherboard = type('Motherboard', (), {'socket': 'AM5'})()
        compatible, messages = check_cpu_motherboard(cpu, motherboard)
        self.assertTrue(compatible)
        self.assertEqual(len(messages), 0)

    def test_incompatible_sockets(self):
        cpu = type('CPU', (), {'socket': 'AM5'})()
        motherboard = type('Motherboard', (), {'socket': 'LGA1700'})()
        compatible, messages = check_cpu_motherboard(cpu, motherboard)
        self.assertFalse(compatible)
        self.assertIn('не поддерживается', messages[0])

    def test_missing_socket_warning(self):
        cpu = type('CPU', (), {'socket': 'AM5'})()
        motherboard = type('Motherboard', (), {'socket': None})()
        compatible, messages = check_cpu_motherboard(cpu, motherboard)
        self.assertTrue(compatible)
        self.assertIn('Не указан сокет', messages[0])

    def test_none_components(self):
        compatible, messages = check_cpu_motherboard(None, None)
        self.assertTrue(compatible)
        self.assertEqual(messages, [])


class TestCPURAMCompatibility(TestCase):
    def test_compatible_memory_type(self):
        cpu = type('CPU', (), {'memory_types': ['DDR5'], 'max_memory': None, 'base_clock': 4.0})()
        ram = type('RAM', (), {'ram_type': 'DDR5', 'speed': 5200, 'total_capacity': 32})()
        compatible, messages = check_cpu_ram(cpu, ram)
        self.assertTrue(compatible)
        self.assertEqual(len(messages), 0)

    def test_incompatible_memory_type(self):
        cpu = type('CPU', (), {'memory_types': ['DDR5'], 'max_memory': None, 'base_clock': 4.0})()
        ram = type('RAM', (), {'ram_type': 'DDR4', 'speed': 3200, 'total_capacity': 32})()
        compatible, messages = check_cpu_ram(cpu, ram)
        self.assertFalse(compatible)
        self.assertIn('не поддерживает тип памяти', messages[0])

    def test_memory_capacity_exceeds_max(self):
        cpu = type('CPU', (), {'memory_types': ['DDR5'], 'max_memory': 64, 'base_clock': 4.0})()
        ram = type('RAM', (), {'ram_type': 'DDR5', 'speed': 5200, 'total_capacity': 128})()
        compatible, messages = check_cpu_ram(cpu, ram)
        self.assertFalse(compatible)
        self.assertIn('превышает максимальный', messages[0])


class TestMotherboardRAMCompatibility(TestCase):
    def test_compatible_memory_type(self):
        mb = type('Motherboard', (), {'memory_type': 'DDR5', 'memory_slots': 4, 'memory_max': 128})()
        ram = type('RAM', (), {'ram_type': 'DDR5', 'modules_quantity': 2, 'total_capacity': 32, 'speed': 5600})()
        compatible, messages = check_motherboard_ram(mb, ram)
        self.assertTrue(compatible)
        self.assertEqual(len(messages), 0)

    def test_incompatible_memory_type(self):
        mb = type('Motherboard', (), {'memory_type': 'DDR5', 'memory_slots': 4, 'memory_max': 128})()
        ram = type('RAM', (), {'ram_type': 'DDR4', 'modules_quantity': 2, 'total_capacity': 32, 'speed': 3200})()
        compatible, messages = check_motherboard_ram(mb, ram)
        self.assertFalse(compatible)
        self.assertIn('поддерживает', messages[0])

    def test_exceeds_slots(self):
        mb = type('Motherboard', (), {'memory_type': 'DDR5', 'memory_slots': 2, 'memory_max': 64})()
        ram = type('RAM', (), {'ram_type': 'DDR5', 'modules_quantity': 4, 'total_capacity': 64, 'speed': 5600})()
        compatible, messages = check_motherboard_ram(mb, ram)
        self.assertFalse(compatible)
        self.assertIn('слота(ов)', messages[0])

    def test_single_channel_warning(self):
        mb = type('Motherboard', (), {'memory_type': 'DDR5', 'memory_slots': 4, 'memory_max': 128})()
        ram = type('RAM', (), {'ram_type': 'DDR5', 'modules_quantity': 1, 'total_capacity': 32, 'speed': 5600})()
        compatible, messages = check_motherboard_ram(mb, ram)
        self.assertTrue(compatible)
        self.assertIn('двухканального режима', messages[0])

    def test_ddr4_high_frequency_warning(self):
        mb = type('Motherboard', (), {'memory_type': 'DDR4', 'memory_slots': 4, 'memory_max': 128})()
        ram = type('RAM', (), {'ram_type': 'DDR4', 'modules_quantity': 2, 'total_capacity': 32, 'speed': 4400})()
        compatible, messages = check_motherboard_ram(mb, ram)
        self.assertTrue(compatible)
        self.assertIn('ручная настройка XMP', messages[0])


class TestCPUCoolerCompatibility(TestCase):
    def test_compatible_socket(self):
        cpu = type('CPU', (), {'socket': 'AM5'})()
        cooler = type('Cooler', (), {'cpu_sockets': 'AM4, AM5, LGA1700'})()
        compatible, messages = check_cpu_cooler(cpu, cooler)
        self.assertTrue(compatible)
        self.assertEqual(len(messages), 0)

    def test_incompatible_socket(self):
        cpu = type('CPU', (), {'socket': 'LGA1700'})()
        cooler = type('Cooler', (), {'cpu_sockets': 'AM4, AM5'})()
        compatible, messages = check_cpu_cooler(cpu, cooler)
        self.assertFalse(compatible)
        self.assertIn('не поддерживает сокет', messages[0])


class TestMotherboardCaseCompatibility(TestCase):
    def test_compatible_form_factor(self):
        mb = type('Motherboard', (), {'form_factor': 'ATX'})()
        case = type('Case', (), {'supported_motherboard_form_factors': 'ATX, Micro ATX, Mini ITX'})()
        compatible, messages = check_motherboard_case(mb, case)
        self.assertTrue(compatible)
        self.assertEqual(len(messages), 0)

    def test_incompatible_form_factor(self):
        mb = type('Motherboard', (), {'form_factor': 'E-ATX'})()
        case = type('Case', (), {'supported_motherboard_form_factors': 'ATX, Micro ATX'})()
        compatible, messages = check_motherboard_case(mb, case)
        self.assertFalse(compatible)
        self.assertIn('не поддерживает форм-фактор', messages[0])

    def test_missing_form_factor_warning(self):
        mb = type('Motherboard', (), {'form_factor': 'ATX'})()
        case = type('Case', (), {'supported_motherboard_form_factors': None})()
        compatible, messages = check_motherboard_case(mb, case)
        self.assertTrue(compatible)
        self.assertIn('Не указаны форм-факторы', messages[0])


class TestGPUCaseCompatibility(TestCase):
    def test_length_within_limit(self):
        gpu = type('GPU', (), {'length': 280, 'case_expansion_slot_width': 2})()
        case = type('Case', (), {'max_video_card_length': 350, 'expansion_slots': 7})()
        compatible, messages = check_gpu_case(gpu, case)
        self.assertTrue(compatible)
        self.assertEqual(len(messages), 0)

    def test_length_exceeds_limit(self):
        gpu = type('GPU', (), {'length': 360, 'case_expansion_slot_width': 2})()
        case = type('Case', (), {'max_video_card_length': 320, 'expansion_slots': 7})()
        compatible, messages = check_gpu_case(gpu, case)
        self.assertFalse(compatible)
        self.assertIn('превышает максимально допустимую', messages[0])

    def test_slot_width_warning(self):
        gpu = type('GPU', (), {'length': 280, 'case_expansion_slot_width': 4})()
        case = type('Case', (), {'max_video_card_length': 350, 'expansion_slots': 3})()
        compatible, messages = check_gpu_case(gpu, case)
        self.assertTrue(compatible)
        self.assertIn('занимает 4 слота', messages[0])


class TestPSUCaseCompatibility(TestCase):
    def test_compatible_form_factor(self):
        psu = type('PSU', (), {'form_factor': 'ATX'})()
        case = type('Case', (), {'supported_power_supply_form_factors': 'ATX, SFX'})()
        compatible, messages = check_psu_case(psu, case)
        self.assertTrue(compatible)
        self.assertEqual(len(messages), 0)

    def test_incompatible_form_factor(self):
        psu = type('PSU', (), {'form_factor': 'SFX-L'})()
        case = type('Case', (), {'supported_power_supply_form_factors': 'ATX, SFX'})()
        compatible, messages = check_psu_case(psu, case)
        self.assertFalse(compatible)
        self.assertIn('не поддерживает форм-фактор БП', messages[0])


class TestStorageMotherboardCompatibility(TestCase):
    def test_sata_with_available_ports(self):
        storage = type('Storage', (), {'interface': 'SATA'})()
        mb = type('Motherboard', (), {'sata_6_gb_s': 4, 'm2_slots': 2})()
        compatible, messages = check_storage_motherboard(storage, mb)
        self.assertTrue(compatible)
        self.assertIn('Проверьте наличие свободного порта SATA', messages[0])

    def test_sata_no_ports_error(self):
        storage = type('Storage', (), {'interface': 'SATA'})()
        mb = type('Motherboard', (), {'sata_6_gb_s': 0, 'm2_slots': 2})()
        compatible, messages = check_storage_motherboard(storage, mb)
        self.assertFalse(compatible)
        self.assertIn('нет свободных портов SATA', messages[0])

    def test_nvme_with_available_slots(self):
        storage = type('Storage', (), {'interface': 'M.2 NVMe'})()
        mb = type('Motherboard', (), {'sata_6_gb_s': 4, 'm2_slots': 2})()
        compatible, messages = check_storage_motherboard(storage, mb)
        self.assertTrue(compatible)
        self.assertIn('Проверьте наличие свободного слота M.2', messages[0])

    def test_nvme_no_slots_error(self):
        storage = type('Storage', (), {'interface': 'M.2 NVMe'})()
        mb = type('Motherboard', (), {'sata_6_gb_s': 4, 'm2_slots': 0})()
        compatible, messages = check_storage_motherboard(storage, mb)
        self.assertFalse(compatible)
        self.assertIn('нет слотов M.2', messages[0])