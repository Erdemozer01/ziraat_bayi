from django.db.models import Q
from django.views import generic
from .models import ProductCategory, Product


class CategoriesListView(generic.ListView):
    model = ProductCategory
    template_name = 'pages/bayi.html'
    paginate_by = 10


class ProductListView(generic.ListView):
    model = Product
    template_name = 'pages/bayi.html'
    paginate_by = 10
    context_object_name = 'product_list'

    def get_queryset(self):
        object_list = Product.objects.all()
        ara = self.request.GET['ara']
        if ara:
            object_list = object_list.filter(Q(name__icontains=ara) | Q(category__name=ara))
        return object_list
