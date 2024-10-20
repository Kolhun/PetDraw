
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', include('main.urls')),
    path('', views.redirect_to_home, name='redirect_to_home'),
]
