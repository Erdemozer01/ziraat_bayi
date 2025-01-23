from django.contrib import admin
from .models import Customer
from bayi.models import Cart, CartItem


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'telephone', 'quantity', 'is_loan', 'date')
    list_filter = ('is_loan', 'date')
    search_fields = ('user__username', 'telephone')
    search_help_text = 'Müşteri adı veya telefon numarasına göre arama yap'


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    classes = ['collapse']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'user', 'total', 'created')
    search_fields = ('session_key', 'user__username')
    inlines = [CartItemInline]
