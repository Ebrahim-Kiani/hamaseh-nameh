from rest_framework import serializers
from .models import ContactUs, UserMessages


class TicketCreateSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ContactUs
        fields = ['id', 'title', 'description', 'user', ]


class TicketListSerializer(serializers.ModelSerializer):

    is_awnsered = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ContactUs
        fields = ['id', 'title', 'description', 'is_awnsered']


class ReplySerializer(serializers.ModelSerializer):
    admin_awnser = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ContactUs
        fields = ['admin_awnser']


class UserMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMessages
        exclude = ['id', 'user']
