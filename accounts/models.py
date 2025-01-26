from django.db import models


class Customer(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='Müşteri')
    telephone = models.CharField(max_length=11, verbose_name='Telefon')
    address = models.CharField(max_length=100, verbose_name='Adres')
    is_loan = models.BooleanField(default=False, verbose_name='Borçlu ?')
    bought = models.PositiveIntegerField(default=0, verbose_name='Toplam satın aldığı ürün adeti')
    total_loan = models.FloatField(verbose_name='Toplam Borç', default=0)
    total_pay = models.FloatField(verbose_name='Toplam Harcamalar', default=0)
    date = models.DateField(verbose_name='Katılma Tarihi', auto_now_add=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Müşteriler'
        verbose_name = 'Müşteri'

    def save(self, *args, **kwargs):
        if self.total_loan == 0:
            self.is_loan = False
        return super().save(*args, **kwargs)


class OrderModel(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Müşteri', related_name='orders')
    product = models.ManyToManyField('bayi.Product', verbose_name='Ürün Adı', related_name='products')
    order_number = models.UUIDField(unique=True, db_index=True, verbose_name='Sipariş Numarası')

    quantity = models.PositiveIntegerField(verbose_name='Aldığı ürün miktarı', default=0)
    cost = models.FloatField(verbose_name='Ödeme Girişi', default=0, null=True, blank=True)
    total = models.FloatField(verbose_name='Kalan tutar', default=0)
    remain = models.FloatField(verbose_name='Kalan tutar', default=0)

    order_date = models.DateTimeField(verbose_name='Sipariş Tarihi', auto_now_add=True)
    last_date = models.DateField(verbose_name='Son Ödeme Tarihi', blank=True, null=True)

    def __str__(self):
        return self.order_number.__str__() + ' - ' + self.customer.user.username

    class Meta:
        ordering = ['-order_date']
        verbose_name = 'Sipariş'
        verbose_name_plural = 'Siparişler'



