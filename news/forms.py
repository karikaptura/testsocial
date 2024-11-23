from django import forms
from .models import Post
from .models import Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image', 'video']  # Укажите поля вашей модели
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Что у вас нового?'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']