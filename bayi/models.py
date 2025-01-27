from django.db import models
from autoslug.fields import AutoSlugField
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field


class SettingsSite(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Site Adı")
    favicon = models.ImageField(upload_to="favicon", null=True, verbose_name="Favicon", blank=True)


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
    price = models.FloatField(verbose_name='Fiyat')
    ordered = models.PositiveIntegerField(verbose_name='Satış adeti', default=0, db_index=True)
    is_stock = models.BooleanField(default=True, verbose_name='Stokta var mı ?')

    created = models.DateTimeField(auto_now_add=True, verbose_name='Eklenme Tarihi')
    updated = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ürün'
        verbose_name_plural = 'Ürünler'


class Cart(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='cart', verbose_name='Müşteri')
    cart_number = models.CharField(max_length=100, verbose_name='Sepet ID')
    total = models.FloatField(default=0)
    is_ordered = models.BooleanField(default=False, verbose_name='Sipariş verildi mi ?')

    created = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')

    def __str__(self):
        return self.user.username + ' ' + self.cart_number

    class Meta:
        verbose_name = 'Sepet'
        verbose_name_plural = 'Sepetler'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_item', verbose_name='Sepet')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='product_item', verbose_name='Ürün')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Miktar')
    sub_total = models.FloatField(default=0, verbose_name='Ara Toplam')

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = 'Sepetteki Ürün'
        verbose_name_plural = 'Sepetteki Ürünler'


class CaseModel(models.Model):
    order = models.ForeignKey('accounts.OrderModel', on_delete=models.CASCADE, verbose_name='Sipariş')
    total = models.FloatField(verbose_name='Ödenen')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ödeme Tarihi')

    class Meta:
        verbose_name = 'Kasa'
        verbose_name_plural = 'Kasa'

    def save(self, *args, **kwargs):
        if self.order.remain >= 0:
            return super().save(*args, **kwargs)
        else:
            pass


class Contact(models.Model):
    subject = models.CharField(max_length=100, verbose_name='Konu')
    name = models.CharField(max_length=100, verbose_name='Ad Soyad')
    email = models.EmailField(verbose_name='Email')
    message = models.TextField(verbose_name='Mesaj')

    created = models.DateTimeField(auto_now_add=True, verbose_name='Gönderilme Tarihi')

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'İletişim'
        verbose_name_plural = 'İletişim'


class SubscriptModel(models.Model):
    email = models.EmailField(verbose_name='Email adresini giriniz')

    class Meta:
        verbose_name = "Abone"
        verbose_name_plural = "Aboneler"
