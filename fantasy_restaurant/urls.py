from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.staticfiles.views import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/menu/', include('menu.api.urls')),
    path('api/pages/', include('pages.api.urls')),
    path('api/accounts/', include('accounts.api.urls')),
    # path('menu/', include('menu.urls')),
    # path('accounts/', include('accounts.urls')),
    # path('', include('pages.urls')),
    path('media/.*', serve, {'document_root': settings.MEDIA_ROOT,}),
    re_path('.*', TemplateView.as_view(template_name='index.html')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
