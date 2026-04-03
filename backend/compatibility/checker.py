from .rules import check_full_compatibility#, calculate_total_power

def check_compatibility(build):
    """ Загружает объекты из БД и возвращает результат """
    from components.models import CPU, Motherboard, RAM, GPU, PowerSupply, Case, CPUCooler, Storage

    # Маппинг категорий на модели
    model_map = {
        'cpu': CPU,
        'motherboard': Motherboard,
        'ram': RAM,
        'gpu': GPU,
        'psu': PowerSupply,
        'case': Case,
        'cooler': CPUCooler,
        'storage': Storage,
    }

    # Загрузка объектов
    components = {}
    for key, model in model_map.items():
        comp_id = build.get(key)
        if comp_id:
            try:
                components[key] = model.objects.get(id=comp_id)
            except model.DoesNotExist:
                components[key] = None
        else:
            components[key] = None

    compatible, messages = check_full_compatibility(components)
    return compatible, messages