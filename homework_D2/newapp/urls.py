from django.urls import path
from .views import NewsList, NewsDetail, SearchList

urlpatterns = [
    path('', NewsList.as_view()),
    path('<int:pk>', NewsDetail.as_view()),
    path('search/', SearchList.as_view()),
]