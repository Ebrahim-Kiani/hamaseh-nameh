from rest_framework import generics, permissions
from rest_framework.response import Response

from .models import ContactUs , UserMessages
from .seryalizers import TicketCreateSerializer, UserMessagesSerializer ,ReplySerializer, TicketListSerializer


class CreateTicketAPIView(generics.CreateAPIView):
    queryset = ContactUs.objects.all()
    serializer_class = TicketCreateSerializer
    permission_classes = [permissions.IsAuthenticated]  # Ensure user is authenticated

    def perform_create(self, serializer):
        # Set the user field automatically from the authenticated user
        serializer.save(user=self.request.user)


class UserTicketListAPIView(generics.ListAPIView):
    serializer_class = TicketListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter the messages for the logged-in user
        return ContactUs.objects.filter(user=self.request.user, is_awnsered=True, admin_awnser__isnull=False)


class UserReplyAPIView(generics.RetrieveAPIView):
    serializer_class = ReplySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter the messages for the logged-in user
        return ContactUs.objects.filter(user=self.request.user, is_awnsered=True, admin_awnser__isnull=False)


class UserMessagesAPIView(generics.ListAPIView):
    serializer_class = UserMessagesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter the messages for the logged-in user
        return UserMessages.objects.filter(user=self.request.user)
