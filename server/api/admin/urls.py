from django.urls import path
from server.api.admin.views.users import UserListView, UserCreateView, UserDetailView, UserUpdateView, UserDeleteView


urlpatterns = [
    path('users/', UserListView.as_view()),                                 # GET - /admin/users/
    path('users/create/', UserCreateView.as_view()),                        # POST - /admin/users/create/
    path('users/<uuid:pk>/', UserDetailView.as_view()),                     # GET - /admin/users/:id/
    path('users/<uuid:pk>/update/', UserUpdateView.as_view()),              # PUT, PATCH - /admin/users/:id/update/
    path('users/<uuid:pk>/delete/', UserDeleteView.as_view()),              # DELETE  - /admin/users/:id/delete/
]