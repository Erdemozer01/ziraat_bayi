import uuid

from django.db import models
from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.views import generic
from decimal import Decimal

from accounts.models import Customer
from .models import ProductCategory, Product, SubscriptModel, Cart, CartItem
from django.contrib import messages
from .forms import CustomerForm, UserForm


class CategoriesListView(generic.ListView):
    model = ProductCategory
    template_name = 'pages/bayi.html'

    def get_queryset(self):
        object_list = Product.objects.filter(category__slug=self.kwargs['slug'], is_stock=True)
        ara = self.request.GET.get('ara', None)
        if ara:
            object_list = object_list.filter(Q(name__icontains=ara) | Q(category__name=ara))
            messages.success(self.request, f'{len(object_list)} ürün bulundu')
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
    quantity = request.GET.get('quantity', None)

    if request.user.is_anonymous:
        messages.info(request, 'Üye olun yada giriş yapın')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if quantity:
        try:
            cart = Cart.objects.get(user=request.user, session_key=request.session.session_key)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=request.user, session_key=request.session.session_key)


        quantity = float(quantity)
        product.stock -= int(quantity)
        product.save()

        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.quantity += quantity
            cart_item.sub_total += product.price * quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            CartItem.objects.create(cart=cart, product=product, quantity=quantity, sub_total=product.price * quantity)

        cart.total += quantity * product.price
        cart.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ShoppingListView(generic.ListView):
    model = CartItem
    template_name = 'pages/dashboard.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            messages.info(request, 'Üye olun yada giriş yapın')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        try:
            cart = Cart.objects.get(user=self.request.user, session_key=request.session.session_key)
        except Cart.DoesNotExist:
            messages.info(self.request, 'Sepetiniz Boş')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        try:
            return CartItem.objects.filter(cart=Cart.objects.get(user=self.request.user))
        except:
            return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart.objects.get(user=self.request.user, session_key=self.request.session.session_key)
        context['cart'] = cart
        context['cart_items'] = CartItem.objects.filter(cart=cart)
        return context


def checkout(request, user, session_key):
    if request.user.username == user:
        cart_items = CartItem.objects.filter(cart__user__username=user, cart__session_key=session_key)
        cart = Cart.objects.get(user__username=user, session_key=session_key)
        try:
            customer = Customer.objects.get(user=request.user)
        except Customer.DoesNotExist:
            customer = Customer.objects.create(user=request.user)
        quantity = cart_items.aggregate(models.Sum('quantity'))['quantity__sum']
        form = UserForm(request.POST or None, instance=request.user)
        form2 = CustomerForm(request.POST or None, instance=customer)

        if request.method == 'POST':
            if form.is_valid() and form2.is_valid():
                form.save()
                address = form2.cleaned_data['address']
                telephone = form2.cleaned_data['telephone']
                customer.address = address
                customer.telephone = telephone
                form2.save()
                messages.success(request, 'Başarılı')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        return render(request, 'pages/checkout.html', {'form': form, 'cart_items': cart_items, 'cart': cart, 'quantity': quantity, 'form2': form2})

    else:

        messages.info(request, 'Sepetiniz Boş')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



