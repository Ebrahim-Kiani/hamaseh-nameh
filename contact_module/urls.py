from django.urls import path
from .views import CreateTicketAPIView, UserReplyAPIView, UserTicketListAPIView, UserMessagesAPIView

urlpatterns = [
    path('ticket/replys/<int:pk>', UserReplyAPIView.as_view(), name='user-messages'),  # User can see their messages
    path('ticket/create/', CreateTicketAPIView.as_view()),
    path('ticket/list/', UserTicketListAPIView.as_view()),
    path('messages/', UserMessagesAPIView.as_view()),

]