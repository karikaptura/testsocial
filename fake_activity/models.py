# fake_activity/models.py
from django.db import models

class ActivityLog(models.Model):
    activity_type = models.CharField(max_length=50)  # Тип действия: "создание пользователей", "создание постов"
    details = models.TextField()  # Детали, например, количество созданных пользователей
    created_at = models.DateTimeField(auto_now_add=True)  # Время выполнения

    def __str__(self):
        return f"{self.activity_type} - {self.created_at}"
