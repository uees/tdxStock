from django.db import models
from django.utils import timezone


class Timestamp(models.Model):
    created_at = models.DateTimeField("创建时间", null=True, editable=False, default=timezone.now)
    updated_at = models.DateTimeField("更新时间", null=True, editable=False, auto_now=True)  # 调用 save() 会自动更新, 调用 objects.update 不会更新

    class Meta:
        abstract = True


class DynamicModel(object):
    _instance = dict()

    def __new__(cls, base_cls, db_table):
        """
        创建类根据表名
        :param base_cls: 类名(这个类要models基类)
        :param tb_name: 表名
        :return: base_cls 类的实例
        """
        new_cls_name = "%s_To_%s" % (base_cls.__name__, '_'.join(map(lambda x: x.capitalize(), db_table.split('_'))))
        if new_cls_name not in cls._instance:
            new_meta_cls = base_cls.Meta
            new_meta_cls.db_table = db_table
            model_cls = type(
                str(new_cls_name),
                (base_cls,),
                {
                    '__tablename__': db_table,
                    'Meta': new_meta_cls,
                    '__module__': cls.__module__
                }
            )
            cls._instance[new_cls_name] = model_cls

        return cls._instance[new_cls_name]
