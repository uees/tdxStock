import json


def is_json_stringify(v):
    try:
        json.loads(v)
    except ValueError:
        return False
    return True


def dict_merge(target: dict, origin: dict):
    """ 嵌套字典合并 """
    for key in origin.keys():
        if isinstance(target.get(key), dict) and isinstance(origin[key], dict):
            dict_merge(target[key], origin[key])
        else:
            target[key] = origin[key]
