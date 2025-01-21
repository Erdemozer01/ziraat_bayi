from django.contrib import admin
from .models import Product, ProductCategory, Header, SettingsSite


@admin.register(SettingsSite)
class SettingsSiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created', 'updated')

    def has_add_permission(self, request):
        if SettingsSite.objects.count() == 0:
            return True
        else:
            return False


@admin.register(Header)
class HeaderAdmin(admin.ModelAdmin):
    list_display = ('title', 'created')

    def has_add_permission(self, request):
        if Header.objects.count() == 0:
            return True
        else:
            return False


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'stock', 'price', 'ordered', 'is_stock')
    list_filter = ('name', 'price',)
    search_fields = ('name', 'category__name')



