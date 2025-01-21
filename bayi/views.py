from django.db.models import Q
from django.views import generic
from .models import ProductCategory, Product
from django.contrib import messages

class CategoriesListView(generic.ListView):
    model = ProductCategory
    template_name = 'pages/bayi.html'
    paginate_by = 10


class ProductListView(generic.ListView):
    model = Product
    template_name = 'pages/bayi.html'
    paginate_by = 10

    def get_queryset(self):
        object_list = Product.objects.all()
        ara = self.request.GET.get('ara', None)
        if ara:
            object_list = object_list.filter(Q(name__icontains=ara) | Q(category__name=ara))
            messages.success(self.request, f'{len(object_list)} ürün bulundu')
        return object_list
