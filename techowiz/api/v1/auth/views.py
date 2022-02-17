import jwt
import requests
from django.contrib.auth import authenticate
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework import status, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from techowiz.api.v1.auth.serializers import LoginSerializer, PasswordResetSerializer, RegisterSerializer, ProfileSerializer
from techowiz.models.user import User


class StatusView(APIView):    
    def get(self, request):
        if request.user and request.user.is_authenticated:
            return Response(data={'detail': 'Logged in'}, status=status.HTTP_200_OK)
        else:
            return Response(data={'detail': 'Expired or logged out'}, status=status.HTTP_401_UNAUTHORIZED)


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

                message = render_to_string('verification_mail.html', {
                    'user': user,
                    'url': f'{settings.FRONTEND_BASE_URL}/auth/email_verify?verify_token={encoded_jwt}' 
                })

                # Send the encoded token in email
                send_mail('Welcome to Techowiz', message, 'support@techowiz.com', [user.email], fail_silently=True)

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
            message = render_to_string('password_reset_email', {
                'user': user,
                'url': f'{settings.FRONTEND_BASE_URL}/auth/password_reset/?reset_token={encoded_jwt}'
            })

            send_mail('Password Reset Email', message, 'noreply@techowiz.in', [user.email], fail_silently=True)
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


class GoogleCallbackView(APIView):
    def get(self, request):
        mode = request.query_params.get('mode', None)
        if not mode or mode not in ['login', 'register']:
            return Response(data={'detail': 'Please provide valid mode'}, status=status.HTTP_404_NOT_FOUND)

        code = request.query_params.get('code', None)
        if not code:
            return Response(data={'detail': 'Please provide authorization code'}, status=status.HTTP_404_NOT_FOUND)

        data = {
            'code': code,
            'client_id': settings.GOOGLE_CLIENT_ID,
            'client_secret': settings.GOOGLE_CLIENT_SECRET,
            'redirect_uri': settings.GOOGLE_REDIRECT_URI,
            'grant_type': 'authorization_code'
        }

        token_response = requests.post(settings.GOOGLE_TOKEN_URL, data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})

        if not token_response.status_code == status.HTTP_200_OK:
            return Response(data={'detail': 'Unable to fetch details from google server'}, status=status.HTTP_400_BAD_REQUEST)

        token_response_data = token_response.json()
        access_token = token_response_data.get('access_token')
        
        profile_response = requests.get(settings.GOOGLE_PROFILE_URL, params={'access_token': access_token})

        if not profile_response.status_code == status.HTTP_200_OK:
            return Response(data={'detail': 'Unable to contact google server'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        profile_data = profile_response.json()

        if mode == 'register':
            try:
                existing_user = User.objects.get(email=profile_data['email'])
                if not existing_user.google_id:
                    existing_user.google_id = profile_data['google_id']
                    existing_user.save()
                    return Response(data={'detail': 'Google account connected'}, status=status.HTTP_200_OK)

                return Response(data={'detail': 'Account already exists'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            except User.DoesNotExist:
                user = User(email=profile_data['email'], google_id=profile_data['id'], first_name=profile_data['given_name'], last_name=profile_data['family_name'])
                user.save()
                # Send a welcome message
                return Response(data={'detail': 'Signed up with google success'}, status=status.HTTP_200_OK)
        elif mode == 'login':
            try:
                user = User.objects.get(email=profile_data['email'])
                if not user.google_id:
                    user.google_id = profile_data['id']
                    user.save()

                login_access_token = AccessToken.for_user(user)
                login_refresh_token = RefreshToken.for_user(user)

                return Response(data={'access_token': str(login_access_token), 'refresh_token': str(login_refresh_token)}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response(data={'detail': 'No account found'}, status=status.HTTP_404_NOT_FOUND)


