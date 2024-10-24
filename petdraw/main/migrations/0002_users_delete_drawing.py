# Generated by Django 5.1.2 on 2024-10-21 07:58

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='Имя покупателя')),
                ('balance', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10, verbose_name='Баланс')),
                ('age', models.PositiveIntegerField(verbose_name='Возраст')),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, related_name='default', to='auth.group', verbose_name='группы')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='default', to='auth.permission', verbose_name='разрешения')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='Drawing',
        ),
    ]
