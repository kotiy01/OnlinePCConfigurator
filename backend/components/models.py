from django.db import models
from django.contrib.auth.models import User

# Commit с обновленными данными: [skip ci] Automated opendb sync - 2026-03-15T17:53:05.041Z

class BaseComponent(models.Model):
    """Абстрактная модель для всех комплектующих"""
    opendb_id = models.CharField(max_length=36, unique=True, verbose_name="OpenDB UUID")
    name = models.CharField(max_length=255, verbose_name="Название")
    brand = models.CharField(max_length=100, blank=True, verbose_name="Бренд")
    normalized_name = models.CharField(max_length=255, db_index=True, blank=True, verbose_name="Нормализованное название")
    mpn = models.CharField(max_length=100, blank=True, null=True, verbose_name="Part Number (MPN)")
    is_verified = models.BooleanField(default=True, verbose_name="Из эталонного источника")

    # Дополнительные мета-поля (необязательные)
    series = models.CharField(max_length=100, blank=True, verbose_name="Серия")
    variant = models.CharField(max_length=100, blank=True, verbose_name="Вариант/модификация")
    release_year = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Год выпуска")

    # Для хранения списка part numbers
    part_numbers_json = models.JSONField(default=list, blank=True, verbose_name="Список Part Numbers")

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Автоматическое заполнение normalized_name при сохранении
        if not self.normalized_name:
            self.normalized_name = self._normalize_name(self.name)
        super().save(*args, **kwargs)

    def _normalize_name(self, name):
        """Простая нормализация имени для поиска"""
        if not name:
            return ""
        name = name.lower()
        # Список стоп-слов
        stop_words = ['cpu', 'processor', 'intel', 'amd', 'ryzen', 'core', 'series', 'black', 'gray']
        for word in stop_words:
            name = name.replace(word, '')
        # Замена разделителей на дефис
        import re
        name = re.sub(r'[\s\-_]+', '-', name)
        return name.strip('-')


class CPU(BaseComponent):
    # Ядра и потоки
    cores_total = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Всего ядер")
    cores_performance = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Производительных ядер")
    threads = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Потоков")

    # Частоты
    base_clock = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Базовая частота (ГГц)")
    boost_clock = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Макс. частота (ГГц)")

    # Кэш
    l2_cache = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Кэш L2 (МБ)")
    l3_cache = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Кэш L3 (МБ)")

    # Спецификации
    integrated_graphics = models.CharField(max_length=100, blank=True, verbose_name="Встроенная графика")
    max_memory = models.PositiveIntegerField(null=True, blank=True, verbose_name="Макс. память (ГБ)")
    tdp = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="TDP (Вт)")
    ecc_support = models.BooleanField(null=True, blank=True, verbose_name="Поддержка ECC")
    includes_cooler = models.BooleanField(null=True, blank=True, verbose_name="В комплекте кулер")
    packaging = models.CharField(max_length=50, blank=True, verbose_name="Тип упаковки")
    lithography = models.CharField(max_length=20, blank=True, verbose_name="Техпроцесс")
    smt = models.BooleanField(null=True, blank=True, verbose_name="Одновременная многопоточность")

    # Архитектура и сокет
    microarchitecture = models.CharField(max_length=100, blank=True, verbose_name="Микроархитектура")
    core_family = models.CharField(max_length=100, blank=True, verbose_name="Семейство ядер")
    socket = models.CharField(max_length=50, blank=True, verbose_name="Сокет")

    # Дополнительные данные
    memory_types = models.JSONField(default=list, blank=True, verbose_name="Поддерживаемые типы памяти")

    class Meta:
        verbose_name = "Процессор"
        verbose_name_plural = "Процессоры"


class CPUCooler(BaseComponent):
    min_fan_rpm = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Мин. обороты вентилятора")
    max_fan_rpm = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Макс. обороты вентилятора")
    min_noise_level = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, verbose_name="Мин. уровень шума (Дб)")
    max_noise_level = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, verbose_name="Макс. уровень шума (Дб)")
    color = models.CharField(max_length=100, blank=True, verbose_name="Цвет")
    height = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Высота (мм)")

    # Список сокетов
    cpu_sockets = models.TextField(blank=True, verbose_name="Совместимые сокеты")
    water_cooled = models.BooleanField(default=False, verbose_name="Водяное охлаждение")
    radiator_size = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Размер радиатора (мм)")
    fanless = models.BooleanField(default=False, verbose_name="Пассивное охлаждение")
    fan_size = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Размер вентилятора (мм)")
    fan_quantity = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Количество вентиляторов")

    class Meta:
        verbose_name = "Кулер для процессора"
        verbose_name_plural = "Кулеры для процессора"


