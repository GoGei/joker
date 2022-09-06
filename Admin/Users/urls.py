from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.users_list, name='users-list'),
    url(r'^(?P<user_pk>\d+)/view/$', views.users_view, name='users-view'),
]
