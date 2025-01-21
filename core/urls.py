from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django_ckeditor_5.views import upload_file
from bayi.models import SettingsSite

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path("ckeditor5/image_upload/", upload_file, name="ckeditor_upload_file"),
    path(r"images-handler/", include("galleryfield.urls")),
    path('', include('bayi.urls')),
    path('müşteriler/', include('accounts.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

try:
    site = SettingsSite.objects.latest('created')
    admin.site.site_title = site.name + ' Yönetici Paneli'
    admin.site.site_header = site.name + ' Yönetici Paneli'
    admin.site.index_title = site.name + ' Yönetici Paneli'
    admin.site.name = site.name + ' Yönetici Paneli'
except:
    pass
