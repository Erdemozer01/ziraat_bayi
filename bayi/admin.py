from django.contrib import admin
from django.contrib import messages
from django.http import HttpResponseRedirect

from .models import Product, ProductCategory, Header, SettingsSite, SubscriptModel, Cart, CartItem, CaseModel, Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'email', 'is_read', 'created')
    list_filter = ('email', 'created',)
    search_fields = ('subject', 'email',)
    search_help_text = 'Konu veya Email'

    def has_add_permission(self, request):
        return False


@admin.register(SubscriptModel)
class SubscriptAdmin(admin.ModelAdmin):
    list_display = ('email',)

    def has_add_permission(self, request):
        return False


@admin.register(SettingsSite)
class SettingsSiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'address', 'created', 'updated')

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
    list_editable = ('price', 'stock',)
    readonly_fields = ('created', 'is_stock', 'ordered')


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    classes = ['collapse']
    readonly_fields = ('product', 'sub_total', 'quantity')
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user__first_name', 'user__last_name', 'user__email', 'total', 'is_ordered', 'created',)
    search_fields = ('user__first_name', 'user__last_name', 'user__email')
    search_help_text = 'Ad, soyad yada Email adresine göre arayın.'
    readonly_fields = ('cart_number', 'is_ordered', 'user', 'total', 'created')
    list_filter = ('is_ordered', 'created',)
    inlines = [CartItemInline]

    def has_add_permission(self, request):
        return False


@admin.display(description="Sipariş Numarası")
def order_number(obj):
    return f"{obj.order.order_number}".upper()


@admin.display(description="Müşteri")
def customer(obj):
    return f"{obj.order.customer.user}".upper()


@admin.register(CaseModel)
class CaseModelAdmin(admin.ModelAdmin):
    list_display = (order_number, customer, 'total', 'created_at',)
    list_filter = ('created_at',)
    search_fields = ('order__order_number', 'order__cost', 'order__customer__user__username')
    search_help_text = 'Sipariş Numarası, ödeme tutarı, kullanıcı adı göre ara...'
    readonly_fields = ('order', 'created_at', 'total')

    def has_add_permission(self, request):
        return False

    def delete_queryset(self, request, queryset):
        if len(queryset) > 1:
            messages.error(request, 'Sadece bir işlemi silebilirsiniz')
            return HttpResponseRedirect(request.get_full_path())


        elif len(queryset) == 1:

            for case in queryset:
                case.order.remain += case.total
                case.order.save()

                case.order.customer.total_loan += case.total
                case.order.customer.total_pay -= case.total
                case.order.customer.is_loan = True
                case.order.customer.save()

            return super().delete_queryset(request, queryset)
