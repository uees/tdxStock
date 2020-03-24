from django.db import connection, models
from django.utils import timezone


class Timestamp(models.Model):
    created_at = models.DateTimeField("创建时间", null=True, editable=False, default=timezone.now)
    updated_at = models.DateTimeField("更新时间", null=True, editable=False, auto_now=True)  # 调用 save() 会自动更新, 调用 objects.update 不会更新

    class Meta:
        abstract = True


class DynamicModel(object):
    _instance = dict()
    _tables = [tableinfo.name for tableinfo in connection.introspection.get_table_list(connection.cursor())]

    def __new__(cls, base_cls, db_table_suffix):
        """
        创建类
        :param base_cls: 模型基类, 要在基类 Meta 中定义 abstract = True
        :param db_table_suffix: 表后缀
        :return new_model_cls: 类
        """
        new_cls_name = f"{base_cls.__name__}_{db_table_suffix}"
        if new_cls_name not in cls._instance:
            new_db_table = "{}_{}".format(base_cls._meta.db_table, db_table_suffix)
            model_cls = type(new_cls_name, (base_cls,), {'__module__': base_cls.__module__})
            model_cls._meta.db_table = new_db_table
            cls._instance[new_cls_name] = model_cls

            # 不存在表则创建表
            if new_db_table not in cls._tables:
                with connection.schema_editor() as schema_editor:
                    schema_editor.create_model(model_cls)
                    cls._tables.append(new_db_table)

        return cls._instance[new_cls_name]
