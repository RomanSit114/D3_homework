from django.urls import path

from . import views
from .views import NewsListView, NewsDetailView, SearchListView, NewsCreateView, NewsUpdateView, NewsDeleteView, i_am_author

urlpatterns = [
    path('', NewsListView.as_view(), name='main_page'),
    path('<int:pk>', NewsDetailView.as_view(), name='new'),
    path('search/', SearchListView.as_view()),
    path('add/', NewsCreateView.as_view(), name='news-create'),
    path('<int:pk>/edit/', NewsUpdateView.as_view(), name='news-update'),
    path('<int:pk>/delete/', NewsDeleteView.as_view(), name='news-delete'),
    path('be_author/', i_am_author, name = 'be_author')
]