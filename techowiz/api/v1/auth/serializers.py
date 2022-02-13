from rest_framework import serializers
from techowiz.models.user import User


class RegisterSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=False)
    password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class PasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'avatar',
            'gender',
            'date_of_birth',
        ]