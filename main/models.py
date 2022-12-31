from django.db import models
from django.db.models import DateTimeField
from django.contrib.auth.models import User

class DateTimeWithoutTZField(DateTimeField):
    def db_type(self, connection):
        return 'timestamp'

class Task(models.Model):

    CHOICE_CATEGORY = (
        ('Продукты', 'Продукты'),
        ('Проезд', 'Проезд'),
        ('Баловашки', 'Баловашки'), 
        ('Прочее', 'Прочее'),
    )

    CHOICE_BUDGET = (
        ('Алихан', 'Алихан'),
        ('Таня', 'Таня'),
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='owner', blank=True, null=True)

    money = models.CharField('Сумма', max_length=50, null=True)
    category = models.CharField('Категория', choices=CHOICE_CATEGORY, max_length=50, null=True, default='Продукты')
    budget = models.CharField('Бюджет', choices=CHOICE_BUDGET, max_length=50, default='Алихан')
    description = models.CharField('Описание', max_length=50, null=True, blank=True)
    date = models.DateTimeField('Дата')

    def __str__(self):
        return self.money

    class Meta:
        verbose_name = 'Column'
        verbose_name_plural = 'Columns'

class ExcelFile(models.Model):
    file = models.FileField(upload_to='excel')

