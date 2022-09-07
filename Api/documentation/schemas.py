from django.conf import settings
from django.conf.urls import include, url
from rest_framework import permissions

from Api.v1.routers import router as router_v1

from drf_yasg2.views import get_schema_view
from drf_yasg2 import openapi

api_url = '%s://api%s' % (settings.SITE_SCHEME, settings.PARENT_HOST)

if settings.HOST_PORT:
    api_url = '%s://api%s:%s' % (settings.SITE_SCHEME, settings.PARENT_HOST, settings.HOST_PORT)

schema_view_v1 = get_schema_view(
    openapi.Info(
        title="Documentation API",
        default_version='v1',
        description='API for v1',
    ),
    url=api_url,
    patterns=[url(r'^v1/', include((router_v1.urls, 'Api'), namespace='api-v1'))],
    public=True,
    permission_classes=(permissions.AllowAny,),
)
