from django.shortcuts import render
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from .models import video, VideoCategory
from .seryalizers import VideosSerializer, VideoCategorySerializer


# Create your views here.

class MemoryListPagination(PageNumberPagination):
    page_size = 10


class videosListAPIView(generics.ListAPIView):
    model = video
    serializer_class = VideosSerializer
    queryset = video.objects.all()
    pagination_class = MemoryListPagination


class videosCategoriesAPIListView(generics.ListAPIView):
    model = VideoCategory
    serializer_class = VideoCategorySerializer
    queryset = VideoCategory.objects.all()
    pagination_class = MemoryListPagination
