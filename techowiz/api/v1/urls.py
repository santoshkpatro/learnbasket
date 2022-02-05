from django.urls import path
from techowiz.api.v1.auth.views import LoginView, PasswordResetView, EmailVerifyView, RegisterView, ProfileDetailView
from techowiz.api.v1.programs.views import ProgramListView, ProgramDetailView, ProgramEnrolledView

urlpatterns = [
    path('auth/register/', RegisterView.as_view()),                             # POST - /auth/register/
    path('auth/login/', LoginView.as_view()),                                   # POST - /auth/login/
    path('auth/verify/', EmailVerifyView.as_view()),                            # GET - /auth/verify/?verify_token=
    path('auth/password_reset/', PasswordResetView.as_view()),                  # GET, POST, PUT - /auth/password_reset/?reset_token=
    path('auth/profile/', ProfileDetailView.as_view()),                         # GET, PUT - /auth/profile/
    
    path('programs/', ProgramListView.as_view()),                               # GET - /programs/
    path('programs/<uuid:pk>/', ProgramDetailView.as_view()),                   # GET - /programs/:pk/
    path('programs/enrolled/', ProgramEnrolledView.as_view()),                  # GET - /programs/enrolled/
]