class CaseFan(BaseComponent):
    size = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Размер (мм)")
    color = models.CharField(max_length=100, blank=True, verbose_name="Цвет")
    quantity = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Количество в упаковке")
    min_airflow = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, verbose_name="Мин. воздушный поток (CFM)")
    max_airflow = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, verbose_name="Макс. воздушный поток (CFM)")
    min_noise_level = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, verbose_name="Мин. уровень шума (Дб)")
    max_noise_level = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, verbose_name="Макс. уровень шума (Дб)")
    pwm = models.BooleanField(null=True, blank=True, verbose_name="PWM")
    led = models.CharField(max_length=50, blank=True, verbose_name="Подсветка")
    connector = models.CharField(max_length=20, blank=True, verbose_name="Разъем")
    controller = models.CharField(max_length=50, blank=True, verbose_name="Контроллер")
    static_pressure = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name="Статическое давление")
    flow_direction = models.CharField(max_length=20, blank=True, verbose_name="Направление потока")

    class Meta:
        verbose_name = "Корпусной вентилятор"
        verbose_name_plural = "Корпусные вентиляторы"


class GPU(BaseComponent):
    chipset_manufacturer = models.CharField(max_length=50, blank=True, verbose_name="Производитель чипсета")
    chipset = models.CharField(max_length=100, blank=True, verbose_name="Чипсет")
    memory = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Память (ГБ)")
    memory_type = models.CharField(max_length=20, blank=True, verbose_name="Тип памяти")
    core_base_clock = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Базовая частота ядра (МГц)")
    core_boost_clock = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Boost частота (МГц)")
    effective_memory_clock = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Эффективная частота памяти (МГц)")
    memory_bus = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Шина памяти (бит)")
    interface = models.CharField(max_length=30, blank=True, verbose_name="Интерфейс")
    frame_sync = models.CharField(max_length=50, blank=True, verbose_name="Технология синхронизации")
    length = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Длина (мм)")
    tdp = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="TDP (Вт)")
    case_expansion_slot_width = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Занимает слотов расширения")
    total_slot_width = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Общая ширина (слоты)")
    cooling = models.CharField(max_length=100, blank=True, verbose_name="Система охлаждения")
    color = models.CharField(max_length=100, blank=True, verbose_name="Цвет(а)")
    core_count = models.PositiveIntegerField(null=True, blank=True, verbose_name="Количество ядер CUDA / потоковых процессоров")

    # Разъемы питания
    power_connectors = models.JSONField(default=dict, blank=True, verbose_name="Разъемы питания")
    # Видеовыходы
    video_outputs = models.JSONField(default=dict, blank=True, verbose_name="Видеовыходы")

    class Meta:
        verbose_name = "Видеокарта"
        verbose_name_plural = "Видеокарты"


class Motherboard(BaseComponent):
    socket = models.CharField(max_length=50, blank=True, verbose_name="Сокет")
    form_factor = models.CharField(max_length=50, blank=True, verbose_name="Форм-фактор")
    chipset = models.CharField(max_length=100, blank=True, verbose_name="Чипсет")
    color = models.CharField(max_length=100, blank=True, verbose_name="Цвет(а)")

    # Память
    memory_max = models.PositiveIntegerField(null=True, blank=True, verbose_name="Макс. объем памяти (ГБ)")
    memory_type = models.CharField(max_length=20, blank=True, verbose_name="Тип памяти")
    memory_slots = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Слотов памяти")

    # Хранилища
    sata_6_gb_s = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Порты SATA")
    m2_slots = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Слотов M.2")
    m2_slots_info = models.JSONField(default=list, blank=True, verbose_name="Детали M.2 слотов")
    pcie_slots_info = models.JSONField(default=list, blank=True, verbose_name="Детали PCIe слотов")
    raid_support = models.BooleanField(default=False, verbose_name="Поддержка RAID")

    # Сеть и аудио
    onboard_ethernet = models.TextField(blank=True, verbose_name="Встроенный Ethernet")
    wireless = models.CharField(max_length=100, blank=True, verbose_name="Wi-Fi")
    audio = models.CharField(max_length=100, blank=True, verbose_name="Аудиочип")

    # Порты на задней панели
    back_panel_ports = models.TextField(blank=True, verbose_name="Порты задней панели")

    # Разъемы питания
    power_connectors = models.JSONField(default=dict, blank=True, verbose_name="Разъемы питания")

    # Заголовки
    usb_headers = models.JSONField(default=dict, blank=True, verbose_name="USB заголовки")
    fan_headers = models.JSONField(default=dict, blank=True, verbose_name="Заголовки вентиляторов")
    rgb_headers = models.JSONField(default=dict, blank=True, verbose_name="RGB заголовки")

    # BIOS особенности
    bios_features = models.JSONField(default=dict, blank=True, verbose_name="Особенности BIOS")

    class Meta:
        verbose_name = "Материнская плата"
        verbose_name_plural = "Материнские платы"


