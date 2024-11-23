from django.urls import path
from .views import register_user, login_user, logout_user

urlpatterns = [
    path('register/', register_user, name='register'),  # Исправлено на register_user
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
]
