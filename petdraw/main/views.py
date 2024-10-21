
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseNotFound
from .forms import UserRegister
from django.contrib.auth import authenticate, login, logout
from .models import *


def home(request):
    return render(request, 'home.html')



def index(request):
    byers = Users.objects.all()
    context = {
        "Users": byers,
    }
    return render(request, 'four_task/index.html', context)


def sign_up_by_html(request):
    info = {}
    message = ""

    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            name = request.POST.get('name', '').strip()
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
            elif Users.objects.filter(name=name).exists():
                info['error'] = 'Пользователь с таким именем уже существует'
            else:
                # Создание пользователя
                user = Users(name=name, age=age, balance=10)
                user.set_password(password)  # Устанавливаем хешированный пароль
                user.save()

                message = f"Приветствуем, {name}! Регистрация успешно завершена."

                # Аутентификация пользователя по оригинальному паролю
                user = authenticate(request, username=name, password=password)
                print(f"user registration {user}, name {name}, password {password},")
                if user is not None:
                    login(request, user)  # Вход пользователя в систему
                    return redirect('home')  # Перенаправление на главную страницу
                else:
                    info['error'] = 'Ошибка при аутентификации'
    else:
        form = UserRegister()

    info['form'] = form
    if message:
        info['message'] = message
    return render(request, 'registration.html', context=info)
def log_in(request):
    error = None
    if request.method == 'POST':
        username = request.POST['name'].strip()
        password = request.POST['password'].strip()

        # Аутентификация пользователя
        user = authenticate(request, username=username, password=password)

        print(f"user login {user}, name {username}, password {password}")

        if user is not None:
            login(request, user)  # Вход пользователя
            return redirect('home')  # Перенаправление на главную страницу
        else:
            error = "Неверное имя пользователя или пароль"

    return render(request, 'login.html', {'error': error})

def log_out(request):
    logout(request)
    return redirect('/main')

def return_to_home(request):
    return redirect('/main')