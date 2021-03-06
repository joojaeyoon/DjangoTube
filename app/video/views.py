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


def login(request):

    return render(request, 'login.html')


def handle_uploaded_file(f):
    with open(settings.MEDIA_ROOT+'videos/name.mp4', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
