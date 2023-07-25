from datetime import date
from django.db import models
from django.core.validators import MinLengthValidator


class CreditCard(models.Model):
    number = models.CharField('number', max_length=255, unique=True, db_index=True)
    exp_date = models.DateField('exp_date', format='%Y-%m-%d')
    holder = models.CharField('holder', max_length=30, validators=[MinLengthValidator(3)])
    cvv = models.CharField('cvv', max_length=4, blank=True, null=True)
    brand = models.CharField('brand', max_length=10)

    class Meta:
        verbose_name = 'Credit Card'
        verbose_name_plural = 'Credita Cards'

    def __str__(self) -> str:
        valid = 'valid'
        if self.exp_date > date.today():
            valid = 'expired'
        return f'{self.holder} {self.brand} - {valid}'
    
