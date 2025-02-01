# Generated by Django 5.1.5 on 2025-02-01 04:42

import django.db.models.deletion
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
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='bayi.product', verbose_name='Ürün Adı'),
        ),
    ]
