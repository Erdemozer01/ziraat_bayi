# Generated by Django 5.1.5 on 2025-01-29 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('bayi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordermodel',
            name='product',
            field=models.ManyToManyField(related_name='products', to='bayi.product', verbose_name='Ürün Adı'),
        ),
    ]
