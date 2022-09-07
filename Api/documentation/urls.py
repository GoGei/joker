from django.conf.urls import url
from .schemas import schema_view_v1

urlpatterns = []
schemas = (schema_view_v1,)
for counter, schema in enumerate(schemas, start=1):
    urlpatterns += [
        url(r'^v{i}/swagger(?P<format>\.json|\.yaml)$'.format(i=counter), schema.without_ui(cache_timeout=0),
            name=f'schema-json-{counter}'),
        url(r'^v{i}/swagger/$'.format(i=counter), schema.with_ui('swagger', cache_timeout=0),
            name=f'schema-swagger-ui-{counter}'),
        url(r'^v{i}/redoc/$'.format(i=counter), schema.with_ui('redoc', cache_timeout=0),
            name=f'schema-redoc-{counter}'),
    ]
