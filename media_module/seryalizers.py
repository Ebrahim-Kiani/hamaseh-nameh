from rest_framework import serializers
from .models import video


class VideosSerializer(serializers.ModelSerializer):
    class Meta:
        model = video
        fields = '__all__'


class VideoCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = video
        fields = '__all__'
