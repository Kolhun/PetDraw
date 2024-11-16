from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseNotFound
from .forms import UserRegister
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .models import *
from django.shortcuts import render
import cv2
import numpy as np
import matplotlib.pyplot as plt
from .forms import ImageUploadForm
from io import BytesIO
import base64
import os


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


def generate_vertex_texture(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    img = cv2.GaussianBlur(img, (5, 5), 0)  # Убираем шумы
    img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)
    sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=5)
    sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=5)
    magnitude = np.sqrt(sobelx ** 2 + sobely ** 2)
    sobelx /= (magnitude + 1e-5)
    sobely /= (magnitude + 1e-5)
    normal_map = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    normal_map[..., 0] = ((sobelx + 1) * 127.5).astype(np.uint8)
    normal_map[..., 1] = ((sobely + 1) * 127.5).astype(np.uint8)
    normal_map[..., 2] = 255

    return img, normal_map


def vertex_texture_generator(request):
    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():

            image = form.cleaned_data['image']

            temp_dir = "temp"
            complete_dir = "temp_complete"

            os.makedirs(temp_dir, exist_ok=True)
            os.makedirs(complete_dir, exist_ok=True)

            img_path = os.path.join(temp_dir, image.name)

            with open(img_path, 'wb+') as temp_image:
                for chunk in image.chunks():
                    temp_image.write(chunk)

            original_image, vertex_texture = generate_vertex_texture(img_path)

            output_path = os.path.join(complete_dir, f"vertex_texture_{image.name}")
            plt.imsave(output_path, vertex_texture)

            buffer_original = BytesIO()
            plt.figure(figsize=(4, 4))
            plt.imshow(original_image, cmap='gray')
            plt.axis('off')
            plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
            plt.savefig(buffer_original, format="png", bbox_inches='tight', pad_inches=0)
            buffer_original.seek(0)
            original_png = buffer_original.getvalue()
            buffer_original.close()

            encoded_original_image = base64.b64encode(original_png).decode("utf-8")

            buffer_texture = BytesIO()
            plt.figure(figsize=(4, 4))
            plt.imshow(vertex_texture)
            plt.axis('off')
            plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
            plt.savefig(buffer_texture, format="png", bbox_inches='tight', pad_inches=0)
            buffer_texture.seek(0)
            texture_png = buffer_texture.getvalue()
            buffer_texture.close()

            encoded_texture_image = base64.b64encode(texture_png).decode("utf-8")

            os.remove(img_path)

            return render(request, "generator_header.html", {
                "form": form,
                "original_image_data": encoded_original_image,
                "texture_image_data": encoded_texture_image,
                "download_link": output_path,
            })

    else:
        form = ImageUploadForm()

    return render(request, "generator_header.html", {"form": form})

def generator(request):
    return render(request, 'generator_header.html')
def deletor(request):
    return render(request, 'deletor_in_image.html')

def pass_edit(request):
    info = {'error': '', 'message': ''}

    if request.method == 'POST':
        old_password = request.POST.get('old_password', '').strip()
        new_password = request.POST.get('new_password', '').strip()
        repeat_new_password = request.POST.get('repeat_new_password', '').strip()

        if not request.user.check_password(old_password):
            info['error'] = 'Старый пароль не верен'
        elif repeat_new_password != new_password:
            info['error'] = 'Новый повторный пароль должен совпадать с новым'
        elif not new_password:
            info['error'] = 'Новый пароль должен быть заполнен'
        elif not old_password:
            info['error'] = 'Старый пароль должен быть заполнен'
        else:
            user = request.user
            user.set_password(new_password)
            user.save()

            info['message'] = 'Пароль успешно изменён'
            update_session_auth_hash(request, user)

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
