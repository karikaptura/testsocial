from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('users/', include('users.urls')),
    path('profiles/', include('profiles.urls')),
    path('messages/', include('messages_app.urls')),
    path('news/', include('news.urls')),
    path('settings/', include('settings.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

