from django import template
from bayi.models import SettingsSite, ProductCategory
from django.contrib.admin.models import LogEntry
register = template.Library()


@register.simple_tag
def get_setting():
    try:
        return SettingsSite.objects.latest('created')
    except SettingsSite.DoesNotExist:
        return None

@register.simple_tag
def get_product_category():
    return ProductCategory.objects.all()


