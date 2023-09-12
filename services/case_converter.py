def snake_to_camel(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def to_camel_case_mapper(json_obj):
    if isinstance(json_obj, list):
        return [to_camel_case_mapper(item) for item in json_obj]
    elif isinstance(json_obj, dict):
        return {snake_to_camel(key): to_camel_case_mapper(value) for key, value in json_obj.items()}
    else:
        return json_obj