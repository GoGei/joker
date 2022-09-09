from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from Api.serializers import EmptySerializer


class ApiActions(object):
    CREATE = 'create'
    RETRIEVE = 'retrieve'
    UPDATE = 'update'
    PARTIAL_UPDATE = 'partial_update'
    DESTROY = 'destroy'
    LIST = 'list'

    ARCHIVE = 'archive'
    RESTORE = 'restore'


class MappedSerializerVMixin(viewsets.GenericViewSet):
    """
    viewset to specify serializer mapping
    serializer_map = {
        ApiActions.LIST: ListSerializer,
        ApiActions.CREATE: CreateSerializer,
        ...
    }
    empty_serializers = ('action1', 'action2', ...)
    """
    serializer_map = dict()
    empty_serializers = tuple()

    def get_serializer_class(self):
        action = self.action
        if action in self.empty_serializers:
            return EmptySerializer
        return self.serializer_map.get(action, self.serializer_class)


class ArchiveRestoreMixin(MappedSerializerVMixin):
    """
    Implement functionality of archive/restore action from
    core.Utils.Mixins.models.CrmMixin archive/restore actions
    """
    empty_serializers = (ApiActions.ARCHIVE, ApiActions.RESTORE)

    @action(methods=['post'], detail=True, url_path='archive', url_name='archive')
    def archive(self, request, pk=None):
        obj = self.get_object()
        obj.archive()
        return Response('Object is archived', status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path='restore', url_name='restore')
    def restore(self, request, pk=None):
        obj = self.get_object()
        obj.restore()
        return Response('Object is restored', status=status.HTTP_200_OK)


class UpdateCrmMixin(mixins.UpdateModelMixin, MappedSerializerVMixin):
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        instance.modify(request.user)

        return Response(serializer.data)


class CrmMixin(ArchiveRestoreMixin, UpdateCrmMixin):
    pass
