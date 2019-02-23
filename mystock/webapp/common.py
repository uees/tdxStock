# -*- coding: utf-8 -*-
'''
Created on 2016-12-14

@author: Wan
'''
import functools
import json

import pandas as pd
from flask import abort, url_for
from flask_login import current_user
from pandas.io.json import json_normalize

from webapp.extensions import cache

cached = functools.partial(cache.cached,
                           unless=lambda: current_user.is_authenticated)


def q_and(x, y=None):
    if y:
        return x & y
    else:
        return x


def q_or(x, y=None):
    if y:
        return x | y
    else:
        return x


def to_int(value):
    try:
        value = int(value)
    except:
        abort(404)
    return value


def page_url(endpoint, **kwargs):
    def page_url(**kwargs):
        return url_for(endpoint, **kwargs)
    return page_url


def json_list(objs):
    return [obj.json for obj in objs]


def mongo_to_dataframe(mongo_data):

    sanitized = json.loads(mongo_data.to_json())
    try:
        normalized = json_normalize(sanitized)
    except IndexError:
        df = None
    else:
        df = pd.DataFrame(normalized)
        del df['_id.$oid']

    return df
