from django.shortcuts import render
from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import video, VideoCategory
from .seryalizers import VideosSerializer, VideoCategorySerializer


# Create your views here.

class MemoryListPagination(PageNumberPagination):
    page_size = 10


class VideosRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = VideosSerializer
    queryset = video.objects.none()  # Dummy queryset to satisfy the requirement

    def retrieve(self, request, *args, **kwargs):
        # Get the category ID from the URL path (e.g., /api/videos/<pk>/)
        category_id = self.kwargs.get('pk')

        if not category_id:
            raise NotFound(detail="Category ID is required to filter videos.")

        # Filter videos by the given category ID
        queryset = video.objects.filter(video_category_id=category_id)

        if not queryset.exists():
            raise NotFound(detail="No videos found for the provided category ID.")

        # Serialize the filtered queryset
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class videosCategoriesAPIListView(generics.ListAPIView):
    model = VideoCategory
    serializer_class = VideoCategorySerializer
    queryset = VideoCategory.objects.all()
    pagination_class = MemoryListPagination
