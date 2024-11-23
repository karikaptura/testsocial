from django.urls import path
from . import views

urlpatterns = [
    path('', views.conversation_list, name='conversation_list'),  # Список диалогов
    path('<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),  # Просмотр диалога
    path('<int:conversation_id>/send/', views.send_message, name='send_message'),  # Отправка сообщения
    path('start/<int:user_id>/', views.start_conversation, name='start_conversation'),  # Начало нового диалога
    path('<int:conversation_id>/fetch/', views.fetch_new_messages, name='fetch_new_messages'),  # Fetch новых сообщений
]
