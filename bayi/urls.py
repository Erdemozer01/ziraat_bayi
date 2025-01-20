from django.urls import path
from bayi import views
from django.views import generic

urlpatterns = [
    path('', generic.TemplateView.as_view(template_name='pages/index.html'), name='index'),
]