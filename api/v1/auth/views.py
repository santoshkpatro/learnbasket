import jwt
from django.contrib.auth import authenticate
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from rest_framework import status, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from api.v1.auth.serializers import LoginSerializer, PasswordResetSerializer, RegisterSerializer, ProfileSerializer
from core.models.user import User


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            try:
                User.objects.get(email=email)
                return Response(data={'detail': 'User already exist with this email'}, status=status.HTTP_403_FORBIDDEN)
            except User.DoesNotExist:
                data = serializer.data
                password = data.pop('password')
                data.pop('confirm_password')
                user = User(**data)
                user.set_password(password)
                user.save()

                encoded_jwt = jwt.encode(
                    {
                        "email": user.email, 
                        "first_name": user.first_name
                    }, 
                    settings.SECRET_KEY,
                    algorithm="HS256"
                )

                # Send the encoded token in email
                send_mail('Email activation', f'Email activation link - {encoded_jwt}', 'support@techowiz.com', [user.email], fail_silently=True)

                return Response(data={'detail': 'Account created'}, status=status.HTTP_201_CREATED)
        else:
            return Response(data={'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class EmailVerifyView(APIView):
    def get(self, request):
        verify_token = request.query_params.get('verify_token', None)
        try:
            decoded = jwt.decode(verify_token, settings.SECRET_KEY, algorithms=["HS256"])
            email = decoded.get('email', None)
            if not email:
                return Response(data={'detail': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
            try:
                user = User.objects.get(email=email)
                user.is_email_verified = True
                user.save()
                return Response(data={'detail': 'User verified'}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response(data={'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except jwt.InvalidSignatureError:
            return Response(data={'detail': 'Invalid email activation token'}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(**serializer.data)
            if not user:
                return Response(data={'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

            if user.password_reset_required:
                return Response(data={'detail': 'Please reset your password to continue'}, status=status.HTTP_307_TEMPORARY_REDIRECT)
            
            user.last_login_ip = request.META['REMOTE_ADDR']
            user.save()

            return Response(data={
                'access_token': str(AccessToken.for_user(user)),
                'refresh_token': str(RefreshToken.for_user(user))
            })
        else:
            return Response(data={'detail': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    def get(self, request):
        reset_token = request.query_params.get('reset_token', None)
        if not reset_token:
            return Response(data={'detail': 'Reset token not found'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payload = jwt.decode(reset_token, settings.SECRET_KEY, algorithms=["HS256"])
            email = payload.get('email')
            try:
                User.objects.get(email=email, is_active=True)
                return Response(data={'detail': 'Valid token'}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response(data={'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except jwt.ExpiredSignatureError:
            return Response(data={'detail': 'Password reset token has expired'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidSignatureError:
            return Response(data={'detail': 'Invalid password reset token'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        email = request.data.get('email', None)
        if not email:
            return Response(data={'detail': 'Email not found'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email, is_active=True)
            encoded_jwt = jwt.encode(
                {
                    "email": user.email, 
                    "exp": timezone.now() + timezone.timedelta(minutes=15)
                }, 
                settings.SECRET_KEY,
                algorithm="HS256"
            )
            # Send password reset email
            send_mail('Password Reset Email', f'Password reset token - {encoded_jwt}', 'support@techowiz.com', [user.email], fail_silently=True)
            return Response(data={'detail': 'Password reset email has been sent'}, status=status.HTTP_201_CREATED)

        except User.DoesNotExist:
            return Response(data={'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        reset_token = request.query_params.get('reset_token', None)
        if not reset_token:
            return Response(data={'detail': 'Reset token not found'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = PasswordResetSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={'detail': 'Invalid password input'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payload = jwt.decode(reset_token, settings.SECRET_KEY, algorithms=["HS256"])
            email = payload.get('email')
            try:
                user = User.objects.get(email=email, is_active=True)

                # Reset password
                user.set_password(serializer.data.get('password'))
                user.save()

                return Response(data={'detail': 'Password reset success'}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response(data={'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except jwt.ExpiredSignatureError:
            return Response(data={'detail': 'Password reset token has expired'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidSignatureError:
            return Response(data={'detail': 'Invalid password reset token'}, status=status.HTTP_400_BAD_REQUEST)



class ProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = User.objects.filter(is_active=True)
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        return user