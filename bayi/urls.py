from django.urls import path
from bayi import views
from django.views import generic

app_name = 'bayi'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='anasayfa'),
]