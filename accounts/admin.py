from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer', 'telephone', 'quantity', 'is_loan', 'date')
    list_filter = ('is_loan', 'date')
    search_fields = ('customer__username', 'telephone')
    search_help_text = 'Müşteri adı veya telefon numarasına göre arama yap'
