from django.conf.urls import url
from . import views

urlpatterns = [
    url('^login/$', views.login_view, name='admin-login'),
    url('^logout/$', views.logout_view, name='admin-logout')
]
