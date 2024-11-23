from django.urls import path
from . import views

urlpatterns = [
    path('add_photo/', views.add_photo, name='add_photo'),
    path('add_video/', views.add_video, name='add_video'),


    path('<str:username>/gallery/', views.media_gallery, name='media_gallery'),
    path('friends/', views.friends_list, name='friends_list'),  # Страница друзей
    path('<str:username>/', views.view_profile, name='view_profile'),
    path('<str:username>/edit/', views.edit_profile, name='edit_profile'),
    path('<int:user_id>/send_request/', views.send_friend_request, name='send_friend_request'),
    path('requests/<int:request_id>/<str:response>/', views.respond_to_friend_request, name='respond_to_friend_request'),
    path('<int:user_id>/remove_friend/', views.remove_friend, name='remove_friend'),
    path('<str:username>/upload-media/', views.upload_media, name='upload_media'),
]
