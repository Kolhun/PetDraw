from django.contrib import admin
from .models import Users


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'balance', 'age')
    search_fields = ('username',)

