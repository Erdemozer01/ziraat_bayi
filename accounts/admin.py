from django.conf import settings
from django.contrib import admin
from django.http import HttpResponseRedirect

from .models import Customer, OrderModel
from bayi.models import CaseModel
from django.contrib import messages
from bayi.email import email_sender

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'user__email', 'telephone', 'total_loan', 'total_pay', 'is_loan', 'date')
    list_filter = ('is_loan', 'date')
    search_fields = ('user__username', 'telephone')
    search_help_text = 'Müşteri adı veya telefon numarasına göre arama yap'
    readonly_fields = ('user', 'telephone', 'address', 'total_loan', 'bought', 'is_loan', 'total_pay')


@admin.register(OrderModel)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer', 'payment', 'total', 'remain', 'order_date', 'last_date', 'cost')
    list_filter = ('customer', 'payment', 'order_date')
    list_editable = ('cost',)
    readonly_fields = ('order_number', 'customer', 'payment', 'total', 'remain', 'product', 'quantity')
    search_fields = ('customer__user__username', 'customer__telephone', 'customer__user__email', 'customer__address')
    search_help_text = 'Müşteri, telefon, email göre arama yap...'
    actions = ['loan_reminder']

    @admin.action(description='Borcunu Hatırlat')
    def loan_reminder(self, request, queryset):
        total_remain = 0
        for order in queryset:

            total_remain += order.remain

            context = {
                'order_number': order.order_number,
                'ad': order.customer.user.first_name + ' ' + order.customer.user.last_name,
                'payment': order.payment,
                'total': total_remain,
                'remain': order.remain,
                'order_date': order.order_date,
                'email': order.customer.user.email,
                'address': order.customer.address,
                'phone': order.customer.telephone,
                'order_list': queryset,
                'last_date': order.last_date,
                'site': request.META.get('HTTP_ORIGIN')
            }
            email_sender(
                subject="Borç Hatırlatma",
                sender=settings.EMAIL_HOST_USER,
                recipients=order.customer.user.email,
                template="loan",
                context=context,
            )

            messages.success(request, 'Borç hatırlatma başarılı.')

            messages.success(request, 'Email Başarılı şekilde gönderildi.')

    def save_model(self, request, obj, form, change):

        if change:

            if obj.payment == 'Borç':

                if obj.remain > 0:

                    obj.remain -= obj.cost
                    obj.customer.total_loan -= obj.cost
                    CaseModel.objects.create(order=obj, total=obj.cost)

                    obj.save()

                    if obj.customer.total_loan <= 0:
                        obj.customer.total_loan = 0
                        obj.customer.is_loan = False

                    obj.customer.save()
                    obj.cost = 0
                    obj.save()

                else:
                    messages.error(request, 'Borç bulunmamaktadır')
                    pass
            else:
                messages.error(request, 'Borç bulunmamaktadır')
                pass
        else:
            CaseModel.objects.create(order=obj, total=obj.cost)
            return super().save_model(request, obj, form, change)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
