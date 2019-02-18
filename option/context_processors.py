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
    Option.query_options(['site_name', 'site_seo_description', 'site_description', 'site_keywords',
                          'site_host', 'open_site_comment', 'beian_code', 'gongan_beian_code', 'show_gongan_code'])
    value = {
        'SITE_NAME': Option.get_option('site_name'),
        'SITE_SEO_DESCRIPTION': Option.get_option('site_seo_description'),
        'SITE_DESCRIPTION': Option.get_option('site_description'),
        'SITE_KEYWORDS': Option.get_option('site_keywords'),
        'SITE_BASE_URL': '%s://%s/' % (requests.scheme, Option.get_option('site_host')),
        'OPEN_SITE_COMMENT': Option.get_option('open_site_comment'),
        'BEIAN_CODE': Option.get_option('beian_code'),
        "BEIAN_CODE_GONGAN": Option.get_option('gongan_beian_code'),
        "SHOW_GONGAN_CODE": Option.get_option('show_gongan_code'),
    }
    cache.set(key, value, 60 * 60 * 10)

    return value
