from django.shortcuts import render
from .models import Video


def videos(request):
    context = {
        "videos": Video.objects.all()
    }

    return render(request, 'index.html', context)
