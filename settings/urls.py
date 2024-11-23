from django.urls import path
from . import views
from .views import settings_page, remove_background

urlpatterns = [
    path('', views.settings_page, name='settings'),
    path('remove-background/', remove_background, name='remove_background'),
]
