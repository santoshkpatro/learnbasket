from django.urls import path
from techowiz.api.v1.auth.views import LoginView, PasswordResetView, EmailVerifyView, RegisterView, ProfileDetailView
from techowiz.api.v1.programs.views import ProgramListView, ProgramDetailView, ProgramEnrolledView
from techowiz.api.v1.orders.views import OrderCreateView, OrderProcessView, payment_view, OrderListView


urlpatterns = [
    path('auth/register/', RegisterView.as_view()),                             # POST - /auth/register/
    path('auth/login/', LoginView.as_view()),                                   # POST - /auth/login/
    path('auth/verify/', EmailVerifyView.as_view()),                            # GET - /auth/verify/?verify_token=
    path('auth/password_reset/', PasswordResetView.as_view()),                  # GET, POST, PUT - /auth/password_reset/?reset_token=
    path('auth/profile/', ProfileDetailView.as_view()),                         # GET, PUT - /auth/profile/
    
    path('programs/', ProgramListView.as_view()),                               # GET - /programs/
    path('programs/<uuid:pk>/', ProgramDetailView.as_view()),                   # GET - /programs/:pk/
    path('programs/enrolled/', ProgramEnrolledView.as_view()),                  # GET - /programs/enrolled/

    path('orders/', OrderListView.as_view()),                                   # GET - /orders/
    path('orders/create/', OrderCreateView.as_view()),                          # GET - /orders/create/?program_id=&coupon_code=
    path('orders/<str:order_id>/process/', OrderProcessView.as_view()),         # POST - /orders/:order_id/process/
    path('orders/<str:order_id>/payment/', payment_view),                       # Development - GET - /orders/payment/
]