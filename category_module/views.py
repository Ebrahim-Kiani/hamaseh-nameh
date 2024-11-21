from django_filters.rest_framework import DjangoFilterBackend
from .models import MainCategory, SubCategory
from rest_framework import generics
from .seryalizers import MainCategorySerializer, SubCategorySerializer


# Reverse List of MainCategories.
class MainCategoryListAPIView(generics.ListAPIView):
    queryset = MainCategory.objects.all()
    serializer_class = MainCategorySerializer


# Reverse List of SubCategories by getting there MainCategory ID.
class SubCategoryListAPIView(generics.ListAPIView):
    serializer_class = SubCategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['MainCategory__title']
    queryset = SubCategory.objects.all()

