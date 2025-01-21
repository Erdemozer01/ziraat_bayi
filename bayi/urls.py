from django.urls import path
from bayi import views
from django.views import generic

app_name = 'bayi'

urlpatterns = [
    path('', generic.TemplateView.as_view(template_name='pages/bayi.html'), name='anasayfa'),
]