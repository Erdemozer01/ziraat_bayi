from django import template
from bayi.models import SettingsSite, ProductCategory

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
