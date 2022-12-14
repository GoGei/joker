from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response

from Api.base_views import MappedSerializerVMixin, ApiActions

from core.User.models import User
from core.Privilege.models import PrivilegeUser
from .serializers import (
    UserSerializer, UserSerializerListSerializer, UserSerializerViewSerializer, UserSetPasswordSerialzier,
    UserAdminViewSerializer
)


class UserViewSet(viewsets.ModelViewSet, MappedSerializerVMixin):
    queryset = User.objects.all().order_by('email')
    serializer_class = UserSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ('username', 'email')
    ordering_fields = ('username', 'email')
    filterset_fields = ('is_staff', 'is_superuser', 'is_active')

    serializer_map = {
        ApiActions.LIST: UserSerializerListSerializer,
        ApiActions.RETRIEVE: UserSerializerViewSerializer,
        'set_password': UserSetPasswordSerialzier
    }

    class Meta:
        model = User

    @action(detail=True, methods=['post'], url_path='set-password', url_name='set-password')
    def set_password(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user = self.get_object()
        user.set_password(data['password'])
        user.save()
        return Response(f'Password set to user {user.label}', status=status.HTTP_200_OK)


class UserAdminViewSet(viewsets.ReadOnlyModelViewSet, MappedSerializerVMixin):
    queryset = User.objects.all().filter(is_active=True, is_superuser=False).order_by('email')
    serializer_class = UserAdminViewSerializer
    permission_classes = (AllowAny,)

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ('email',)
    ordering_fields = ('email',)

    class Meta:
        model = User

    def get_queryset(self):
        queryset = self.queryset
        params = self.request.query_params

        unprivileged = params.get('unprivileged')
        if unprivileged:
            privileged = PrivilegeUser.objects.all().values_list('user_id', flat=True)
            queryset = queryset.exclude(id__in=privileged)

        return queryset
