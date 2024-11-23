from django.contrib import admin
from .models import ActivityLog
from .utils import create_fake_users_and_posts

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('activity_type', 'details', 'created_at')

# Добавляем кнопку в админке
def generate_fake_data(modeladmin, request, queryset):
    created_users = create_fake_users_and_posts()
    ActivityLog.objects.create(
        activity_type="Создание пользователей и постов",
        details=f"Создано {len(created_users)} пользователей с постами."
    )
    modeladmin.message_user(request, f"Создано {len(created_users)} пользователей с постами.")

generate_fake_data.short_description = "Создать фейковых пользователей и посты"

admin.site.add_action(generate_fake_data)
