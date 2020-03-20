import json
import os

from .settings import BASE_DIR


def is_json_stringify(v):
    try:
        json.loads(v)
    except ValueError:
        return False
    return True


def is_number(value):
    try:
        value + 1
    except TypeError:
        return False
    else:
        return True


def is_number_like(value):
    try:
        int(value)
    except ValueError:
        return False
    else:
        return True


def str_fix_null(value):
    if value is None:
        value = ''
    return value


def dict_merge(target: dict, origin: dict):
    """ 嵌套字典合并 """
    for key in origin.keys():
        if isinstance(target.get(key), dict) and isinstance(origin[key], dict):
            dict_merge(target[key], origin[key])
        else:
            target[key] = origin[key]


def read_cookie(name):
    path = os.path.join(os.path.join(BASE_DIR, 'storage/cookies'), name)
    with open(path, 'r') as f:
        cookie_str = f.readline()

    return string2dict(cookie_str)


def string2dict(string, eq='=', split=';'):
    result = {}
    for item in string.split(split):
        pos = item.find(eq)
        key = item[:pos].strip()
        value = item[pos + len(eq):]
        result[key] = value

    return result
