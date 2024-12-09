from django.shortcuts import render
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from .models import slide
from .seryalizers import SlidesSerializer
# Create your views here.

class MemoryListPagination(PageNumberPagination):
    page_size = 10

class slidesListAPIView(generics.ListAPIView):
    model = slide
    serializer_class = SlidesSerializer
    queryset = slide.objects.all()
