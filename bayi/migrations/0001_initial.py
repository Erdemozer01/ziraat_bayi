# Generated by Django 5.1.5 on 2025-01-23 05:02

import autoslug.fields
import django.db.models.deletion
import django_ckeditor_5.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
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
                ('session_key', models.CharField(max_length=100, verbose_name='id numarası')),
                ('total', models.FloatField(default=0)),
                ('is_ordered', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Sepet',
                'verbose_name_plural': 'Sepetler',
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_item', to='bayi.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='product_item', to='bayi.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='bayi.productcategory', verbose_name='Ürün Kategorisi'),
        ),
    ]
