# Generated by Django 5.1.5 on 2025-01-27 02:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bayi', '0003_settingssite_card_alter_settingssite_favicon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='settingssite',
            name='card',
        ),
    ]
