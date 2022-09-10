from django.conf.urls import url
from . import views

urlpatterns = [
    url('^$', views.home_view, name='home-index'),
    url('^all-jokes/$', views.home_all_jokes_view, name='home-all-jokes'),
    url('^top-jokes/$', views.home_top_jokes_view, name='home-top-jokes'),
    url('^liked/$', views.home_liked_views, name='home-liked-jokes'),
]
