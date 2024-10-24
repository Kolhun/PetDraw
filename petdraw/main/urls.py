from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout', views.log_out, name='logout'),
    path('login', views.log_in, name='login'),
    path('register', views.sign_up_by_html, name='register'),
    path('profile', views.profile, name='profile'),
    path('pass_edit', views.pass_edit, name='pass_edit'),

]
