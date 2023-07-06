
from django.contrib import admin
from django.urls import path, include
from allauth.account.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages', include('django.contrib.flatpages.urls')),
    path('news/', include('newapp.urls')),
    path('accounts/', include('allauth.urls')),
    path('accounts/logout/', LogoutView.as_view(), name='account_logout'),
    # path('accounts/login/', include('allauth.urls')), # пока не понятно нужно или нет
    # path('accounts/logout/', include('allauth.urls')), # пока не понятно нужно или нет
]
