from django.db import models

class Customer(models.Model):
    customer = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='Müşteri')
    telephone = models.CharField(max_length=11, verbose_name='Telefon')
    address = models.CharField(max_length=100, verbose_name='Adres')
    quantity = models.PositiveIntegerField(verbose_name='Aldığı ürün miktarı')
    cost = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Ödediği Tutar')
    remain = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Kalan tutar')
    is_loan = models.BooleanField(default=False, verbose_name='Borçlu ?')
    date = models.DateField(verbose_name='Satın aldığı tarih')

    def __str__(self):
        return self.customer.username

    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Müşteriler'
        verbose_name = 'Müşteri'
