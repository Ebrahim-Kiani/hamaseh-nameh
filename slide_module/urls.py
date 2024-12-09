from django.urls import path, include
from . import views


urlpatterns = [
    path('list/', views.slidesListAPIView.as_view(), name='slides-list')
]