from django.conf.urls import url
from . import views
from .PrivilegeMessages.urls import urlpatterns as message_urls

urlpatterns = [
    url(r'^$', views.privilege_user_list, name='privileged-user-list'),
    url(r'^add/$', views.privilege_user_add, name='privileged-user-add'),
    url(r'^(?P<privileged_user_id>\d+)/delete/$', views.privilege_user_delete, name='privileged-user-delete'),
    url(r'^(?P<privileged_user_id>\d+)/view/$', views.privilege_user_view, name='privileged-user-view'),
]

urlpatterns += message_urls
