from rest_framework import serializers
from core.Utils.validators import PasswordValidators
from core.User.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'middle_name',
            'is_active',
            'is_staff',
        )
        read_only_fields = ('id',)


class UserSerializerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'is_active',
            'is_staff',
            'is_superuser',
        )
        read_only_fields = fields


class UserSerializerViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'middle_name',
            'is_active',
            'is_staff',
            'is_superuser',
        )
        read_only_fields = fields


class UserSetPasswordSerialzier(serializers.Serializer):
    password = serializers.CharField(validators=PasswordValidators)
    repeat_password = serializers.CharField(validators=PasswordValidators)

    def validate(self, data):
        if data.get('password') != data.get('repeat_password'):
            msg = 'Password mismatch!'
            raise serializers.ValidationError({'password': msg, 'repeat_password': msg})
        return data


class UserAdminViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
        )
