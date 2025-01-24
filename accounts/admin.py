from django.contrib import admin
from .models import Customer
from bayi.models import Cart, CartItem


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'user__email', 'telephone', 'quantity', 'is_loan', 'date')
    list_filter = ('is_loan', 'date')
    search_fields = ('user__username', 'telephone')
    search_help_text = 'Müşteri adı veya telefon numarasına göre arama yap'
    readonly_fields = ('quantity', 'remain', 'is_loan', 'user', 'telephone', 'address', 'remain', 'cost')


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    classes = ['collapse']
    readonly_fields = ('product', 'quantity', 'sub_total')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user__first_name', 'user__last_name', 'user__email', 'total', 'created', 'last_date')
    search_fields = ('user__first_name', 'user__last_name', 'user__email')
    search_help_text = 'Ad, soyad yada Email adresine göre arayın.'
    readonly_fields = ('cart_number', 'is_ordered', 'user', 'total', 'created')
    list_editable = ('last_date', )
    inlines = [CartItemInline]



