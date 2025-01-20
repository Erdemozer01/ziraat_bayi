from django.contrib import admin
from .models import Customer, Product, ProductCategory, Header, SettingsSite


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


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer', 'telephone', 'quantity', 'is_loan', 'date')
    list_filter = ('is_loan', 'date')
    search_fields = ('customer__username', 'telephone')
    search_help_text = 'Müşteri adı veya telefon numarasına göre arama yap'
