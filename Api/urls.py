from django.conf import settings
from django.conf.urls import include, url
from Api.documentation.urls import urlpatterns as doc_urlpatterns

urlpatterns = [
    url('', include('urls')),
    url(r'^v1/', include('Api.v1.routers'), name='api-v1'),
]

if settings.API_DOCUMENTATION:
    urlpatterns += doc_urlpatterns
