from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    friends = models.ManyToManyField('self', blank=True)  # Связь "друзья"
    birth_date = models.DateField(blank=True, null=True)  # Дата рождения
    location = models.CharField(max_length=100, blank=True, null=True)  # Местоположение
    interests = models.TextField(blank=True, null=True)  # Интересы

    def __str__(self):
        return self.user.username


class FriendRequest(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='friend_requests_sent'
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='friend_requests_received'
    )
    status = models.CharField(
        max_length=10,
        choices=(('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined')),
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username} ({self.status})"



# profiles/models.py

class ProfileMediaQuerySet(models.QuerySet):
    def images(self):
        return self.filter(media_type='image')

    def videos(self):
        return self.filter(media_type='video')


class ProfileMedia(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile_media')
    media_file = models.FileField(upload_to='profile_media/')
    media_type = models.CharField(max_length=10, choices=[('image', 'Image'), ('video', 'Video')])
    created_at = models.DateTimeField(auto_now_add=True)
    
class Media(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='media_items')
    file = models.FileField(upload_to='profile_media/')
    media_type = models.CharField(max_length=10, choices=[('image', 'Image'), ('video', 'Video')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.media_type} for {self.profile.user.username}"