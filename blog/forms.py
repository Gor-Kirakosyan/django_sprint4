from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Category, Location, Comment

class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'image', 'pub_date', 'location', 'category']
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'text': forms.Textarea(attrs={'rows': 10}),
        }
        help_texts = {
            'pub_date': 'Если установить дату и время в будущем — можно делать отложенные публикации.',
            'image': 'Загрузите изображение для публикации (необязательно)',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Фильтруем только опубликованные категории
        self.fields['category'].queryset = Category.objects.filter(is_published=True)
        # Фильтруем только опубликованные местоположения
        self.fields['location'].queryset = Location.objects.filter(is_published=True)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
        }
        help_texts = {
            'text': 'Напишите ваш комментарий',
        }
