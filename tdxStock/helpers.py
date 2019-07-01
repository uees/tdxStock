import json


def is_json_stringify(v):
    try:
        json.loads(v)
    except ValueError:
        return False
    return True
