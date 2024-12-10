from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.videosListAPIView.as_view(), name="videos-list"),
    path('categories/', views.videosCategoriesAPIListView.as_view(), name='videos-categories')
]