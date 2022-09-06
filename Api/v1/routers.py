from rest_framework import routers
from Api.v1.Users.views import UserViewSet, UserAdminViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'users-admin', UserAdminViewSet, basename='users-admin')
urlpatterns = [

]

urlpatterns += router.urls
