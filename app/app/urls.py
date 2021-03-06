from django.contrib import admin
from django.urls import path, include

from django.views.generic import TemplateView

from django.conf.urls.static import static
from django.conf import settings

from video.views import index, video, login

urlpatterns = [
    path('admin/', admin.site.urls),

    path("api-auth/", include("rest_framework.urls")),
    path("rest-auth/", include("rest_auth.urls")),
    path("rest-auth/registration/", include("rest_auth.registration.urls")),

    path("", index, name="index"),
    path('api/', include('video.api.urls')),
    path("videos/<slug>", video, name="video-view"),
    path("login/", login),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
