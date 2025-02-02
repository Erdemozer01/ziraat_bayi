# Generated by Django 5.1.5 on 2025-02-01 04:42

import autoslug.fields
import django.db.models.deletion
import django_ckeditor_5.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100, verbose_name='Konu')),
                ('name', models.CharField(max_length=100, verbose_name='Ad Soyad')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('message', models.TextField(verbose_name='Mesaj')),
                ('is_read', models.BooleanField(default=False, verbose_name='Cevaplandı ?')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Gönderilme Tarihi')),
            ],
            options={
                'verbose_name': 'İletişim',
                'verbose_name_plural': 'İletişim',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Header',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Başlık')),
                ('content', django_ckeditor_5.fields.CKEditor5Field(verbose_name='İçerik')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='title')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')),
            ],
            options={
                'verbose_name': 'Duyuru',
                'verbose_name_plural': 'Duyuru',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='product/')),
                ('name', models.CharField(max_length=100, verbose_name='Ürün adı')),
                ('content', django_ckeditor_5.fields.CKEditor5Field(verbose_name='İçerik')),
                ('stock', models.PositiveIntegerField(default=0, verbose_name='Stok')),
                ('price', models.FloatField(verbose_name='Fiyat')),
                ('ordered', models.PositiveIntegerField(db_index=True, default=0, verbose_name='Satış adeti')),
                ('is_stock', models.BooleanField(default=True, verbose_name='Stokta var mı ?')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Eklenme Tarihi')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')),
            ],
            options={
                'verbose_name': 'Ürün',
                'verbose_name_plural': 'Ürünler',
            },
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, unique=True, verbose_name='Kategori')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')),
                ('slug', autoslug.fields.AutoSlugField(default='', editable=False, populate_from='name', unique_with=('created',))),
            ],
            options={
                'verbose_name': 'Ürün Kategorisi',
                'verbose_name_plural': 'Ürün Kategorisi',
            },
        ),
        migrations.CreateModel(
            name='SettingsSite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Site Adı')),
                ('favicon', models.ImageField(blank=True, null=True, upload_to='favicon', verbose_name='Favicon')),
                ('phone', models.CharField(blank=True, max_length=11, null=True, verbose_name='Telefon No')),
                ('address', models.TextField(blank=True, null=True, verbose_name='Adres')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Site Ayarları',
                'verbose_name_plural': 'Site Ayarları',
            },
        ),
        migrations.CreateModel(
            name='SubscriptModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='Email adresini giriniz')),
            ],
            options={
                'verbose_name': 'Abone',
                'verbose_name_plural': 'Aboneler',
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_number', models.CharField(max_length=100, verbose_name='Sepet ID')),
                ('total', models.FloatField(default=0)),
                ('is_ordered', models.BooleanField(default=False, verbose_name='Sipariş verildi mi ?')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to=settings.AUTH_USER_MODEL, verbose_name='Müşteri')),
            ],
            options={
                'verbose_name': 'Sepet',
                'verbose_name_plural': 'Sepetler',
            },
        ),
        migrations.CreateModel(
            name='CaseModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.FloatField(verbose_name='Ödenen')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Ödeme Tarihi')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.ordermodel', verbose_name='Sipariş')),
            ],
            options={
                'verbose_name': 'Kasa',
                'verbose_name_plural': 'Kasa',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Miktar')),
                ('sub_total', models.FloatField(default=0, verbose_name='Ara Toplam')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_item', to='bayi.cart', verbose_name='Sepet')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='product_item', to='bayi.product', verbose_name='Ürün')),
            ],
            options={
                'verbose_name': 'Sepetteki Ürün',
                'verbose_name_plural': 'Sepetteki Ürünler',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='bayi.productcategory', verbose_name='Ürün Kategorisi'),
        ),
    ]
