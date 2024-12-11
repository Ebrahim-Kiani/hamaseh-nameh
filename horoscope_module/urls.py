from django.urls import path
from .views import RandomHoroscopeAPIView
urlpatterns = [
    path('random/', RandomHoroscopeAPIView.as_view())
]