class RAM(BaseComponent):
    modules_quantity = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Количество модулей в комплекте")
    capacity_per_module = models.PositiveIntegerField(null=True, blank=True, verbose_name="Объем одного модуля (ГБ)")
    total_capacity = models.PositiveIntegerField(null=True, blank=True, verbose_name="Суммарный объем (ГБ)")

    speed = models.PositiveIntegerField(null=True, blank=True, verbose_name="Частота (МГц)")
    ram_type = models.CharField(max_length=20, blank=True, verbose_name="Тип памяти")
    form_factor = models.CharField(max_length=30, blank=True, verbose_name="Форм-фактор")
    color = models.CharField(max_length=100, blank=True, verbose_name="Цвет")

    cas_latency = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="CAS Latency")
    timings = models.CharField(max_length=50, blank=True, verbose_name="Тайминги")
    voltage = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name="Напряжение (В)")
    ecc = models.CharField(max_length=20, blank=True, verbose_name="ECC")
    registered = models.CharField(max_length=20, blank=True, verbose_name="Registered/Buffered")
    heat_spreader = models.BooleanField(null=True, blank=True, verbose_name="Теплораспределитель")
    rgb = models.BooleanField(null=True, blank=True, verbose_name="Подсветка")
    profile_support = models.JSONField(default=list, blank=True, verbose_name="Поддерживаемые профили (XMP/EXPO)")

    class Meta:
        verbose_name = "Оперативная память"
        verbose_name_plural = "Оперативная память"


class Storage(BaseComponent):
    capacity = models.PositiveIntegerField(null=True, blank=True, verbose_name="Объем (ГБ)")
    type = models.CharField(max_length=20, blank=True, verbose_name="Тип (SSD/HDD)")
    form_factor = models.CharField(max_length=50, blank=True, verbose_name="Форм-фактор")
    interface = models.CharField(max_length=50, blank=True, verbose_name="Интерфейс")
    nvme = models.BooleanField(null=True, blank=True, verbose_name="NVMe")
    # RPM для HDD
    rpm = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Скорость вращения (RPM)")

    class Meta:
        verbose_name = "Накопитель"
        verbose_name_plural = "Накопители"


class Case(BaseComponent):
    case_type = models.CharField(max_length=50, blank=True, verbose_name="Тип корпуса")
    supported_motherboard_form_factors = models.TextField(blank=True, verbose_name="Поддерживаемые форм-факторы материнских плат")
    color = models.CharField(max_length=100, blank=True, verbose_name="Цвет")
    power_supply = models.CharField(max_length=50, blank=True, verbose_name="Блок питания (в комплекте)")
    side_panel = models.CharField(max_length=50, blank=True, verbose_name="Боковая панель")
    has_transparent_side_panel = models.BooleanField(null=True, blank=True, verbose_name="Прозрачная панель")
    front_panel_usb = models.TextField(blank=True, verbose_name="USB на передней панели")
    max_video_card_length = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Макс. длина видеокарты (мм)")
    max_cpu_cooler_height = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Макс. высота кулера CPU (мм)")
    internal_3_5_bays = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Внутренних отсеков 3.5 дюйма")
    internal_2_5_bays = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Внутренних отсеков 2.5 дюйма")
    expansion_slots = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Слотов расширения")
    dimensions = models.CharField(max_length=100, blank=True, verbose_name="Габариты")
    volume = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name="Объем (литры)")
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Вес (кг)")

    # Списки поддерживаемых форм-факторов БП
    supported_power_supply_form_factors = models.TextField(blank=True, verbose_name="Поддерживаемые форм-факторы БП")

    class Meta:
        verbose_name = "Корпус"
        verbose_name_plural = "Корпуса"


class PowerSupply(BaseComponent):
    wattage = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Мощность (Вт)")
    form_factor = models.CharField(max_length=20, blank=True, verbose_name="Форм-фактор")
    efficiency_rating = models.CharField(max_length=30, blank=True, verbose_name="Сертификат эффективности")
    modular = models.CharField(max_length=30, blank=True, verbose_name="Модульность")
    color = models.CharField(max_length=100, blank=True, verbose_name="Цвет")
    length = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Длина (мм)")
    fanless = models.BooleanField(default=False, verbose_name="Пассивное охлаждение")

    # Разъемы
    connectors = models.JSONField(default=dict, blank=True, verbose_name="Разъемы")

    class Meta:
        verbose_name = "Блок питания"
        verbose_name_plural = "Блоки питания"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Профиль {self.user.username}"