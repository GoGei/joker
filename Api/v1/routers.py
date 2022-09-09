from rest_framework import routers
from Api.v1.Users.views import UserViewSet, UserAdminViewSet
from Api.v1.Jokes.views import JokeViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'users-admin', UserAdminViewSet, basename='users-admin')
router.register(r'jokes', JokeViewSet, basename='jokes')

urlpatterns = [

]

urlpatterns += router.urls
