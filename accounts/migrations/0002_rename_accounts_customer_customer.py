# Generated by Django 5.1.5 on 2025-01-20 23:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='accounts',
            new_name='customer',
        ),
    ]
