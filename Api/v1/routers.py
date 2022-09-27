from django.conf.urls import url
from rest_framework import routers
from Api.v1.Users.views import UserViewSet, UserAdminViewSet
from Api.v1.Jokes.views import JokeViewSet
from Api.v1.Jokes.api_views import JokeSendToEmailAPIView, JokeSendToTelegramAPIView

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'users-admin', UserAdminViewSet, basename='users-admin')
router.register(r'jokes', JokeViewSet, basename='jokes')

urlpatterns = router.urls

urlpatterns += [
    url(r'^joke-email-form/$', JokeSendToEmailAPIView.as_view(), name='send-joke-to-email-form'),
    url(r'^joke-telegram-form/$', JokeSendToTelegramAPIView.as_view(), name='send-joke-to-telegram-form'),
]
