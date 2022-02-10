from rest_framework import serializers, generics, permissions, pagination
from techowiz.models.user import User
from techowiz.api.admin.pagination import DefaultPagination


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'avatar',
            'is_active',
            'is_admin',
            'is_instructor',
            'is_staff'
        ]


class UserDetailSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'password',
            'first_name',
            'last_name',
            'gender',
            'date_of_birth',
            'phone',
            'avatar',
            'is_active',
            'is_admin',
            'is_instructor',
            'is_staff',
            'password_reset_required',
            'last_login',
            'last_logout',
            'last_login_ip',
            'last_login_user_agent',
            'is_email_verified',
            'is_phone_verified',
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        return user

    def update(self, instance, validated_data):
        if validated_data.get('email'):
            email = validated_data.pop('email')
    
        if validated_data.get('password'):
            password = validated_data.pop('password')
            instance.set_password = password
            instance.save()
        return super().update(instance, validated_data)


class UserListView(generics.ListAPIView):
    serializer_class = UserListSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    pagination_class = DefaultPagination


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


class UserDeleteView(generics.DestroyAPIView):
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]