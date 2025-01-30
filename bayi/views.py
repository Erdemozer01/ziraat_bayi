import uuid
from django.utils import timezone

from django.contrib.auth.mixins import LoginRequiredMixin
from .email import email_sender
from django.db import models
from django.shortcuts import render, redirect
from django.db.models import Q, Sum
from django.http import HttpResponseRedirect

from django.views import generic

from accounts.models import Customer, OrderModel
from .models import Product, SubscriptModel, Cart, CartItem, Contact, CaseModel, SettingsSite
from django.contrib import messages
from .forms import CustomerForm, UserForm, ContactForm, CustomerInformationModelForm
from django.core.mail import settings
from django_plotly_dash import DjangoDash
from dash import html, dcc, Output, Input, dash_table
from collections import OrderedDict
import pandas as pd
import dash_bootstrap_components as dbc


def AboutView(request):
    form = ContactForm(request.POST or None)
    try:
        site = SettingsSite.objects.latest('created')
    except SettingsSite.DoesNotExist:
        site = None
    if request.method == 'POST':
        if form.is_valid():

            form.save(commit=False)

            messages.success(request, 'Mesajınız iletilmiştir. En kısa sürede cevap vereceğiz')

            subject = "İletişim Formu"

            from_email = settings.EMAIL_HOST_USER

            obj = Contact.objects.create(
                email=form.cleaned_data['email'],
                name=form.cleaned_data['name'],
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message'],
            )

            context = {
                'name': form.cleaned_data['name'],
                'email': form.cleaned_data['email'],
                'subject': form.cleaned_data['subject'],
                'message': form.cleaned_data['message'],
                'obj': obj,
                'site': request.META.get('HTTP_ORIGIN'),
            }

            email_sender(
                subject=subject,
                sender=from_email,
                recipients=from_email,
                template='contact',
                context=context,
            )

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        else:

            form = ContactForm()

    return render(request, 'pages/about.html', {'form': form, 'site': site})


class DashboardView(generic.ListView):
    model = Customer
    template_name = 'pages/dashboard.html'

    def get(self, request, *args, **kwargs):

        app = DjangoDash('IncomeTable', external_stylesheets=[dbc.themes.BOOTSTRAP])

        app.layout = dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Label('Kazanç', className='mt-3'),

                                dcc.Dropdown(
                                    options={
                                        'günlük': 'Günlük',
                                        'aylık': 'Aylık',
                                        'yıllık': 'Yıllık'
                                    },
                                    value="günlük",
                                    id="dates",
                                    clearable=False,
                                    className="dropdown mb-2",
                                ),

                                dbc.Label('Ay'),

                                dcc.Dropdown(
                                    id="months",
                                    options=[i for i in range(1, 13)],
                                    value=timezone.now().month,
                                    clearable=False,
                                    className="dropdown mb-2",
                                ),

                                dbc.Label('Yıl'),

                                dcc.Dropdown(
                                    id="years",
                                    options=[years.order_date.year for years in OrderModel.objects.all()],
                                    value=timezone.now().year,
                                    clearable=False,
                                    className="dropdown mb-4",
                                ),

                            ], md=4, sm=4, lg=4

                        ),

                        dbc.Col(
                            [
                                html.Div(id='table-content', style={'margin-top': '3rem'}),
                                html.Div(id='table-total', style={'float': 'right'}),
                            ], md=8, sm=8, lg=8, align='right'
                        ),
                    ]
                ),
            ],
        )

        @app.callback(
            Output('table-content', 'children'),
            Output('table-total', 'children'),
            Input('dates', 'value'),
            Input('months', 'value'),
            Input('years', 'value'),
        )
        def update_table(value, month, year):

            global obj

            if value == "günlük":
                obj = CaseModel.objects.filter(created_at__day=timezone.now().day, created_at__month=month,
                                               created_at__year=year)

            elif value == "aylık":
                obj = CaseModel.objects.filter(created_at__month=month, created_at__year=year)

            elif value == "yıllık":
                obj = CaseModel.objects.filter(created_at__year=year)

            data = OrderedDict(
                [
                    ("Ödeme Tarihi", [str(i.created_at.date()) for i in obj.all()]),
                    ("Müşteri", [str(i.order.customer.user) for i in obj.all()]),
                    ("Ürünler", [i.order.product.values('name').first().get('name') for i in obj.all()]),
                    ("Birim Fiyat", [i.order.product.values('price').first().get('price') for i in obj.all()]),
                    ("Adet", [str(i.order.quantity) for i in obj.all()]),
                    ("Toplam", [str(i.total) + " " + "TL" for i in obj.all()]),
                ]
            )

            total = obj.aggregate(Sum('total'))['total__sum']

            total_income = f"{value} Toplam Kazanç: {total} TL".upper()

            df = pd.DataFrame(data)

            table = dash_table.DataTable(
                data=df.to_dict('records'),
                columns=[{'id': c, 'name': c} for c in df.columns],
                page_size=20,
                sort_action='native',
            )

            return table, total_income

        return super().get(request, *args, **kwargs)

    def get_context_data(
            self, *, object_list=..., **kwargs
    ):
        context = super().get_context_data(**kwargs)
        context['is_read'] = Contact.objects.filter(is_read=False).count()
        return context


