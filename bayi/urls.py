from django.urls import path
from bayi import views
from django.views import generic

app_name = 'bayi'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='anasayfa'),
    path('<slug>/', views.CategoriesListView.as_view(), name='category_list'),
    path('abone-ol', views.SubscriptView.as_view(), name='abone_ol'),
    path('ayrıntılar/<pk>/<slug>/<name>/', views.ProductDetailView.as_view(), name='product_detail'),
]