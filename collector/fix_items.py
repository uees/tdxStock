from django.db.models import Q
from twisted.internet import defer

from basedata.models import ReportItem


async def _fix_item(item):
    try:
        item.value_number = float(item.value)
    except ValueError:
        print('字符串%s' % item.id)
        item.value_type = 2  # 字符串
    else:
        item.value_type = 1
        item.value = None

    item.save()


async def fix_report_items(start, limit):
    items = ReportItem.objects.filter(
            Q(value__isnull=False) & Q(value_number__isnull=True) & Q(pk__gt=start)
        ).all()[:limit]
    count = 0
    next_start = -1
    for item in items:
        print('fixing... %s' % item.id)
        count += 1
        next_start = item.id
        if item.value_number is None:
            await _fix_item(item)

    if count < limit:
        print('最后一页')
        return

    await fix_report_items(next_start, limit)


def run():
    from twisted.internet import reactor

    defer.ensureDeferred(fix_report_items(0, 1000))
    reactor.run()
