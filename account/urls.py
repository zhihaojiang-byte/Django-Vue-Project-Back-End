from django.urls import path
from account import views

urlpatterns = [
    path('login', views.user_login),
    path('logout', views.user_logout),
    path('info', views.UserInfo.as_view()),
    path('register', views.UserRegister.as_view()),
]
