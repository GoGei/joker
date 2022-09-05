from django.conf.urls import include, url

urlpatterns = [
    url('', include('urls')),
    url(r'^', include('Admin.Home.urls')),
]
