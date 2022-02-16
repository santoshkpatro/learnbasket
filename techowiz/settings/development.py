import os
from techowiz.settings.base import *
from datetime import timedelta
from dotenv import load_dotenv

# Load credntials from .env
load_dotenv()

# REST FRAMEWORK SIMPLEJWT CONFIG
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=3),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# RAZORPAY
RAZORPAY_KEY_ID = os.environ.get('RAZORPAY_KEY_ID')
RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET')

# CORS
CORS_ALLOW_ALL_ORIGINS = True

# CELERY
# CELERY_RESULT_BACKEND = 'redis://localhost'
# CELERY_BROKER = 'redis://localhost'

# FRONTEND DETAILS
FRONTEND_BASE_URL = os.environ.get('FRONTEND_BASE_URL', 'http:127.0.0.1:3000')

# GOOGLE OAUTH
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
GOOGLE_REDIRECT_URI = os.environ.get('GOOGLE_REDIRECT_URI')
GOOGLE_TOKEN_URL = os.environ.get('GOOGLE_TOKEN_URL', 'https://oauth2.googleapis.com/token')
GOOGLE_PROFILE_URL = os.environ.get('GOOGLE_PROFILE_URL', 'https://www.googleapis.com/oauth2/v2/userinfo')