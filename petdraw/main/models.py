from django.db import models
from decimal import Decimal
from django.contrib.auth.models import AbstractBaseUser, Group, Permission


class Users(AbstractBaseUser):
    name = models.CharField(max_length=150, unique=True, verbose_name="Имя покупателя")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), verbose_name="Баланс")
    age = models.PositiveIntegerField(verbose_name="Возраст")


    groups = models.ManyToManyField(
        Group,
        related_name='default',
        blank=True,
        verbose_name='группы'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='default',
        blank=True,
        verbose_name='разрешения'
    )

    def __str__(self):
        return self.name
