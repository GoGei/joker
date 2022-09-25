from django.conf.urls import url
from . import views

urlpatterns = [
    url('^$', views.register_view, name='home-register'),
    url('^resend/$', views.register_resend_view, name='home-register-resend'),
    url('^activate/(?P<user_pk>\d+)/(?P<code>[\w\W]+)/$', views.register_activate_view,
        name='home-register-activate')
]
