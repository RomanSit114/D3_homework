import django_filters
from django_filters import FilterSet
from .models import Post

class NewsFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'dateCreation': ['gte'],
            'author': ['exact'],
            'text': ['icontains'],
        }