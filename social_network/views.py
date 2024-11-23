from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def home(request):
    if request.user.is_authenticated:
        # Если пользователь авторизован, показываем главную страницу
        return render(request, 'home.html')
    else:
        # Если пользователь не авторизован, показываем страницу приветствия
        return render(request, 'welcome.html')
