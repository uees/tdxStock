from datetime import datetime, timedelta
from urllib.parse import parse_qsl, urlparse

from django.db.models.query import QuerySet


def object_to_json(model, ignore=None):
    if ignore is None:
        ignore = []
    if type(model) in [QuerySet, list]:
        json = []
        for element in model:
            json.append(_django_single_object_to_json(element, ignore))
        return json
    else:
        return _django_single_object_to_json(model, ignore)


def _django_single_object_to_json(element, ignore=None):
    return dict([(attr, getattr(element, attr)) for attr in [f.name for f in element._meta.fields]])


def timestamp(t):
    """时间对象转时间戳"""
    return int(round(t * 1000))


def fromtimestamp(t):
    """时间戳转时间对象"""
    t /= 1000
    if t < 0:
        return datetime(1970, 1, 1) + timedelta(seconds=t) + timedelta(hours=8)

    return datetime.fromtimestamp(t)


def trans_cookie(cookie_str):
    return string2dict(cookie_str)


def string2dict(string, eq="=", split=";"):
    result = {}
    items = string.split(split)

    for item in items:
        eq_pos = item.find(eq)
        key = item[:eq_pos].strip()
        value = item[eq_pos + len(eq):]
        result[key] = value

    return result


def get_params(response):
    params = {}
    url = response.request.url
    for item in parse_qsl(urlparse(url).query):
        params[item[0]] = item[1]

    return params
