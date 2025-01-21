from django.db.models import Q
from django.views import generic
from .models import ProductCategory, Product
from django.contrib import messages


class CategoriesListView(generic.ListView):
    model = ProductCategory
    template_name = 'pages/bayi.html'

    def get_queryset(self):
        object_list = Product.objects.filter(category__slug=self.kwargs['slug'])
        ara = self.request.GET.get('ara', None)
        if ara:
            object_list = object_list.filter(Q(name__icontains=ara) | Q(category__name=ara))
            messages.success(self.request, f'{len(object_list)} ürün bulundu')
        return object_list


class ProductListView(generic.ListView):
    model = Product
    template_name = 'pages/bayi.html'

    def get_queryset(self):
        object_list = Product.objects.all()
        ara = self.request.GET.get('ara', None)
        if ara:
            object_list = object_list.filter(Q(name__icontains=ara) | Q(category__name__icontains=ara))
            messages.success(self.request, f'{len(object_list)} ürün bulundu')
        return object_list
