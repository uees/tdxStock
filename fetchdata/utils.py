import re
from datetime import datetime, timedelta
from urllib.parse import parse_qsl, urlparse

import pytz
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
    """时间对象转时间戳(毫秒级)"""
    if isinstance(t, datetime):
        return int(round(t.timestamp() * 1000))

    return int(round(t * 1000))


def fromtimestamp(t):
    """毫秒级时间戳转时间对象"""
    t /= 1000
    if t < 0:
        d = datetime(1970, 1, 1, tzinfo=pytz.utc) + timedelta(seconds=t)  # <1970 先转化为 UTC 时间
        tz = pytz.timezone('Asia/Shanghai')
        return d.astimezone(tz)  # 再转为北京时间

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


def get_quarter_by_report_type(report_type):
    if report_type in ['年报', '四季度']:
        return 4

    if report_type in ['三季报', '三季度']:
        return 3

    if report_type in ['中报', '二季度']:
        return 2

    if report_type in ['一季报', '一季度']:
        return 1


def get_quarter_date(year, quarter):
    if quarter == 1:
        return datetime(year, 3, 31)

    if quarter == 2:
        return datetime(year, 6, 30)

    if quarter == 3:
        return datetime(year, 9, 30)

    if quarter == 4:
        return datetime(year, 12, 31)


def parse_report_name(report_name):
    p = re.compile(r'(?P<year>\d{4})(?P<report_type>.+)')
    match = p.match(report_name)
    if match:
        report_year = int(match.group('year'))
        report_quarter = get_quarter_by_report_type(match.group('report_type'))

        return report_year, report_quarter

    return None, None


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
