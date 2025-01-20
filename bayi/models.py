from django.db import models


# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Ürün Adı')
    quantity = models.PositiveIntegerField(verbose_name='Ürün Miktarı')
    price = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return self.name
