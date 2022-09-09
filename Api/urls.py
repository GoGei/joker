from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static

from Api.v1.routers import router as router_v1
from Api.documentation.urls import urlpatterns as doc_urlpatterns

urlpatterns = [
    url(r'^', include('urls')),
    url(r'^', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^v1/', include((router_v1.urls, 'api'), namespace='api-v1')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.API_DOCUMENTATION:
    urlpatterns += doc_urlpatterns
