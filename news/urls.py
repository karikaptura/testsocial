from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_post, name='create_post'),
    path('', views.news_feed, name='news_feed'),
    path('toggle-like/<int:post_id>/', views.toggle_like, name='toggle_like'),
    path('add-comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
]
