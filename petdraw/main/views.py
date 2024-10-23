from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseNotFound
from .forms import UserRegister
from django.contrib.auth import authenticate, login, logout
from .models import *


def home(request):
    return render(request, 'home.html')


def index(request):
    users = Users.objects.all()
    context = {
        "Users": users,
    }
    return render(request, 'four_task/index.html', context)


def sign_up_by_html(request):
    info = {}
    message = ""

    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            name = request.POST.get('name', '').strip()
            username = request.POST.get('username', '').strip()
            password = request.POST.get('password', '').strip()
            repeat_password = request.POST.get('repeat_password', '').strip()
            age = request.POST.get('age', '').strip()

            if not name or len(name) > 30:
                info['error'] = 'Некорректный логин'
            elif not password or len(password) < 8:
                info['error'] = 'Пароль должен содержать не менее 8 символов'
            elif password != repeat_password:
                info['error'] = 'Пароли не совпадают'
            elif not age.isdigit() or int(age) < 18:
                info['error'] = 'Вы должны быть старше 18 лет'
            elif Users.objects.filter(username=username).exists():
                info['error'] = 'Пользователь с таким именем уже существует'
            else:

                user = Users(username=username, name=name, age=age, balance=10)
                user.set_password(password)
                user.save()

                message = f"Приветствуем, {name}! Регистрация успешно завершена."

                user = authenticate(request, username=username, password=password)
                print(f"user registration {user}, name {username}, password {password},")
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    info['error'] = 'Ошибка при аутентификации'
    else:
        form = UserRegister()

    info['form'] = form
    if message:
        info['message'] = message
    return render(request, 'registration.html', context=info)

def pass_edit(request):
    info = {}
    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            old_password = request.POST.get('old_password', '').strip()
            new_password = request.POST.get('new_password', '').strip()
            repeat_new_password = request.POST.get('password', '').strip()

            if not request.user.check_password(old_password):
                info['error'] = 'Старый пароль не верен'
            elif repeat_new_password != new_password:
                info['error'] = 'Новый повторный пароль должен совпадать с новым'
            elif not new_password:
                info['error'] = 'Новый пароль должен быть заполнен'
            elif not old_password:
                info['error'] = 'Старый пароль должен быть заполнен'
            else:
                info['message'] = 'Пароль успешно изменён'

                user = request.user
                user.set_password(new_password)
                user.save()

    return render(request, 'pass_edit.html', context=info)

def log_in(request):
    error = None
    if request.method == 'POST':
        username = request.POST['username'].strip()
        password = request.POST['password'].strip()

        user = authenticate(request, username=username, password=password)

        print(f"user login {user}, name {username}, password {password}")

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error = "Неверное имя пользователя или пароль"

    return render(request, 'login.html', {'error': error})


def profile(request):
    return render(request, 'profile.html')


def log_out(request):
    logout(request)
    return render(request, 'logout.html')


def return_to_home(request):
    return redirect('/main')
