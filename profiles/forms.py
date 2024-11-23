# profiles/forms.py
from django import forms
from .models import Profile
from .models import ProfileMedia

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'birth_date', 'location', 'interests']



class ProfileMediaForm(forms.ModelForm):
    class Meta:
        model = ProfileMedia
        fields = ['file']  # Это поле должно соответствовать полю модели

