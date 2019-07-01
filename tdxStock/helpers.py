import json

from django.db import connection

from tdxStock.abstract_models import DynamicModel


def is_json_stringify(v):
    try:
        json.loads(v)
    except ValueError:
        return False
    return True


def get_or_create_model(base_cls, db_table):
    model_cls = DynamicModel(base_cls, db_table)

    cursor = connection.cursor()
    if db_table not in connection.introspection.get_table_list(cursor):
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(model_cls)

    return model_cls
