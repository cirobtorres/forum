from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from django.urls import include, path

urlpatterns = [
    path(route='admin/', view=admin.site.urls),
    path(route='', view=include('apps.forum.urls')),
    path(route='', view=include('apps.account.urls')),
    # path(route='', view=include('apps.tag.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)