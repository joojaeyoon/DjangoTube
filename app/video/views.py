from django.shortcuts import render
from .models import Video


def index(request):
    context = {
        "videos": Video.objects.all()
    }

    return render(request, 'index.html', context)


def video(request, slug):

    context = {
        'video': Video.objects.filter(slug=slug)[0]
    }

    context["video"].view_count += 1

    context["video"].save()

    return render(request, 'video.html', context)
