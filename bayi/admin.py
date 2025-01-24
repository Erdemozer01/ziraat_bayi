from django.contrib import admin
from .models import Product, ProductCategory, Header, SettingsSite, SubscriptModel


@admin.register(SubscriptModel)
class SubscriptAdmin(admin.ModelAdmin):
    list_display = ('email',)

    def has_add_permission(self, request):
        return False


@admin.register(SettingsSite)
class SettingsSiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'updated')

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
    list_filter = ('is_stock',)
    search_fields = ('name', 'category__name')
    search_help_text = 'Başlık yada Kategori adı'
    list_editable = ('price',)
    readonly_fields = ('created', 'is_stock', 'ordered')




