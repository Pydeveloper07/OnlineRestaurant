from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/menu/', include('menu.api.urls')),
    path('api/pages/', include('pages.api.urls')),
    path('menu/', include('menu.urls')),
    path('accounts/', include('accounts.urls')),
    path('', include('pages.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
