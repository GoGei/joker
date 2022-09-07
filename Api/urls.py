from django.conf.urls import include, url


urlpatterns = [
    url('', include('urls')),
    url(r'^v1/', include('Api.v1.routers'), name='api-v1'),
]