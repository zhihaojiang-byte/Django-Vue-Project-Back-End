from django.urls import path
from system import views

urlpatterns = [
    path('swipe/list', views.slider_list),
    path('send/verification', views.SendVerificationCode.as_view()),
]

