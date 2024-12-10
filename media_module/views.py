from django.shortcuts import render
from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import video, VideoCategory
from .seryalizers import VideosSerializer, VideoCategorySerializer


# Create your views here.

class MemoryListPagination(PageNumberPagination):
    page_size = 10  # Number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 50  # Optional: limit the max page size


class VideosListAPIView(APIView):
    serializer_class = VideosSerializer
    pagination_class = MemoryListPagination

    def get(self, request, pk, *args, **kwargs):
        category_id = pk

        if not category_id:
            raise NotFound(detail="Category ID is required to filter videos.")

        queryset = video.objects.filter(video_category_id=category_id)

        if not queryset.exists():
            raise NotFound(detail="No videos found for the provided category ID.")

        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        serializer = VideosSerializer(paginated_queryset, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)



class videosCategoriesAPIListView(generics.ListAPIView):
    model = VideoCategory
    serializer_class = VideoCategorySerializer
    queryset = VideoCategory.objects.all()
    pagination_class = MemoryListPagination
