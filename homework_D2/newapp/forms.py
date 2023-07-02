from django.forms import ModelForm, forms
from .models import Post, Comment


# Создаём модельную форму
class NewsForm(forms.ModelForm):
    class Meta:
        model = Post
        # fields = ['author', 'title', 'dateCreation', 'text']
        fields = ['author', 'title', 'text']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['commentPost', 'commentUser', 'text']