class CategoriesListView(generic.ListView):
    model = Product
    template_name = 'pages/bayi.html'

    def get_queryset(self):
        object_list = Product.objects.filter(is_stock=True, category__slug=self.kwargs['slug'])
        ara = self.request.GET.get('ara', None)
        category = str(self.kwargs['slug'].title().replace('-', ' '))
        if ara:
            object_list = object_list.filter(Q(name__icontains=ara) | Q(category__name__icontains=ara))
            messages.success(self.request,
                             f'{category} ürünlerinde {len(object_list)} ürün bulundu')
        return object_list


class ProductListView(generic.ListView):
    model = Product
    template_name = 'pages/bayi.html'

    def get_queryset(self):
        object_list = Product.objects.filter(is_stock=True)
        ara = self.request.GET.get('ara', None)
        if ara:
            object_list = object_list.filter(Q(name__icontains=ara) | Q(category__name__icontains=ara))
            messages.success(self.request, f'{len(object_list)} ürün bulundu')
        return object_list


class SubscriptView(generic.View):
    http_method_names = ['get', 'post']

    def get(self, request):
        email = request.GET.get('email', None)
        if SubscriptModel.objects.filter(email=email).exists():
            messages.info(request, "Zaten abonesiniz")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            SubscriptModel.objects.create(email=email)
            messages.success(request, "Bültenimize abone olduğunuz için teşekkür ederiz.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'pages/detail.html'

    def get_queryset(self):
        return Product.objects.filter(is_stock=True)

    def get(self, request, *args, **kwargs):
        ara = request.GET.get('ara')
        if ara:
            return HttpResponseRedirect('/?ara={}'.format(ara))
        else:
            return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.filter(
            Q(category__slug=self.get_object().category.slug) |
            Q(category__name__icontains=self.get_object().category.name) |
            Q(price=self.get_object().price)
        )
        context['recent_list'] = products.exclude(pk=self.get_object().pk).order_by('-created')[:10]
        context['new_products'] = Product.objects.filter(is_stock=True).order_by('-created')[:10]
        return context


def CartItemsAddView(request, pk):
    product = Product.objects.get(pk=pk)
    quantity = float(request.GET.get('quantity', None))

    if request.user.is_anonymous:
        messages.info(request, 'Üye olun yada giriş yapın')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if request.user.is_superuser:
        messages.info(request, 'Admin olarak oturum açtın')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if quantity:

        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=request.user, cart_number=uuid.uuid4(), total=quantity * product.price)

        try:

            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.quantity += quantity
            cart_item.sub_total += product.price * quantity
            cart_item.save()

        except CartItem.DoesNotExist:
            CartItem.objects.create(cart=cart, product=product, quantity=quantity, sub_total=product.price * quantity)

        messages.success(request, 'Ürün sepetinize eklendi')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ShoppingListView(generic.ListView):
    model = CartItem
    template_name = 'pages/dashboard.html'

    def get_queryset(self):
        try:
            cart = Cart.objects.get(user=self.request.user)
        except Cart.DoesNotExist:
            return None
        return CartItem.objects.filter(cart=cart)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            cart = Cart.objects.get(user=self.request.user)
        except Cart.DoesNotExist:
            return None
        context['cart'] = cart
        context['cart_items'] = CartItem.objects.filter(cart=cart)
        return context


