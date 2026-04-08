import math
from decimal import Decimal

def _safe_float(value):
    """ Преобразование Decimal или число в float """
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
    
def check_cpu_motherboard(cpu, motherboard):
    """ Проверка совместимости процессора и материнской платы """
    if not cpu or not motherboard:
        return True, [] # если один из компонентов не выбран, считается совместимым

    errors = []
    warnings = []

    # Сокет
    if cpu.socket and motherboard.socket:
        if cpu.socket.lower() != motherboard.socket.lower():
            errors.append(f"Сокет процессора ({cpu.socket}) не поддерживается материнской платой ({motherboard.socket}).")
    else:
        warnings.append("Не указан сокет у одного из компонентов, проверьте совместимость вручную.")

    return not errors, errors + warnings

def check_cpu_ram(cpu, ram):
    """ Проверка совместимости процессора и оперативной памяти """
    if not cpu or not ram:
        return True, []

    errors = []
    warnings = []

    # Тип памяти
    if cpu.memory_types and ram.ram_type:
        if ram.ram_type.lower() not in [t.lower() for t in cpu.memory_types]:
            errors.append(f"Процессор не поддерживает тип памяти {ram.ram_type}.")

    # Частота
    if cpu.max_memory and ram.speed and cpu.max_memory < ram.speed:
        warnings.append(f"Процессор поддерживает частоту памяти до {cpu.max_memory} МГц, выбрана {ram.speed} МГц. Возможно снижение частоты.")
    if cpu.base_clock and ram.speed:
        # Если частота RAM сильно выше базовой, предупреждение
        if ram.speed > 2 * cpu.base_clock * 1000:
            warnings.append(f"Высокая частота RAM ({ram.speed} МГц) может быть недостижима без разгона.")

    # Объем
    if cpu.max_memory and ram.total_capacity:
        if ram.total_capacity > cpu.max_memory:
            errors.append(f"Суммарный объем памяти ({ram.total_capacity} ГБ) превышает максимальный для процессора ({cpu.max_memory} ГБ).")

    return not errors, errors + warnings

def check_motherboard_ram(motherboard, ram):
    """ Проверка совместимости материнской платы и оперативной памяти """
    if not motherboard or not ram:
        return True, []

    errors = []
    warnings = []

    # Тип памяти
    if motherboard.memory_type and ram.ram_type:
        if motherboard.memory_type.lower() != ram.ram_type.lower():
            errors.append(f"Материнская плата поддерживает {motherboard.memory_type}, выбрана {ram.ram_type}.")

    # Количество слотов
    if motherboard.memory_slots and ram.modules_quantity:
        if ram.modules_quantity > motherboard.memory_slots:
            errors.append(f"Материнская плата имеет {motherboard.memory_slots} слота(ов) памяти, выбрано {ram.modules_quantity} модулей.")
        # Предупреждение о несимметричных модулях
        if ram.modules_quantity == 1 and motherboard.memory_slots >= 2:
            warnings.append("Используйте два модуля для двухканального режима.")

    # Объем
    if motherboard.memory_max and ram.total_capacity:
        if ram.total_capacity > motherboard.memory_max:
            errors.append(f"Максимальный объем памяти материнской платы {motherboard.memory_max} ГБ, выбрано {ram.total_capacity} ГБ.")

    # Частота
    if ram.speed and motherboard.memory_type:
        if ram.speed > 4000 and motherboard.memory_type == 'DDR4':
            warnings.append("Для работы на частоте выше 4000 МГц может потребоваться ручная настройка XMP.")
        if ram.speed > 6000 and motherboard.memory_type == 'DDR5':
            warnings.append("Высокая частота памяти может потребовать включения EXPO/XMP в BIOS.")

    return not errors, errors + warnings

def check_cpu_cooler(cpu, cooler):
    """ Проверка совместимости процессора и кулера """
    if not cpu or not cooler:
        return True, []

    errors = []
    warnings = []

    # TDP
    # if cpu.tdp and cooler.tdp:
    #     if cooler.tdp < cpu.tdp:
    #         errors.append(f"Максимальное TDP кулера ({cooler.tdp} Вт) меньше TDP процессора ({cpu.tdp} Вт).")
    # elif cpu.tdp and not cooler.tdp:
    #     warnings.append("Для кулера не указан TDP, проверьте достаточность охлаждения вручную.")

    # Сокет
    if cpu.socket and cooler.cpu_sockets:
        supported_sockets = [s.strip().lower() for s in cooler.cpu_sockets.split(',')]
        if cpu.socket.lower() not in supported_sockets:
            errors.append(f"Кулер не поддерживает сокет {cpu.socket}. Поддерживаемые: {cooler.cpu_sockets}.")

    return not errors, errors + warnings

def check_motherboard_case(motherboard, case):
    """ Проверка совместимости материнской платы и корпуса """
    if not motherboard or not case:
        return True, []

    errors = []
    warnings = []

    if motherboard.form_factor and case.supported_motherboard_form_factors:
        supported = [ff.strip().lower() for ff in case.supported_motherboard_form_factors.split(',')]
        if motherboard.form_factor.lower() not in supported:
            errors.append(f"Корпус не поддерживает форм-фактор {motherboard.form_factor}. Поддерживаемые: {case.supported_motherboard_form_factors}.")
    else:
        warnings.append("Не указаны форм-факторы корпуса или материнской платы, проверьте совместимость вручную.")

    return not errors, errors + warnings

