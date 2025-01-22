from django import template
from bayi.models import ProductCategory

register = template.Library()


@register.simple_tag
def get_product_category():
    return ProductCategory.objects.all()


@register.filter(name='breadcrumbs')
def breadcrumbs(value):
    return value.rsplit('/', 2)[1].replace('-', ' ')