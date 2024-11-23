from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser
from django.contrib.auth.models import User

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=30, required=False, label="Имя")
    last_name = forms.CharField(max_length=30, required=False, label="Фамилия")

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
