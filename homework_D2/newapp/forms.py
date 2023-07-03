from django.forms import ModelForm, forms
from .models import Post, Comment

class NewsForm(ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'title', 'text']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['commentPost', 'commentUser', 'text']