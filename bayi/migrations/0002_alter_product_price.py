# Generated by Django 5.1.5 on 2025-01-21 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bayi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Birim Fiyat'),
        ),
    ]
