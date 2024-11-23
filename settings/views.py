from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import SettingsForm
from .models import UserSettings
from django.contrib import messages

@login_required
def settings_page(request):
    user_settings, created = UserSettings.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = SettingsForm(request.POST, request.FILES, instance=user_settings)
        if form.is_valid():
            form.save()
            return redirect('settings')
    else:
        form = SettingsForm(instance=user_settings)
    return render(request, 'settings/settings.html', {'form': form, 'settings': user_settings})

@login_required
def remove_background(request):
    user_settings = request.user.settings
    user_settings.background_image.delete(save=False)  # Удаляем файл
    user_settings.background_image = None  # Сбрасываем поле
    user_settings.save()
    messages.success(request, 'Фоновое изображение удалено.')
    return redirect('settings')  # Перенаправляем на страницу настроек