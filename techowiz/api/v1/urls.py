import os
from django.urls import path
from techowiz.api.v1.auth.views import LoginView, PasswordResetView, EmailVerifyView, RegisterView, ProfileDetailView, StatusView, GoogleCallbackView
from techowiz.api.v1.programs.views import ProgramListView, ProgramDetailView, ProgramEnrolledView, LessonListView
from techowiz.api.v1.orders.views import OrderCreateView, OrderProcessView, payment_view, OrderListView


urlpatterns = [
    path('auth/status/', StatusView.as_view()),                                 # GET - v1/auth/status/
    path('auth/register/', RegisterView.as_view()),                             # POST - v1/auth/register/
    path('auth/login/', LoginView.as_view()),                                   # POST - v1/auth/login/
    path('auth/verify/', EmailVerifyView.as_view()),                            # GET - v1/auth/verify/?verify_token=
    path('auth/password_reset/', PasswordResetView.as_view()),                  # GET, POST, PUT - v1/auth/password_reset/?reset_token=
    path('auth/profile/', ProfileDetailView.as_view()),                         # GET, PUT - v1/auth/profile/
    path('auth/oauth/google/callback', GoogleCallbackView.as_view()),           # GET - v1/auth/oauth/google/callback/?code=&type=login, register

    path('orders/', OrderListView.as_view()),                                   # GET - v1/orders/
    path('orders/create/', OrderCreateView.as_view()),                          # GET - v1/orders/create/?program_id=&coupon_code=
    path('orders/<str:order_id>/process/', OrderProcessView.as_view()),         # POST - v1/orders/:order_id/process/
    
    path('programs/', ProgramListView.as_view()),                               # GET - v1/programs/
    path('programs/<uuid:pk>/', ProgramDetailView.as_view()),                   # GET - v1/programs/:pk/
    path('programs/enrolled/', ProgramEnrolledView.as_view()),                  # GET - v1/programs/enrolled/
    path('programs/<uuid:program_id>/lessons/', LessonListView.as_view()),      # GET - v1/programs/:program_id/lessons
]

mode = os.environ.get('DJANGO_SETTINGS_MODULE')
if mode == 'development':
    urlpatterns += [
        path('orders/<str:order_id>/payment/', payment_view),                   # GET - v1/orders/payment/
    ]