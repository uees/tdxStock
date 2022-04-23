import logging

from django.core.cache import cache

from .models import Option

logger = logging.getLogger(__name__)


def options_processor(requests):
    key = 'options_cache'
    value = cache.get(key)
    if value:
        return value

    logger.info('set options cache.')
    options = Option.objects.filter(name__in=['site_name',
                                              'site_seo_description',
                                              'site_description',
                                              'site_keywords',
                                              'site_host',
                                              'site_comment_status']).all()
    value = {}
    for option in options:
        value[option.name.upper()] = option.value

    cache.set(key, value, 60 * 60 * 10)

    return value
