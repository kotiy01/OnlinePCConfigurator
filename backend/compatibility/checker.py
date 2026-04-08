from .rules import check_full_compatibility, calculate_total_power

def check_compatibility_for_component(build, component_key, component_id):
    """ Проверка совместимости конкретного компонента с остальными в сборке """
    from components.models import CPU, Motherboard, RAM, GPU, PowerSupply, Case, CPUCooler, Storage
    from compatibility.rules import (
        check_cpu_motherboard, check_cpu_ram, check_cpu_cooler,
        check_motherboard_ram, check_motherboard_case, check_storage_motherboard,
        check_gpu_case, 
    )
    
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
    
    # Загрузка всеч компонентов сборки (кроме проверяемого)
    components = {}
    for key, model in model_map.items():
        if key == component_key:
            continue
        comp_id = build.get(key)
        if comp_id:
            try:
                components[key] = model.objects.get(id=comp_id)
            except model.DoesNotExist:
                components[key] = None
        else:
            components[key] = None
    
    # Загрузка проверяемого компонента
    try:
        model = model_map[component_key]
        new_component = model.objects.get(id=component_id)
    except (KeyError, model.DoesNotExist):
        return True, []
    
    # Проверка релевантных пары
    messages = []
    has_critical_error = False
    
    if component_key == 'cpu':
        if components.get('motherboard'):
            compatible, msgs = check_cpu_motherboard(new_component, components['motherboard'])
            messages.extend(msgs)
            if not compatible:
                has_critical_error = True
        if components.get('ram'):
            compatible, msgs = check_cpu_ram(new_component, components['ram'])
            messages.extend(msgs)
            if not compatible:
                has_critical_error = True
        if components.get('cooler'):
            compatible, msgs = check_cpu_cooler(new_component, components['cooler'])
            messages.extend(msgs)
            if not compatible:
                has_critical_error = True
    
    elif component_key == 'motherboard':
        if components.get('cpu'):
            compatible, msgs = check_cpu_motherboard(components['cpu'], new_component)
            messages.extend(msgs)
            if not compatible:
                has_critical_error = True
        if components.get('ram'):
            compatible, msgs = check_motherboard_ram(new_component, components['ram'])
            messages.extend(msgs)
            if not compatible:
                has_critical_error = True
        if components.get('case'):
            compatible, msgs = check_motherboard_case(new_component, components['case'])
            messages.extend(msgs)
            if not compatible:
                has_critical_error = True
        if components.get('storage'):
            compatible, msgs = check_storage_motherboard(components['storage'], new_component)
            messages.extend(msgs)
            if not compatible:
                has_critical_error = True
    
    elif component_key == 'ram':
        if components.get('motherboard'):
            compatible, msgs = check_motherboard_ram(components['motherboard'], new_component)
            messages.extend(msgs)
            if not compatible:
                has_critical_error = True
        if components.get('cpu'):
            compatible, msgs = check_cpu_ram(components['cpu'], new_component)
            messages.extend(msgs)
            if not compatible:
                has_critical_error = True
    
    elif component_key == 'gpu':
        # if components.get('psu'):
        #     total_power = calculate_total_power({**components, 'gpu': new_component})
        #     compatible, msgs = check_gpu_psu(new_component, components['psu'], total_power)
        #     messages.extend(msgs)
        #     if not compatible:
        #         has_critical_error = True
        if components.get('case'):
            compatible, msgs = check_gpu_case(new_component, components['case'])
            messages.extend(msgs)
            if not compatible:
                has_critical_error = True
    
    # elif component_key == 'psu':
        # if components.get('gpu'):
        #     total_power = calculate_total_power({**components, 'psu': new_component})
        #     compatible, msgs = check_gpu_psu(components['gpu'], new_component, total_power)
        #     messages.extend(msgs)
        #     if not compatible:
        #         has_critical_error = True
        # if components.get('case'):
        #     compatible, msgs = check_psu_case(new_component, components['case'])
        #     messages.extend(msgs)
        #     if not compatible:
        #         has_critical_error = True
    
    elif component_key == 'case':
        if components.get('motherboard'):
            compatible, msgs = check_motherboard_case(components['motherboard'], new_component)
            messages.extend(msgs)
            if not compatible:
                has_critical_error = True
        if components.get('gpu'):
            compatible, msgs = check_gpu_case(components['gpu'], new_component)
            messages.extend(msgs)
            if not compatible:
                has_critical_error = True
        # if components.get('psu'):
        #     compatible, msgs = check_psu_case(components['psu'], new_component)
        #     messages.extend(msgs)
        #     if not compatible:
        #         has_critical_error = True
    
    elif component_key == 'cooler':
        if components.get('cpu'):
            compatible, msgs = check_cpu_cooler(components['cpu'], new_component)
            messages.extend(msgs)
            if not compatible:
                has_critical_error = True
    
    elif component_key == 'storage':
        if components.get('motherboard'):
            compatible, msgs = check_storage_motherboard(new_component, components['motherboard'])
            messages.extend(msgs)
            if not compatible:
                has_critical_error = True
    
    return not has_critical_error, messages