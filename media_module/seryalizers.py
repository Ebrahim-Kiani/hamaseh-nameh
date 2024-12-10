from rest_framework import serializers
from .models import video, VideoCategory


class VideosSerializer(serializers.ModelSerializer):
    class Meta:
        model = video
        fields = '__all__'


class VideoCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoCategory
        fields = '__all__'
