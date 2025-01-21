from django import template
from bayi.models import SettingsSite

register = template.Library()


@register.simple_tag
def get_setting():
    return SettingsSite.objects.latest('created')
