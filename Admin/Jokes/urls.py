from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.jokes_list, name='jokes-list'),
    url(r'^top/$', views.jokes_top_list, name='jokes-top-list'),
    url(r'^add/$', views.jokes_add, name='jokes-add'),
    url(r'^(?P<joke_slug>[\w\W\-]+)/edit/$', views.jokes_edit, name='jokes-edit'),
    url(r'^(?P<joke_slug>[\w\W\-]+)/archive/$', views.jokes_archive, name='jokes-archive'),
    url(r'^(?P<joke_slug>[\w\W\-]+)/restore/$', views.jokes_restore, name='jokes-restore'),
    url(r'^(?P<joke_slug>[\w\W\-]+)/delete/$', views.jokes_delete, name='jokes-delete'),
    url(r'^(?P<joke_slug>[\w\W\-]+)/view/$', views.jokes_view, name='jokes-view'),
]