from django.urls import path
from bayi import views

app_name = 'bayi'

urlpatterns = [
    path('', views.ProductListView, name='anasayfa'),
    path('<slug>/', views.CategoriesListView.as_view(), name='category_list'),
    path('abone-ol', views.SubscriptView.as_view(), name='abone_ol'),
    path('ayrıntılar/<pk>/<slug>/<name>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('add-cart/<pk>/', views.CartItemsAddView, name='add_cart'),
    path('sepetim/<user>/', views.ShoppingListView.as_view(), name='sepetim'),
    path('siparis-özeti/<user>/<cart_number>/', views.checkout, name='checkout'),
    path('siparişlerim/<user>/', views.OrderListView.as_view(), name='shoppinglist'),
    path('delete-cart/<cart_number>/', views.delete_cart, name='delete_cart'),
    path('remove-cart-item/<pk>/', views.remove_cart_item, name='remove_cart_item'),
    path('contact/', views.contact, name='contact'),
]
