# Generated by Django 5.1.5 on 2025-01-21 16:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telephone', models.CharField(max_length=11, verbose_name='Telefon')),
                ('address', models.CharField(max_length=100, verbose_name='Adres')),
                ('quantity', models.PositiveIntegerField(verbose_name='Aldığı ürün miktarı')),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Ödediği Tutar')),
                ('remain', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Kalan tutar')),
                ('is_loan', models.BooleanField(default=False, verbose_name='Borçlu ?')),
                ('date', models.DateField(verbose_name='Satın aldığı tarih')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Müşteri')),
            ],
            options={
                'verbose_name': 'Müşteri',
                'verbose_name_plural': 'Müşteriler',
                'ordering': ['-date'],
            },
        ),
    ]
