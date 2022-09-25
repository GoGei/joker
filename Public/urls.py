from django.conf.urls import include, url

urlpatterns = [
    url('', include('urls')),
    url(r'^', include('Public.Login.urls')),
    url(r'^', include('Public.Home.urls')),
    url(r'^registration/', include('Public.Registration.urls')),
]
