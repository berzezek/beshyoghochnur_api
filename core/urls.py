from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

# settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('grappelli/', include('grappelli.urls')),
    path('api/v1/', include('catalog.api.urls')),
]

if settings:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
