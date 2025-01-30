from django.contrib import admin

from .models import Customer, OrderModel
from bayi.models import CaseModel


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'user__email', 'telephone', 'total_loan', 'total_pay', 'is_loan', 'date')
    list_filter = ('is_loan', 'date')
    search_fields = ('user__username', 'telephone')
    search_help_text = 'Müşteri adı veya telefon numarasına göre arama yap'
    readonly_fields = ('user', 'telephone', 'address', 'total_loan', 'bought', 'is_loan', 'total_pay')


@admin.register(OrderModel)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer', 'total', 'remain', 'order_date', 'last_date', 'cost')
    list_filter = ('customer', 'order_date')
    list_editable = ('cost',)
    readonly_fields = ('order_number', 'customer', 'total', 'remain', 'product', 'quantity')
    search_fields = ('customer__user__username', 'customer__telephone', 'customer__user__email', 'customer__address')
    search_help_text = 'Müşteri, telefon, email göre arama yap...'

    def save_model(self, request, obj, form, change):
        if change:

            obj.remain -= form.cleaned_data['cost']
            obj.cost = None
            if obj.remain >= 0:
                obj.save()
            obj.customer.total_loan -= form.cleaned_data['cost']
            obj.customer.total_pay += form.cleaned_data['cost']
            obj.customer.save()

            CaseModel.objects.create(order=obj, total=form.cleaned_data['cost'])

            if obj.customer.total_loan <= 0:
                obj.customer.is_loan = False
                obj.customer.total_loan = 0
                obj.customer.save()
        else:
            return super().save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False
