from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.privilege_user_list, name='privileged-user-list'),
    url(r'^add/$', views.privilege_user_add, name='privileged-user-add'),
    url(r'^(?P<privileged_user_id>[\w\W\-]+)/delete/$', views.privilege_user_delete, name='privileged-user-delete'),
    url(r'^(?P<privileged_user_id>[\w\W\-]+)/view/$', views.privilege_user_view, name='privileged-user-view'),
]