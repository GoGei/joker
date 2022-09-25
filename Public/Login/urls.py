from django.conf.urls import url
from . import views

urlpatterns = [
    url('^login/$', views.login_view, name='home-login'),
    url('^logout/$', views.logout_view, name='home-logout'),
    url('^register/$', views.register_view, name='home-register'),
    url('^register-resend/$', views.register_resend_view, name='home-register-resend'),
    url('^register-activate/(?P<user_pk>\d+)/(?P<code>[\w\W]+)/$', views.register_activate_view,
        name='home-register-activate')
]
