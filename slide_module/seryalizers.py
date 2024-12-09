from django.db.models import Avg
from rest_framework import serializers
from .models import slide
from account_module.models import Address


class SlidesSerializer(serializers.ModelSerializer):

    class Meta:
        model = slide
        fields = '__all__'

