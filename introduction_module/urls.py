from django.urls import path
from .views import view_for_download
urlpatterns = [
    path('view/', view_for_download )
]