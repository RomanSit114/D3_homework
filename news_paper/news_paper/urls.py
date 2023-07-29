
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from allauth.account.views import LogoutView
from django.contrib.auth import views as auth_views
from allauth.account import views as allauth_views

def redirect_to_news(request):
    return redirect('/news/')

urlpatterns = [
    path('', redirect_to_news),
    path('admin/', admin.site.urls),
    path('pages', include('django.contrib.flatpages.urls')),
    path('news/', include('newapp.urls')),
    path('accounts/', include('allauth.urls')),
    path('accounts/logout/', allauth_views.LogoutView.as_view(), name='logout'),
    path('accounts/login/', allauth_views.LoginView.as_view(), name='login'),
    path('accounts/signup/', allauth_views.SignupView.as_view(), name='signup'),
]