def checkout(request, user, cart_number):
    if request.user.username == user:

        cart_items = CartItem.objects.filter(cart__user__username=user)
        cart = Cart.objects.get(user=request.user)

        try:
            customer = Customer.objects.get(user=request.user)
        except Customer.DoesNotExist:
            customer = Customer.objects.create(user=request.user)

        quantity = cart_items.aggregate(models.Sum('quantity'))['quantity__sum']
        total = cart_items.aggregate(models.Sum('sub_total'))['sub_total__sum']

        form = UserForm(request.POST or None, instance=request.user)
        form2 = CustomerForm(request.POST or None, instance=customer)

        if request.method == 'POST':

            if form.is_valid() and form2.is_valid():
                form.save()
                form2.save(commit=False)

                last_date = form2.cleaned_data['last_date']

                order = OrderModel.objects.create(customer=customer, order_number=cart_number, quantity=quantity,
                                                  remain=total, last_date=last_date, total=total)

                for item in cart_items:
                    order.product.add(item.product)
                    item.product.stock -= item.quantity
                    item.product.ordered += item.quantity
                    item.product.save()
                    if item.product.stock == 0:
                        item.product.is_stock = False
                    item.product.save()

                order.save()

                cart.delete()

                form2.save()

                customer.is_loan = True

                customer.bought += quantity

                customer.total_loan = OrderModel.objects.aggregate(models.Sum('remain'))['remain__sum']

                customer.save()

                messages.success(request, 'Satın alma başarılı')

                return redirect('/')

        context = {'form': form, 'cart_items': cart_items, 'cart': cart, 'quantity': quantity, 'form2': form2,
                   'customer': customer}

        return render(request, 'pages/checkout.html', context=context)

    else:
        messages.info(request, 'Sepet Bulunamadı')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class OrderListView(LoginRequiredMixin, generic.ListView):
    model = OrderModel
    template_name = 'pages/dashboard.html'
    context_object_name = 'order_list'

    def get_queryset(self):
        return OrderModel.objects.filter(customer__user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        remain = OrderModel.objects.filter(customer__user=self.request.user).aggregate(models.Sum('remain'))[
            'remain__sum']
        context['cost'] = remain
        return context


def delete_cart(request, cart_number):
    cart = Cart.objects.get(user__username=request.user, cart_number=cart_number)
    cart.delete()
    messages.success(request, 'Sepetinizi sildiniz')
    return redirect('/')


def remove_cart_item(request, pk):
    cart_item = CartItem.objects.get(pk=pk)
    cart_item.delete()
    if cart_item.product is not None:
        cart_item.cart.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def MyInformationDashBoardView(request, pk, user):
    if request.user.username == user:
        try:
            customer = Customer.objects.get(user=request.user)
        except Customer.DoesNotExist:
            customer = Customer.objects.create(user=request.user)
        form = CustomerInformationModelForm(request.POST or None, instance=customer)
        form2 = UserForm(request.POST or None, instance=request.user)
        if request.method == 'POST':
            if form.is_valid() or form2.is_valid():
                form.save(), form2.save()
                messages.success(request, 'Bilgileriniz Güncellendi')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.info(request, 'Yetkisiz işlem')
        return redirect('/')
    return render(request, 'pages/dashboard.html', {'form': form, 'form2': form2})


def mark_as_read(request, pk):
    if request.user.is_superuser:
        obj = Contact.objects.get(pk=pk)
        obj.is_read = True
        obj.save()
        messages.info(request, 'Okudundu olarak işaretlendi')
    return redirect('/')
