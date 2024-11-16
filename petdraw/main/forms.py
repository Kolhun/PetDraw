# task5_legacy/forms.py

from django import forms

class ImageUploadForm(forms.Form):
    image = forms.ImageField(label="Выберите изображение для обработки")

class UserRegister(forms.Form):
    username = forms.CharField(
        label="Введите логин",
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Логин'})
    )
    name = forms.CharField(
        label="Введите отображаемое имя",
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Имя'})
    )
    password = forms.CharField(
        label="Введите пароль",
        min_length=8,
        widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'})
    )
    repeat_password = forms.CharField(
        label="Повторите пароль",
        min_length=8,
        widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'})
    )
    age = forms.IntegerField(
        label="Введите свой возраст",
        min_value=0,
        max_value=999,
        widget=forms.NumberInput(attrs={'placeholder': 'Возраст'})
    )
