from django.db import models
from decimal import Decimal
from django.contrib.auth.models import AbstractBaseUser, Group, Permission, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, username, name, password=None, **extra_fields):
        user = self.model(username=username, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, name, password, **extra_fields)


class Users(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True, verbose_name="Логин", default="")
    name = models.CharField(max_length=25, verbose_name="Имя", default="")
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

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username
