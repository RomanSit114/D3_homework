from django.urls import path
from .views import NewsListView, NewsDetailView, SearchListView

urlpatterns = [
    path('', NewsListView.as_view()),
    path('<int:pk>', NewsDetailView.as_view()),
    path('search/', SearchListView.as_view()),
    path('add/', SearchListView.as_view()),
]