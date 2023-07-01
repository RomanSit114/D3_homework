from django.forms import ModelForm
from .models import Post


# Создаём модельную форму
class NewsForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'dateCreation', 'text']