# def check_gpu_psu(gpu, psu, total_power):
#     """
#     Проверка видеокарты и блока питания.
#     total_power — суммарное энергопотребление сборки (можно рассчитать отдельно).
#     Учитывает мощность, разъёмы питания.
#     """
#     if not gpu or not psu:
#         return True, []

#     errors = []
#     warnings = []

#     # Разъемы питания
#     if gpu.power_connectors and psu.connectors:
#         # gpu.power_connectors {"pcie_8_pin": 2}
#         # psu.connectors {"pcie_6_plus_2_pin": 2}
#         required_8pin = gpu.power_connectors.get('pcie_8_pin', 0)
#         required_6pin = gpu.power_connectors.get('pcie_6_pin', 0)
#         available = psu.connectors.get('pcie_6_plus_2_pin', 0) # 8-pin
#         if required_8pin > available:
#             errors.append(f"Видеокарте требуется {required_8pin} 8-pin разъемов, в БП только {available}.")
#     else:
#         warnings.append("Не удалось проверить разъемы питания, убедитесь, что БП имеет нужные коннекторы.")

#     return not errors, errors + warnings

def check_gpu_case(gpu, case):
    """ Проверка совместимости видеокарты и корпуса по длине """
    if not gpu or not case:
        return True, []

    errors = []
    warnings = []

    if gpu.length and case.max_video_card_length:
        if gpu.length > case.max_video_card_length:
            errors.append(f"Длина видеокарты ({gpu.length} мм) превышает максимально допустимую для корпуса ({case.max_video_card_length} мм).")
    elif gpu.length and not case.max_video_card_length:
        warnings.append("Для корпуса не указана максимальная длина видеокарты, проверьте совместимость вручную.")

    # Ширина/слоты
    if gpu.case_expansion_slot_width and case.expansion_slots:
        if gpu.case_expansion_slot_width > case.expansion_slots:
            warnings.append(f"Видеокарта занимает {gpu.case_expansion_slot_width} слота, в корпусе {case.expansion_slots} свободных слотов. Возможны проблемы.")

    return not errors, errors + warnings

def check_psu_case(psu, case):
    """ Проверка совместимости блока питания и корпуса по длине и форм-фактору """
    if not psu or not case:
        return True, []

    errors = []
    warnings = []

    # Форм-фактор БП
    if psu.form_factor and case.supported_power_supply_form_factors:
        supported = [ff.strip().lower() for ff in case.supported_power_supply_form_factors.split(',')]
        if psu.form_factor.lower() not in supported:
            errors.append(f"Корпус не поддерживает форм-фактор БП {psu.form_factor}. Поддерживаемые: {case.supported_power_supply_form_factors}.")

    # Длина
    # if psu.length and case.max_psu_length:
    #     if psu.length > case.max_psu_length:
    #         errors.append(f"Длина блока питания ({psu.length} мм) превышает максимальную для корпуса ({case.max_psu_length} мм).")

    return not errors, errors + warnings

def check_storage_motherboard(storage, motherboard):
    """ Проверка накопителя и материнской платы (интерфейс, количество портов) """
    if not storage or not motherboard:
        return True, []

    errors = []
    warnings = []

    # SATA
    if storage.interface == 'SATA' and motherboard.sata_6_gb_s is not None:
        if motherboard.sata_6_gb_s <= 0:
            errors.append("На материнской плате нет свободных портов SATA.")
        warnings.append("Проверьте наличие свободного порта SATA.")

    # M.2 NVMe
    if storage.interface in ['M.2 PCIe', 'M.2 NVMe']:
        if motherboard.m2_slots is not None and motherboard.m2_slots <= 0:
            errors.append("На материнской плате нет слотов M.2.")
        else:
            warnings.append("Проверьте наличие свободного слота M.2.")

    return not errors, errors + warnings

def calculate_total_power(build):
    """ Рассчет суммарного энергопотребления сборки в Вт """
    total = 0
    for comp in build.values():
        if hasattr(comp, 'tdp') and comp.tdp:
            total += comp.tdp
        # Добавить другие компоненты, потребляющие энергию (допустим, по 5 Вт на модуль RAM)
    # Запас 50-100 Вт
    return total + 50

def check_full_compatibility(build):
    """ Проверка всей сборки """
    messages = []
    cpu = build.get('cpu')
    motherboard = build.get('motherboard')
    ram = build.get('ram')
    gpu = build.get('gpu')
    psu = build.get('psu')
    case = build.get('case')
    cooler = build.get('cooler')
    storage = build.get('storage')

    # Проверки по всем правилам
    checks = [
        check_cpu_motherboard(cpu, motherboard),
        check_cpu_ram(cpu, ram),
        check_motherboard_ram(motherboard, ram),
        check_cpu_cooler(cpu, cooler),
        check_motherboard_case(motherboard, case),
        # check_gpu_psu(gpu, psu if gpu and psu else 0),
        check_gpu_case(gpu, case),
        # check_psu_case(psu, case),
        check_storage_motherboard(storage, motherboard),
    ]

    all_compatible = True
    for compatible, msgs in checks:
        if not compatible:
            all_compatible = False
        messages.extend(msgs)

    return all_compatible, messages