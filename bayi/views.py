from django.db.models import Q
from django.http import HttpResponseRedirect
from django.views import generic
from .models import ProductCategory, Product, SubscriptModel
from django.contrib import messages


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
