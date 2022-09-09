from django.conf.urls import url
from . import views

BASE_ULR_PATTERN = r'^(?P<privilege_user_id>\d+)/messages/'

urlpatterns = [
    url(BASE_ULR_PATTERN + r'$', views.privilege_message_list, name='privilege-message-list'),
    url(BASE_ULR_PATTERN + r'add/$', views.privilege_message_add, name='privilege-message-add'),
    url(BASE_ULR_PATTERN + r'(?P<message_id>\d+)/edit/$', views.privilege_message_edit, name='privilege-message-edit'),
    url(BASE_ULR_PATTERN + r'(?P<message_id>\d+)/delete/$', views.privilege_message_delete,
        name='privilege-message-delete'),
    url(BASE_ULR_PATTERN + r'(?P<message_id>\d+)/view/$', views.privilege_message_view, name='privilege-message-view'),
]
