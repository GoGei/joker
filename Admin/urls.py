from django.conf.urls import include, url

urlpatterns = [
    url('', include('urls')),
    url(r'^', include('Admin.Home.urls')),
    url(r'^', include('Admin.Login.urls')),
    url(r'^jokes/', include('Admin.Jokes.urls')),
]
