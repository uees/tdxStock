import json

from django.db import models
from django_extensions.db.fields.json import JSONField as JField

from tdxStock.helpers import is_json_stringify


class JSONField(JField):
    """支持纯字符串的JSONField"""

    def to_python(self, value):
        """Convert our string value to JSON after we load it from the DB"""
        try:
            res = super().to_python(value)
        except json.decoder.JSONDecodeError:
            res = value

        return res

    def get_db_prep_save(self, value, connection, **kwargs):
        """Convert our JSON object to a string before we save"""

        if isinstance(value, str) and not is_json_stringify(value):
            value = json.dumps(value)

        return super().get_db_prep_save(value, connection, **kwargs)


# MySQL unsigned integer (range 0 to 4294967295).
class UnsignedAutoField(models.AutoField):
    def db_type(self, connection):
        return 'integer UNSIGNED AUTO_INCREMENT'

    def rel_db_type(self, connection):
        return 'integer UNSIGNED'


class UnsignedBigAutoField(models.AutoField):
    def db_type(self, connection):
        return 'BIGINT UNSIGNED AUTO_INCREMENT'

    def rel_db_type(self, connection):
        return 'BIGINT UNSIGNED'
