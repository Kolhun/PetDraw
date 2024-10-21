from django.db import models
from decimal import Decimal
from django.contrib.auth.models import AbstractBaseUser, Group, Permission, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, name, password=None, **extra_fields):
        if not name:
            raise ValueError('Users must have a name')
        user = self.model(name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(name, password, **extra_fields)


class Users(AbstractBaseUser, PermissionsMixin):
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

    # Обязательные поля для работы с AbstractBaseUser
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'name'  # Поле для логина (name вместо username)
    REQUIRED_FIELDS = ['age']  # Дополнительные обязательные поля при создании суперпользователя

    def __str__(self):
        return self.name
