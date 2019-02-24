import json

from django_extensions.db.fields.json import JSONField

from tdxStock.helpers import is_json_stringify


class JSONField(JSONField):
    """支持纯字符串的JSONField"""

    def get_db_prep_save(self, value, connection, **kwargs):
        """Convert our JSON object to a string before we save"""

        if isinstance(value, str) and not is_json_stringify(value):
            value = json.dumps(value)

        return super().get_db_prep_save(value, connection, **kwargs)
