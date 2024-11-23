from django.db import models
from django.conf import settings

class UserSettings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='settings')
    color_scheme = models.CharField(
        max_length=20,
        choices=[('light', 'Светлая'), ('dark', 'Тёмная')],
        default='light'
    )
    background_image = models.ImageField(upload_to='backgrounds/', blank=True, null=True)

    def __str__(self):
        return f"Настройки {self.user.username}"
