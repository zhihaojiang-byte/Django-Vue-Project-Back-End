from django.urls import path
from order import views

urlpatterns = [
    path('order/submit', views.TicketOrderSubmitView.as_view()),
    path('order/detail/<int:sn>', views.OrderDetail.as_view()),
    path('order/list', views.OrderListView.as_view()),
]
