from django.urls import path
from bayi import views
from django.views import generic

urlpatterns = [
    path('dashboard/', generic.TemplateView.as_view(template_name='pages/dashboard.html'), name='Dashboard'),
    path('', generic.TemplateView.as_view(template_name='pages/bayi.html'), name='bayi'),
]