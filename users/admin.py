from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Настраиваем отображение полей в админке
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('bio', 'avatar')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('bio', 'avatar')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
