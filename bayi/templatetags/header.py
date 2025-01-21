from django import template
from bayi.models import Header

register = template.Library()


@register.simple_tag
def get_header():
    try:
        return Header.objects.latest('created')
    except Header.DoesNotExist:
        return None
