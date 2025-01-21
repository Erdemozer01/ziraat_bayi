from django.db import models
from autoslug.fields import AutoSlugField
from django_ckeditor_5.fields import CKEditor5Field


class SettingsSite(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Site Adı")

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Site Ayarları'
        verbose_name_plural = 'Site Ayarları'


class Header(models.Model):
    title = models.CharField(max_length=100, verbose_name='Başlık')
    content = CKEditor5Field(config_name='extends', verbose_name='İçerik')
    slug = AutoSlugField(populate_from='title')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Duyuru'
        verbose_name_plural = 'Duyuru'


class ProductCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True, verbose_name='Kategori')

    created = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')

    slug = AutoSlugField(populate_from='name', unique_with='created', default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ürün Kategorisi'
        verbose_name_plural = 'Ürün Kategorisi'


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name='Ürün Kategorisi',
                                 related_name='categories')
    image = models.ImageField(upload_to='product/')
    name = models.CharField(max_length=100, verbose_name='Ürün adı')
    content = CKEditor5Field(config_name='extends', verbose_name='İçerik')

    stock = models.PositiveIntegerField(default=0, verbose_name='Stok')
    price = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Birim Fiyat', blank=True, null=True)
    ordered = models.PositiveIntegerField(verbose_name='Satış adeti', default=0, db_index=True)
    is_stock = models.BooleanField(default=True, verbose_name='Stokta var mı ?')

    created = models.DateTimeField(auto_now_add=True, verbose_name='Eklenme Tarihi')
    updated = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ürün'
        verbose_name_plural = 'Ürünler'
