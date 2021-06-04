from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def settings(*names):
    result = ""
    for name in names:
        result += getattr(settings, name, "")

    return result
