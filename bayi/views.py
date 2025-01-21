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
