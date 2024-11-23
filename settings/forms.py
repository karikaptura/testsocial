from django import forms
from .models import UserSettings

class SettingsForm(forms.ModelForm):
    class Meta:
        model = UserSettings
        fields = ['color_scheme', 'background_image']
