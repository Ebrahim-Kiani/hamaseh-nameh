from django.http import HttpRequest
from django.shortcuts import render
from .models import Introduction

# Create your views here.

def view_for_download(request: HttpRequest):
    software_name = Introduction.objects.get(id=1).software_name
    software_description = Introduction.objects.get(id=1).software_description
    apk_download = Introduction.objects.get(id=1).apk_download
    logo = Introduction.objects.get(id=1).logo
    context = {
        'software_name': software_name,
        'software_description': software_description,
        'apk_download':apk_download,
        'logo': logo,
    }
    return render(request, 'production.html', context)