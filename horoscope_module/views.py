import random

from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Horoscope
from .seryalizers import HoroscopeSerializer


class RandomHoroscopeAPIView(APIView):
    def get(self, request, *args, **kwargs):
        count = Horoscope.objects.aggregate(count=Count('id'))['count']
        if count == 0:
            return Response({"error": "No horoscopes available."}, status=404)

        # Use the database to fetch a random row
        random_index = random.randint(0, count - 1)
        random_horoscope = Horoscope.objects.all()[random_index]

        serializer = HoroscopeSerializer(random_horoscope)
        return Response(serializer.data)
