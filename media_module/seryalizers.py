from rest_framework import serializers
from .models import video, VideoCategory


class VideosSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = video
        fields = ['id', 'title', 'video_link', 'image', 'video_category']

    def get_image(self, obj):
        request = self.context.get('request')  # Access the request from the serializer context
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None


class VideoCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoCategory
        fields = '__all__'
