from django.conf.urls import url
from . import views

urlpatterns = [
    url('^$', views.admin_home_view, name='admin-home')
]
