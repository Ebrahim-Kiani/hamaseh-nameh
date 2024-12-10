from django.urls import path, include, re_path
from . import views
from rest_framework.routers import DefaultRouter


memory_user_router = DefaultRouter()
memory_user_router.register('info', views.memoryUserAPIView, basename='memory-info')
memory_user_router.register('pictures', views.memoryPicturesAPIView, basename='memory-pictures')



urlpatterns = [
    path('counties/', views.CountyListAPIView.as_view(), name='county-list'),
    path('user/', include(memory_user_router.urls)),
    path('user/', include(memory_user_router.urls)),
    path('list/', views.memoryListAPIView.as_view(), name='memory-list'),
    path('detail/<int:pk>', views.memoryRetrieveAPIView.as_view(), name='memory-detail'),
    path('list/topten/', views.TopRatedMemoriesAPIView.as_view() , name='topten_memories'),


    path('comment/create/', views.memoryCommentsCreateAPIView.as_view(), name='memory-comments-create'),
    path('comment/edit/<int:pk>', views.memoryCommentsEditAPIView.as_view(), name='memory-comments-edit'),
    path('rating/', views.RatingCreateAPIView.as_view(), name='memory-rating-create'),



    path('bookmarks/', views.BookmarkListCreateAPIView.as_view(), name='bookmark-list'),
    path('bookmarks/delete/<int:pk>/', views.BookMarkDestroyAPIView.as_view(), name='bookmark-delete'),

    path('budget/', views.UserPointsAPIView.as_view())


]