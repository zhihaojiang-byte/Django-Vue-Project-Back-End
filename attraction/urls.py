from django.urls import path
from attraction import views

urlpatterns = [
    path('attraction/list', views.AttractionList.as_view()),
    path('attraction/detail/<int:pk>', views.AttractionDetail.as_view()),
    path('attraction/images/<int:pk>', views.AttractionImages.as_view()),
    path('comment/list/<int:pk>', views.CommentList.as_view()),
    path('comment/post', views.PostCommentView.as_view()),
    path('ticket/list/<int:pk>', views.TicketList.as_view()),
    path('attraction/info/<int:pk>', views.AttractionInfoView.as_view()),
    path('ticket/detail/<int:pk>', views.TicketDetailView.as_view()),
    path('ticket/info/<int:pk>', views.TicketInfoView.as_view()),
]
