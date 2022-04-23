import logging

from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter

# Get an instance of a logger
logger = logging.getLogger(__name__)

register = template.Library()


@register.simple_tag
def timeformat(time_data):
    try:
        return time_data.strftime(settings.TIME_FORMAT)
    except Exception as e:
        logger.error(e)
        return ""


@register.simple_tag
def datetimeformat(datetime_data):
    try:
        return datetime_data.strftime(settings.DATE_TIME_FORMAT)
    except Exception as e:
        logger.error(e)
        return ""


@register.filter(is_safe=True)
@stringfilter
def truncate(content: str):
    from django.utils.html import strip_tags

    return strip_tags(content)[:150]


@register.simple_tag
def query(qs, **kwargs):
    """ template tag which allows queryset filtering. Usage:
          {% query books author=author as mybooks %}
          {% for book in mybooks %}
            ...
          {% endfor %}
    """
    return qs.filter(**kwargs)
