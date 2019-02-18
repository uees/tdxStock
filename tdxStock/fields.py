from django_extensions.db.fields import json
from json.decoder import JSONDecodeError


class JSONField(json.JSONField):

    def to_python(self, value):
        """Convert our string value to JSON after we load it from the DB"""
        try:
            res = json.loads(value)
        except JSONDecodeError:
            res = value
        except TypeError:
            res = value

        if isinstance(res, dict):
            return json.JSONDict(**res)
        elif isinstance(res, list):
            return json.JSONList(res)

        return res

    def get_prep_value(self, value):
        """将 python 对象转换为查询值"""
        return json.dumps(value)
